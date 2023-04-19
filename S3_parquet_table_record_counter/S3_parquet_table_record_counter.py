from pyspark.context import SparkContext
from pyspark.sql import SQLContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

import boto3
import re

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sc = SparkContext.getOrCreate()
sql = SQLContext(sc)
glueContext = GlueContext(sc)
spark = glueContext.spark_session

source = "bucketname"
prefix = ""
table_level = 3
regex = "regex"

s3_client = boto3.client('s3')

#lists objects in specified s3
paginator = s3_client.get_paginator('list_objects')
operation_parameters = {'Bucket': source,
                        'Prefix': prefix}
page_iterator = paginator.paginate(**operation_parameters)

#iterate over every object in the bucket then stores every object that are not a folder in a list
files = [file['Key'] for page in page_iterator for file in page['Contents'] if re.search(regex, file['Key'])]

# get the table level directory for every file in files
tl = table_level - 1
tables = set()
for i in range(len(files)):
    tables.add( '/'.join(files[i].split('/')[:tl]))

for table in tables:
    df = glueContext.create_dynamic_frame.from_options(
        connection_type = "s3",
        connection_options = {"paths": [f"s3://{source}/{table}"]},
        format_options = {
            "withHeader": True
            },
        format="parquet").toDF()

    if df.rdd.isEmpty():
        print(f"[{table}]: EMPTY")
        continue
    rows = f"{table} --- {df.count()} rows"
    print(rows)
    logger.info(rows)
    del df
