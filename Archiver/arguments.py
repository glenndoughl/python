from datetime import datetime
from dateutil.relativedelta import relativedelta

mm_mmmm = (datetime.now()-relativedelta(months=1)).strftime("%m %B")  #get current month in MM_MMMM format (ie: 10 October)
mmmm = (datetime.now()-relativedelta(months=1)).strftime("%m %B")  #get month in MMMM (ie: October)
yyyy = datetime.now().strftime("%Y") #get year in YYYY format (ie: 2022)


args = {
    "source_path" : {
        "bcq": r"C:\Users\glenn\OneDrive\Documents\babeProject",
        "mq": r""
        },
    "target_path" : {
        "bcq": r"C:\Users\glenn\OneDrive\Documents",
        "mq": r""
        },
    "output_filename" : {
        "bcq": f"BCQ OPTIMIZATION {mmmm} {yyyy}.xlsx",
        "mq": f""
        },
    "sheet_name" : {
        "bcq": "BCQ OPTIMIZATION",
        "mq": ""
        },
    "header_rows" : { #number of header rows
        "bcq": 3,
        "mq": 0
        }, 
    "body_rows" : { #number of body rows exclusive of header_rows
        "bcq": 288,
        "mq": 0
        }, 
    "file_name_regex": { #Regex pattern of the file names
        "bcq": r"^BCQ_202[0-9]{5}\.xlsm$",
        "mq": r"202[0-9]{5}\.xlsm$"
        },
    "body_skip_rows": {
        "bcq": 3,
        "mq": 0
    }
    }