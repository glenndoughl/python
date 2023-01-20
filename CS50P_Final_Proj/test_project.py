from project import read_csv, check_int_cols, check_float_cols, check_string_cols, email_validation, email_report

from arguments import int_fields, flt_fields, str_fields, dict_lists

receiver = "glenndoughl@gmail.com"#input("Receiver Email: ")
sender = "glennlatayan.cs50@gmail.com" #input("Sender Email: ") 
password =  "t k q b z j h x g y n g f t m n " #getpass.getpass()

def test_read_csv():

    assert read_csv("samplefoodsales.csv") == True

    try:
        assert read_csv("notexisting.csv") == True
    except SystemExit:
        print("File does not exists")
    try:
        assert read_csv("samplefoodsales.txt") == True
    except SystemExit:
        print("File wrong format")

def test_check_int_cols():
    assert check_int_cols(int_fields) == True

    dummy_list = []
    try:
        assert check_int_cols(dummy_list) == True
    except KeyError:
        print("Columns does not exists")
    try:
        assert check_int_cols("dummy_string") == True
    except KeyError:
        print("Not a Column")    

def test_check_float_cols():
    assert check_float_cols(flt_fields) == True

    try:
        assert check_float_cols("dummy_string") == True
    except KeyError:
        print("Not a float")
    try:
        assert check_float_cols(123) == True
    except TypeError:
        print("Not a float")  

def test_check_string_cols():\

    assert check_string_cols(str_fields, dict_lists) == True

    dummy_dict = {}
    dummy_list = []

    try:
        assert check_string_cols(dummy_list, dict_lists) == True
    except KeyError:
        print("Not a list")
    try:
        assert check_string_cols(str_fields, dummy_dict) == True
    except KeyError:
        print("Not a Dictionary")

def test_email_validation():
    assert email_validation("dummyemail@gmail.com") == "dummyemail@gmail.com"
    try:
        assert email_validation("dummyemail.com") == "dummyemail.com"
    except SystemExit:
        print("Not a valid Email")
    try:
        assert email_validation("dummy@email@com") == "dummy@email@com"
    except SystemExit:
        print("Not a valid Email") 

def test_email_report():
    assert email_report(receiver, sender, password) == True
    try:
        assert email_report(receiver, sender, "password") == True
    except:
        print("Incorrect Password")