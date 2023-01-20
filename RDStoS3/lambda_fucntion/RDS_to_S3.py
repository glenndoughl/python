from sqlalchemy import create_engine, engine
from sqlalchemy.sql import text
from custom_query import query
from datetime import datetime
from io import StringIO
import boto3
import json
import csv

def extract(event,context):
    #import read config.json as args
    args = json.load(open("config.json"))
    
    #current date
    dt = (datetime.now()).strftime("%Y%m%d")
    
    #generate url for engine creation
    url_obj = engine.URL.create(
        args["dbengine"],           #postgresql+psycopg2 or mysql+pymysql
        username=args["dbuser"],
        password=args["dbpassword"],
        host=args["dbhost"],
        database=args["dbname"],
        port=args["dbport"]
        )
    
    #creation and connection to the db engine
    engn = create_engine(url_obj, echo=True)
    conn = engn.connect()
    
    #query execution    
    result = engn.execute(text(query))
    
    #get the header and data from the query result
    header = result.keys()
    data = result.fetchall()
    
    #writing header and data to a generated csv file
    output = StringIO()
    writer = csv.writer(output, delimiter=",")
    writer.writerow(header)
    writer.writerows(data)
    
    #saving the generated csv file to the specified S3 bucket
    s3_resource = boto3.resource('s3')
    s3_resource.Object(f'{args["bucket"]}', rf'{args["path"]}/{args["filename"]}{dt}.csv').put(Body=output.getvalue())

    return "DONE"