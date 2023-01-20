# CSV Reporter

## __Introduction__
This project is created as a requirement for [CS50's Introduction to Programming with Python](https://pages.github.com/) as the Final Project.

The project takes raw sales data from a CSV File, with specified Columns, and summarizes it to produce a Sales Summary Table, which will included in the body of an email to be sent as part of a sales report via Gmail.

__This Project features:__
* CSV File Checking
* Column Name Checking
* Record Data type Checking
    * Date
    * Integer
    * Float
    * String
* Table Groupby and Aggregation
* Regex Email Address Validation
* Gmail Email Sending

## __Dependencies__

The __main()__ function in project.py will be needing several other files.

1. __Sales CSV File with the following columns:__
    * OrderDate
    * Region
    * City
    * Category
    * Product
    * Quantity
    * UnitPrice
    * TotalPrice

    This CSV file will provide the data it needs to continue with the succeeding proccesses.

2. __Arguments Pyhton file consisting of :__
    * Lists [ ] of Acceptable Values for each String Type Columns
        * Cities [ ]
        * Regions [ ]
        * Categories [ ]
        * Products [ ]
    * Dictionary{} realting the Column names to ther Acceptable Value Lists
        * Dictionary of Acceptable String List { "Column" : [ Acceptable Values ] }
    * Lists [ ] of Columns per Data type
        * Date [ ]
        * Integer [ ]
        * Float [ ]
        * String [ ]

    The said Argument Python File will provide most of the project's custom function's needed arguments in order to execute correctly.
3. __Requirements Text File with the needed names of pip installable libraries__
    * [__pandas__](https://pypi.org/project/pandas/)

    Pandas Library will be the only pip installable library used for this project. Pandas will be used to read the CSV File's Data in to Pandas' DataFrame, Process data, and produce the Sales Summary Table for the email report.
4. __Active Gmail Account for Sender and Receiver__

    An active gmail __Sender__ account will be needed in order to send the generated report. However, some steps are needed to be done in order for a gmail account to be used with python.

    A differrent google generated password should be used. 

    To generate the separate password please follow the steps in this link: [__Generate Google App Password__](https://support.google.com/accounts/answer/185833?hl=en)

## Work Flow

Upon runing the program

    ~/project_folder> python project.py
You will be asked to enter the CSV File Name or Directory

    ENTER CSV File Name or Directory: 
The program will try to open the said file using Pandas.

If the File Name or Directory is non existet, or the file type is not in .csv, The program will return a handled exception and will terminate.

    ENTER CSV File Name or Directory: notexist.csv
    *****FAIL! - CSV upload*****
    --- notexist.csv Could not be opened

If it opes the file successfuly it will then begin the checks needed for data quality.

If the Data Quality checks catches anomalies, these anomalies will be shown, and the program will terminate

    *****SUCCESS! - CSV upload*****
    *****FAIL! - Column ''Region'' does not exist in CSV File*****

or

    ENTER CSV File Name or Directory: errors.csv
    *****SUCCESS! - CSV upload*****
    *****FAIL! - Data Quality Checks*****
    OrderDate Column: CSV Row[2] '1/1/202x' is not a Date
    Quantity Column: CSV Row[5] '82x' is not an Integer
    Quantity Column: CSV Row[9] '51.2' is not an Integer
    TotalPrice Column: CSV Row[7] '95.58c' is not a Float
    Region Column: CSV Row[3] [Southeast] is not Acceptable Region
    City Column: CSV Row[4] [LosAngeles] is not Acceptable City
    Category Column: CSV Row[4] [Cokies] is not Acceptable Category

At this point, the records in the columns and rows specified should be corrected or removed to paas all Data Quality Checks

After passing all the Data Quality checks, the program will then generate the Sales Summary Table using pandas. Then it will ask for the Reciever and Sender email addresses

    ENTER CSV File Name or Directory: sales.csv  
    *****SUCCESS! - CSV upload*****
    *****SUCCESS! - Data Quality Checks*****
    ENTER Reciever's Email: receiver@gmail.com
    ENTER Sender's Email: sender@gmail.com

The program is also equiped of Regex email pattern validation. If the entered email for either Receiver or Sender is invalid, the program will continue to loop back on asking for an email until the it satifies the Regex Validation.

    ENTER CSV File Name or Directory: sales.csv
    *****SUCCESS! - CSV upload*****
    *****SUCCESS! - Data Quality Checks*****
    ENTER Reciever's Email: email.com 
    *!!!Invalid Email Address!!!*
    ENTER Reciever's Email: email@gmail
    *!!!Invalid Email Address!!!*
    ENTER Reciever's Email: email@gmail.com
    ENTER Sender's Email: email.com
    *!!!Invalid Email Address!!!*
    ENTER Sender's Email: email@gmail..    
    *!!!Invalid Email Address!!!*
    ENTER Sender's Email: email@gmail.com 

Once Receiver and Sender's email addresses are validated,
it will ask for the Sender's email password. In entering the password, __getpass.getpass()__ is used to encrypt the password input.

If the either Sender's email address or password are incorrect, or if gmail passowrd setup written above in the __Dependencies number 4__ the program will terminate with the following message:

    ENTER CSV File Name or Directory: sales.csv
    *****SUCCESS! - CSV upload*****
    *****SUCCESS! - Data Quality Checks*****
    ENTER Reciever's Email: email@gmail.com
    ENTER Sender's Email: email@gmail.com
    Password:

    *****FAIL! - Gmail Login*****

    *****Please Check the Sender's Email and Password or refer to the guide links below*****
    https://support.google.com/mail/?p=BadCredentials
    https://support.google.com/accounts/answer/185833?hl=en

Once the Gmail login is successful, the program will then send the generated report to Receiver's email address and terminate

    ENTER CSV File Name or Directory: sales.csv
    *****SUCCESS! - CSV upload*****
    *****SUCCESS! - Data Quality Checks*****
    ENTER Reciever's Email: email@gmail.com
    ENTER Sender's Email: email@gmail.com
    Password:
    *****SUCCESS! - Gmail Login*****
    *****SUCCESS! - Email Sent***** 

___
## [__Project Demo__](https://www.youtube.com/watch?v=iNPvc-AcAOs)
#### Video Demo:  https://www.youtube.com/watch?v=iNPvc-AcAOs
## __Author__
__Glenn Latayan__

Malvar Batangas, Philippines 4233

[Linkedin](https://www.linkedin.com/in/latayanglenn0920/)

[Github](https://github.com/glenndoughl)