import subprocess
import csv
import json

# Define the variables
user = "user"
password = "password"
cluster = "clustersname.xxxxxxx.mongodb.net"
filetype = "csv"

# Define a list of databases and collections
dbs = [
    {
        "name" : "db1",
        "collections" : [
            ...
        ]
    },
    {
        "name" : "db2",
        "collections" : [
            ...
        ]
    },
    {
        "name" : "db3",
        "collections" : [
            ...
        ]
    },
    {
        "name" : "db4",
        "collections" : [
           ...
        ]
    }
]
        
# Loop over the databases and collections and run the command
for db in dbs:
    for collection in db["collections"]:
        filename = f"{collection}.{filetype}"
        
        with open(f"mongodb_exports/{db['name']}/{db['name']}_{filename}", 'r') as file:
            reader = csv.reader(file, delimiter = '\t')
            for line in reader:
                data = json.loads(line[0])
                break
            
        fields = []
        for i, key in enumerate(data):
            fields.append(key)

        fields = ",".join(fields)
        fields_str = f'"{fields}"'
        
        command = f"mongoexport --uri=\"mongodb+srv://{user}:{password}@{cluster}/{db['name']}\" --collection {collection} --out mongodb/processed/{db['name']}/{collection}/{filename} --type csv -f {fields_str}"
        subprocess.run(command, shell=True)
      