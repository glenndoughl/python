import boto3
import re
import json
import time
from botocore.config import Config

stage = ""
cluster_name = ""
db = ""
db_user = ""
region = ""
partner_name = ""
rgx = ""
bucket = ""
iam = ""

# unload query
query = """UNLOAD ('SELECT *, TO_DATE(received_at, \\'YYYY-MM-DD\\') as received_date FROM {SCHEMA}.{TABLE}')
        TO '{BUCKET}{PARTNER_NAME}/{SCHEMA}/{TABLE}'
        IAM_ROLE '{IAM}'
        FORMAT PARQUET
        PARTITION BY (received_date) 
        ALLOWOVERWRITE;"""

#create a redshift client using boto3
my_config = Config(
    region_name = region
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
                TABLE = table,
                BUCKET = bucket,
                PARTNER_NAME = partner_name,
                IAM = iam 
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

        #check for status of the query while the query is still running
        while True:
            response = redshift.describe_statement(Id = query_id)
            if response["Status"] == "FINISHED":
                print(f"{schema}.{table} - {response['Status']}")
                break
            elif response["Status"] == "FAILED":
                print(f"Query Status - {response['Status']}")
                print(f'[ERROR] - {json.dumps(response["Error"], default=str)}')
                break
            else:
                print(response['Status'])
                time.sleep(2)