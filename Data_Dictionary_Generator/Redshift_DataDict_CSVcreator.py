import boto3
import re
import json
import time
import csv
from botocore.config import Config

stage = ""
cluster_name = ""
db = ""
db_user = ""
prod_region = ""
partner_name = ""
rgx = f"regex"
query = "SELECT * FROM {SCHEMA}.{TABLE} LIMIT 1;"

#create a redshift client using boto3
my_config = Config(
    region_name = prod_region
)
redshift = boto3.client('redshift-data', config=my_config)

#get schemas for facebook and google ads
response = redshift.list_schemas(
    ClusterIdentifier=cluster_name,
    Database=db,
    DbUser=db_user,
    )

# List all schemas that will satisfy the given regex expression
schemas = [schema for schema in response["Schemas"] if re.findall(rgx, schema)]

# create a csv file and open it in write mode, create a csv writer then write the column names
with open(f"{partner_name}_{stage}_data_dictionary.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['schema','table','column','column_name_order','type','sample'])
    
# iterate over every schema in the schema list
    for schema in schemas:
        #list tables in the schema
        response = redshift.list_tables(
            ClusterIdentifier=cluster_name,
            Database=db,
            DbUser=db_user,
            SchemaPattern=schema
        )
        #get all table descriptions within the schema
        table_desc = [desc for desc in response["Tables"]]
        #get table names within the schama
        tables = [table["name"] for table in table_desc if table["type"] == 'TABLE']
        
        #iterate over all the tables within the schema
        for table in tables:
            #format the sql query
            sql = query.format(
                    SCHEMA = schema,
                    TABLE = table
                    )
            #try to execute the sql query
            try:    
                response = redshift.execute_statement(
                    ClusterIdentifier = cluster_name,
                    Database = db,
                    DbUser = db_user,
                    Sql = sql
                    )
            except:
                pass
            
            #get the query execution ID
            query_id = response["Id"]

            # while loop the query is still Running
            while True:
                #describe the query execution ID
                response = redshift.describe_statement(Id = query_id)
                
                #check if the query is done
                if response["Status"] == "FINISHED":
                    # get execution result
                    response = redshift.get_statement_result(Id=query_id)
                    
                    #check if table is empty
                    if not bool(response["Records"]):
                        writer.writerow([schema,table,None,None,None,None])
                        print(f"[ EMPTY ] {schema}.{table}")
                        break
                    
                    # iterate over each column of the query result
                    for i in range(len(response["ColumnMetadata"])):
                        #iterate over resulting record/values
                        for _, key in enumerate(response['Records'][0][i]):
                            #get column name, column type, column sample value for each column iterations
                            col_name = response['ColumnMetadata'][i]['name']
                            col_type = response['ColumnMetadata'][i]['typeName']
                            sample_val = 'NULL' if 'Null' in f"{response['Records'][0][i]}" else response['Records'][0][i][key]
                            
                            #write the column details to csv
                            writer.writerow([schema,table,col_name,i,col_type,sample_val])
                            
                            # once successfuly done, print shcema name, table name and status of the query
                    print(f"{schema}.{table} - FINISHED")
                    break
                    
                 #check if the query FAILED and print out the error message
                elif response["Status"] == "FAILED":
                    print(f'[ERROR] - {json.dumps(response["Error"], default=str)}')
                    break
                # if the query is still running, sleep for 2 seconds and retart the while loop
                else:
                    time.sleep(2)