# Project Name: CSV Reporter
# Created by: Glenn Latayan
# Address: Malvar Batangas Philippines
# Linkedin: https://www.linkedin.com/in/latayanglenn0920/
# Github:https://github.com/glenndoughl
# Documentation: https://github.com/code50/82019774/tree/main/project
# Completed On: December 22, 2022

#   DEMO : https://www.youtube.com/watch?v=iNPvc-AcAOs
 
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys
import re
import getpass
from datetime import datetime
from arguments import int_fields, flt_fields, str_fields, dict_lists, date_fields

def main():
    #creating an emply list -> "dq_issues" as global in order for functions named "check_***" to access it from main()
    global dq_issues
    dq_issues = []

    #custom function to read csv to pandas dataframe while also handling exceptions
    read_csv(input("ENTER CSV File Name or Directory: "))

    #"check_***" custom function for checking each record's data quality per data type of each specified column from csv file
    #also handles exeptions for column lists from arguments.py that are not existing in CSV file
    
    try:
        check_date_cols(date_fields)
        check_int_cols(int_fields)
        check_float_cols(flt_fields)
        check_string_cols(str_fields, dict_lists)
    except KeyError as error:
        sys.exit(f"*****FAIL! - Column '{error}' does not exist in CSV File*****")

    #if there are no issues passed to dq_issues list by "check_***" functions, proceed to next process
    
    if not dq_issues:
        print("*****SUCCESS! - Data Quality Checks*****")
        receiver = email_validation("Reciever")
        sender = email_validation("Sender")
        password = getpass.getpass() #"t k q b z j h x g y n g f t m n "
        email_report(receiver, sender, password)
        
    #if there are issues in dq_issues, it will show each issue per column per row, and the user have to correct the anomalies in the CSV file as shown
    else:
        print("*****FAIL! - Data Quality Checks*****")
        for issue in dq_issues:
            print(issue)

def read_csv(file:str):
    #read specified CSV File and handles exeptions
    try:
        global sales_df
        sales_df = pd.read_csv(file)
    except (FileNotFoundError):
        sys.exit(f"*****FAIL! - CSV upload*****\n --- {file} Could not be opened")
    else:
        print("*****SUCCESS! - CSV upload*****")
        return True

def check_date_cols(cols: list):
    #checks if date type columns pass regex for mm/dd/yyyy
    regex = r"((\d{2})|(\d))\/((\d{2})|(\d))\/((\d{4})|(\d{2}))"
    for field in cols:
        for dt in sales_df[field]:
            try:
                if(re.fullmatch(regex, dt)):
                    pass
                else:
                    raise ValueError
            except ValueError:
                index = sales_df[sales_df[field]==dt].index.values
                dq_issues.append(f"{field} Column: CSV Row{index+2} '{dt}' is not a Date")

    return True

def check_int_cols(cols: list) -> bool:
    #checks if each record per column in "cols" is int. otherwise generates a string stating anomaly with the column, row, and the record itself and attaches it to global "dq_issues"
    for field in cols:
        for num in sales_df[field]:
            try:
                if "." in str(num):
                    _, d = str(num).split(".")
                    if d == "0":
                        pass
                    else:
                        raise ValueError
                else:
                    int(num)
            except ValueError:
                index = sales_df[sales_df[field]==num].index.values
                dq_issues.append(f"{field} Column: CSV Row{index+2} '{num}' is not an Integer")

    return True

def check_float_cols(cols: list) -> bool:
    #checks if each record per column in "cols" is float. otherwise generates a string stating anomaly with the column, row, and the record itself and attaches it to global "dq_issues"
    for field in cols:
        for flt in sales_df[field]:
            try:
                float(flt)
            except ValueError:
                index = sales_df[sales_df[field]==flt].index.values
                dq_issues.append(f"{field} Column: CSV Row{index+2} '{flt}' is not a Float")

    return True

def check_string_cols(cols: list, ref: dict) -> bool:
    #checks if each record per column in "cols" is in the list of allowable values contained in "arguments.py" file per column.
    #otherwise generates a string stating anomaly with the column, row, and the record itself and attaches it to global "dq_issues"
    for field in cols:
        for word in sales_df[field]:
            try:
                if word.lower() in ref[field]:
                    pass
                else:
                    raise ValueError
            except ValueError:     
                index = sales_df[sales_df[field]==word].index.values
                dq_issues.append(f"{field} Column: CSV Row{index+2} [{word}] is not Acceptable {field}")
    
    return True

def email_validation(owner: str):
    #gets either the Receiver or Sender's email and check ii if it pass the regex check. Otherwise it will continue to ask use for an email until it satify the regex pattern
    regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    while True:
        email = input(f"ENTER {owner}'s Email: ")
        try:
            if(re.fullmatch(regex, email)):
                return email
            else:
                raise ValueError
        except ValueError:
            print("*!!!Invalid Email Address!!!*")
            pass
    
def email_report(receiver, sender, password, ):
    #groups and aggregates the pandas dataframe from CSV and stores it to "report_df"
    report_df = sales_df.groupby(["City","Category","Product"]).agg({"Quantity": "sum", "TotalPrice": "sum"})

    #setting up email parameters
    emsg = MIMEMultipart('alternative')
    emsg["To"] = receiver
    emsg["Subject"] = f"[CS50 Final Project] Food Sales Report (Automated {datetime.now()})"
    emsg["From"] = sender

    #emai content in HTML
    html_txt = """\
    <!DOCTYPE html>
    <html>
    <head>
    <!-- HTML Codes by Quackit.com -->
    <title>
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body {background-color:#ffffff;background-repeat:no-repeat;background-position:top left;background-attachment:fixed;}
    h1{font-family:Impact, sans-serif;color:#000000;background-color:#ffffff;}
    p {font-family:Verdana, sans-serif;font-size:14px;font-style:normal;font-weight:normal;color:#000000;background-color:#ffffff;}
    </style>
    </head>
    <body>
    <p>
    Hello,

    Below is a table describing Total Sales (in USD) & Total items sold per Product per Category per City:
    </p>
    <h1>Foood Sales Summary Table</h1>
    </body>
    </html>
    """

    #converting the pandas dataframe "repord_df" to HTML to be displayed properly on the email body
    html_tbl = """\
    <html>
    <head></head>
    <body>
        {0}
    </body>
    </html>
    """.format(report_df.to_html())

    #email signature
    html_sig = """\
    <!DOCTYPE html>
    <html>
    <head>
    <!-- HTML Codes by Quackit.com -->
    <title>
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <h1></h1>
    <p>Thanks! Regards,</p>
    <p>Glenn Latayan @ CS50P</p>
    </body>
    </html>"""

    #combines all the above html content for the email
    html = html_txt + html_tbl + html_sig

    #configuring the email body
    body = MIMEText(html, 'html')
    emsg.attach(body)

    #setting up the gmail server connection (GMAIL ONLY!!!!)
    conn = smtplib.SMTP("smtp.gmail.com", 587)
    conn.starttls()
    #logging in to gmail
    try:
        conn.login(sender, password)
        print("*****SUCCESS! - Gmail Login*****")
    except smtplib.SMTPAuthenticationError:
        sys.exit("""
*****FAIL! - Gmail Login*****
*****Please Check the Sender's Email and Password or refer to the guide links below*****
https://support.google.com/mail/?p=BadCredentials
https://support.google.com/accounts/answer/185833?hl=en
        """)

    #sending the email report
    conn.sendmail(sender, receiver, str(emsg))
    print("*****SUCCESS! - Email Sent*****")
    return True
    
if __name__ == "__main__":
    main()