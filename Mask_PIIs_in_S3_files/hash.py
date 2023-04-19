from awsglue.transforms import *
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pyspark.sql.functions as F
from pyspark.sql.functions import col, sha2, udf
import hash_congig

import boto3
import re

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

args = hash_congig

source = args['SOURCE']
target = args['TARGET']
prefix = args['PREFIX']
df_cols_to_hash = args['NORMAL_COLUMNS']
partner = args["partner_name"]
conn_type = args["CONNECTION_TYPE"]
str_typ_json_cols = args["STRINGTYPE_JSON_COLS"]


def main():
    #creates boto3 s3 client
    s3_client = boto3.client('s3')

    #lists objects in specified s3
    response = s3_client.list_objects_v2(
        Bucket=source,
        Prefix=prefix
    )

    #iterate over every object in the bucket then stores every object that are not a folder in a list
    files = [content['Key'] for content in response['Contents'] if re.search(rf'^.+\.\w+$', content['Key'])]
    
    #makes the custom function to Pyspark UDF
    custom_udf = udf(mask_stringtype_json_df_cols)
    
    #iterate over every file
    for file in files:
        #gets the file foramat
        _, file_format = file.split(".")

        #try to load the file to a DF
        try:
            df = glueContext.create_dynamic_frame.from_options(
                connection_type = conn_type,
                connection_options = {"paths": [f"s3://{source}/{file}"]},
                format_options = {
                    "withHeader": True,
                    "inferSchema": True
                    },
                format=file_format).toDF()
                
        except Exception as error:
            logger.warning(f"[{file}]: {error}")
            continue

        #creates an empty list to be used in df.select([list])
        final_cols = []

        #STARTS THE HASING PROCESS
        # iterate over all columns of the DF
        for column in df.columns:
            # if column is in normal column to hash list
            if column in df_cols_to_hash:
                final_cols.append(sha2(col(column), 512).alias(column))
            # if column is in json type columns to hash
            elif column in str_typ_json_cols["COLUMNS"]:
                # convert column type to StringType
                df = df.withColumn(column, col(column).cast(StringType()))
                # iterate over each keys to hash in json type columns
                for key in str_typ_json_cols["KEYS"]:
                    # apply the udf function that finds and replaces the original VALUE of the KEY with hashed string
                    df = df.withColumn(column, custom_udf(col(column), F.lit(key)))
                final_cols.append(column)
            #else, if not masking needed, just add the column directly to the final_cols list
            else:
                final_cols.append(column)

        #select all the the processed columns to be the final df
        final_df = df.select(final_cols)
        
        # try to save the final_df to a specified target buket
        try: 
            final_df.write.format(f'{file_format}').option("header", "true").mode("overwrite").save(f"s3://{target}/{partner}/archieve/{file}") 
        except:
            continue
                    
        logger.info(f"[{file}] SAVED")  
        del df

# custom function to find and replace substing of a string
def mask_stringtype_json_df_cols(string, key) -> str:
    # try to match the regex patern of a key value pair or dict item to the input string
    try:
        # gets the matched SUBSTRING
        matched = re.search(fr'"{key}": ("(.*?)")', string).group()
    except:
        # returns the original inputed string if there is no match
        return string
    else:
        # get the only string VALUE of the matched KEY VALUE PAIR 
        _, val = matched.split(':')
        # removes the double quotations
        val = val.replace('"','')
        # hashes the VALUE 
        val = hashlib.sha256(val.encode()).hexdigest()
        # combines the KEY and the hashed VALUE to create the KEY VALUE PAIR SUBSTRING
        result = f'"{key}": "{val}"'
        # replaces the original KEY VALUE substring with the hashed KEY VALUE then RETURN
        return re.sub(fr'"{key}": ("(.*?)")', result, string)

        
if __name__=="__main__":
    main()