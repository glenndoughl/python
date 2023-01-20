import os
import re
import sys
import time
import pandas as pd
from arguments import args

def main():
    startTime = time.time()

    while True:
        try:
            base = input("Enter 'BCQ' or 'MQ' (case does not matter): ").lower()
            if base in ["bcq", "mq"]:
                break
            else:
                raise ValueError
        except ValueError:
            print("Input is not BCQ or MQ!")
            pass


    # initialoizing variables from arguments.py file
    source_path = args["source_path"][base]
    target_path = args["target_path"][base]
    output_filename = args["output_filename"][base]
    sheet_name = args["sheet_name"][base]
    header_rows = args["header_rows"][base]
    body_rows = args["body_rows"][base]
    file_name_regex = args["file_name_regex"][base]
    body_skip_rows = args["body_skip_rows"][base]

    #Creating Dictionary as Functions Parameters
    params = {
    "source_path" : source_path,
    "target_path" : target_path,
    "output_filename" : output_filename,
    "sheet_name" : sheet_name,
    "header_rows" : header_rows,
    "body_rows" : body_rows,
    "file_name_regex": file_name_regex,
    "body_skip_rows": body_skip_rows
    }

    #calling functions list_file_names & combine_excel
    files = list_file_names(source_path, params)
    combine_excel(params,files)

    executionTime = (time.time() - startTime)/60
    print(f"Execution time: {executionTime:.2f} mins")

def list_file_names(dir: str, params: dict):
    file_names = []

    # Get the List of all the available files in the specified source path
    print(f'Source: "{dir}"')
    try:
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)):
                if re.match(params["source_path"], path):
                    file_names.append(path)
        print(f"""{len(file_names)} FILES are now processing:
        {file_names}
        """)

    except FileNotFoundError:
        sys.exit(f'File or Directory: "{params["source_path"]}" not found!')

    return file_names

def combine_excel(params: dict, files: list):

    #Get File Header only
    df = pd.read_excel(
        rf'{params["source_path"]}\{files[0]}',
        sheet_name=params["sheet_name"],
        header=None
        )
    df = df.iloc[:params["header_rows"]]
    print(f"Adding {len(df)} rows of Header")

    #loop through all files and append the data to the df
    for file in files:
        temp_dfs = pd.DataFrame()
        temp_dfs = pd.read_excel(
            rf'{params["source_path"]}\{file}', 
            skiprows=params["body_skip_rows"], header=None, 
            sheet_name=params["sheet_name"]
            )
        temp_dfs = temp_dfs.iloc[:params["body_rows"]]
        df = pd.concat([df, temp_dfs])
        print(f"Adding {len(temp_dfs)} rows of body from {file}")
    
    #save the resulting df to the specified path
    print(f"SAVING {params['output_filename']} to {params['source_path']}")
    df.to_excel(
        engine='xlsxwriter',
        excel_writer = rf'{params["target_path"]}\{params["output_filename"]}',
        sheet_name = params["sheet_name"],
        index = False,
    )

    print(f'{len(df)} Total rows Added to {params["output_filename"]}')
    
if __name__=="__main__":
    main()