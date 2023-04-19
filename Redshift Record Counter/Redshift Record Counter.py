import boto3
import re
import json
import time
from botocore.config import Config


cluster_name = ""
db = f""
db_user = ""
region = ""
partner_name = ""
rgx = f""
bucket = ""


# unload query
query = "SELECT \'{SCHEMA}.{TABLE}\' source, COUNT(*) FROM {SCHEMA}.{TABLE}"

#create a redshift client using boto3
my_config = Config(
    region_name = region
)
redshift = boto3.client('redshift-data', config=my_config)

queries = []

#get schemas for facebook and google ads
response = redshift.list_schemas(
    ClusterIdentifier=cluster_name,
    Database=db,
    DbUser=db_user,
    )

# List all schemas that will satisfy the given regex expression
schemas = [schema for schema in response["Schemas"] if re.findall(rgx, schema)]

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
    
    for table in sorted(tables):
        #format the sql query
        sql = query.format(
                SCHEMA = schema,
                TABLE = table
                )
        queries.append(sql)
                
    query_all = " UNION ALL ".join(queries)

    try:    
        response = redshift.execute_statement(
            ClusterIdentifier = cluster_name,
            Database = db,
            DbUser = db_user,
            Sql = query_all
            )
    except:
        pass
    query_id = response["Id"]

    while True:
                response = redshift.describe_statement(Id = query_id)
                if response["Status"] == "FINISHED":
                    result = redshift.get_statement_result(
                        Id=query_id
                    )
                    for result in result["Records"]:
                        if result[1]['longValue'] > 0:
                            print(f"{result[0]['stringValue']} --- {result[1]['longValue']}")
                            
                    break
                elif response["Status"] == "FAILED":
                    print(f"Query Status - {response['Status']}")
                    print(f'[ERROR] - {json.dumps(response["Error"], default=str)}')
                    break
                else:
                    time.sleep(1)
        