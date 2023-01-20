import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import sys
import re
import getpass
from datetime import datetime
from arguments import int_fields, flt_fields, str_fields, dict_lists

def main():
    global dq_issues
    dq_issues = []

    read_csv("samplefoodsales.csv")
    check_int_cols(int_fields)
    check_float_cols(flt_fields)
    check_string_cols(str_fields, dict_lists)

    if dq_issues:
        print("*****FAIL! - Data Quality Checks*****")
        for issue in dq_issues:
            print(issue)

    else:
        print("*****SUCCESS! - Data Quality Checks*****")
        receiver = email_validation(input("Receiver Email: "))#"glenndoughl@gmail.com"
        sender = email_validation(input("Sender Email: ")) #"glennlatayan.cs50@gmail.com")
        password = getpass.getpass() #"t k q b z j h x g y n g f t m n " 
        email_report(receiver, sender, password)

def read_csv(file:str):
    try:
        global sales_df
        sales_df = pd.read_csv(file)
    except (FileNotFoundError):
        sys.exit(f"*****FAIL! - CSV upload*****\n --- '{file}' Could not be opened")
    else:
        print("*****SUCCESS! - CSV upload*****")
        return True

def check_int_cols(cols: list) -> bool:
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
                dq_issues.append(f"{field} Column: CSV Row{index+2} '{num}' is not an INT")
    return True

def check_float_cols(cols: list) -> bool:
    for field in cols:
        for flt in sales_df[field]:
            try:
                float(flt)
            except ValueError:
                index = sales_df[sales_df[field]==flt].index.values
                dq_issues.append(f"{field} Column: CSV Row{index+2} '{flt}' is not a FLOAT")
    return True

def check_string_cols(cols: list, ref: dict) -> bool:
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

def email_validation(email: str) -> str:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    try:
        if(re.fullmatch(regex, email)):
            return email
        else:
            raise ValueError
    except ValueError:
        sys.exit("Invalid Email Address")

def email_report(receiver, sender, password, ):
    global report_df
    report_df = sales_df.groupby(["City","Category","Product"]).agg({"Quantity": "sum", "TotalPrice": "sum"})

    emsg = MIMEMultipart('alternative')
    emsg["To"] = receiver
    emsg["Subject"] = f"[CS50 Final Project] Food Sales Report (Automated {datetime.now()})"
    emsg["From"] = sender

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
    <p>Hello,</p>
    <p>Below is a table describing Total Sales (in USD) & Total items sold per Product per Category per City:</p>
    <h1>Foood Sales Summary Table</h1>
    </body>
    </html>
    """

    html_tbl = """\
    <html>
    <head></head>
    <body>
        {0}
    </body>
    </html>
    """.format(report_df.to_html())

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


    html = html_txt + html_tbl + html_sig


    body = MIMEText(html, 'html')
    emsg.attach(body)

    conn = smtplib.SMTP("smtp.gmail.com", 587)
    conn.starttls()
    conn.login(sender, password)
    print("*****SUCCESS! - Gmail Login*****")
    conn.sendmail(sender, receiver, str(emsg))
    print("*****SUCCESS! - Email Sent*****")
    return True

if __name__ == "__main__":
    main()