import sqlite3
import csv
import pandas as pd
from time import process_time
from database import DataBase, connect_to_db

"""The functions of this module insert the example data into the bank database."""

db = connect_to_db(DataBase("bank_database.db"))

# ** REFERENCE TABLES **

def insert_EmployeePositions(file: str):
    q = """
    INSERT INTO EmployeePositions(employee_position) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data) # skips header row, reader is iterable
        for row in data:
            db.execute(q,[row[1]])

def insert_CustomerTypes(file: str):
    q = """
    INSERT INTO CustomerTypes(customer_type) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1]])

def insert_AccountTypes(file: str):
    q = """
    INSERT INTO AccountTypes(account_type) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1]])

def insert_AccountStatus(file: str):
    q = """
    INSERT INTO AccountStatus(account_status,reason) VALUES (?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],row[2]])

def insert_LoanTypes(file: str):
    q = """
    INSERT INTO LoanTypes(loan_type) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1]])

def insert_LoanStatus(file: str):
    q = """
    INSERT INTO LoanStatus(loan_status) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1]])

def insert_TransactionTypes(file: str):
    q = """
    INSERT INTO TransactionTypes(transaction_type) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1]])

def insert_AddressTypes(file: str):
    q = """
    INSERT INTO AddressTypes(address_type) VALUES (?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1]])

# ** CORE TABLES **

def insert_Addresses(file: str):
    q = """
    INSERT INTO Addresses(address_type_id,street,postal_code,city,country) VALUES (?,?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],row[2],row[3],row[4],row[5]])

def insert_Branches(file: str):
    q = """
    INSERT INTO Branches(address_id,branch_name,swift_code,phone_number) VALUES (?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],row[2],row[3],row[4]])

def insert_Persons(file: str):
    q = """
    INSERT INTO Persons(address_id,last_name,first_name,date_of_birth,email,phone_number,ssn) VALUES (?,?,?,?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],row[2],row[3],row[4],row[5],row[6],row[7]])

def insert_Employees(file: str):
    q = """
    INSERT INTO Employees(employee_id,position_id,branch_id) VALUES (?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[0],row[1],row[2]])

def insert_Customers(file: str):
    q = """
    INSERT INTO Customers(customer_id,type_id) VALUES (?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[0],row[1]])

# ** FINANCIAL TABLES **

def insert_Accounts(file: str):
    q = """
    INSERT INTO Accounts(type_id,status_id,customer_id,branch_id,account_number,balance,date_opened,date_closed) VALUES (?,?,?,?,?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            if row[8] != "":
                db.execute(q,[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])
            else:
                null = "NULL"
                db.execute(q,[row[1],row[2],row[3],row[4],row[5],row[6],row[7],null])

def insert_Loans(file: str):
    q = """
    INSERT INTO Loans(type_id,status_id,customer_id,amount,interest_rate,term,loan_start_date,loan_end_date) VALUES (?,?,?,?,?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])

def insert_LoanPayments(file: str):
    q = """
    INSERT INTO LoanPayments(loan_id,scheduled_amount,principal,interest,actual_amount,scheduled_date,paid_date) VALUES (?,?,?,?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],row[2],row[3],row[4],row[5],row[6],row[7]])

def insert_Transactions(file: str):
    q = """
    INSERT INTO Transactions(type_id,loan_payment_id,employee_id,from_account_id,to_account_id,amount,transaction_date) VALUES (?,?,?,?,?,?,?)
    """
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            db.execute(q,[row[1],ifnull(row[2]),ifnull(row[3]),row[4],ifnull(row[5]),row[6],row[7]])

def insert_all():
    # Path to files
    path = "./example_data/"

    # Reference tables
    ref = "EmployeePositions.csv CustomerTypes.csv AccountTypes.csv AccountStatus.csv LoanTypes.csv LoanStatus.csv TransactionTypes.csv AddressTypes.csv"
    ref = ref.split()

    insert_EmployeePositions(path+ref[0])
    insert_CustomerTypes(path+ref[1])
    insert_AccountTypes(path+ref[2])
    insert_AccountStatus(path+ref[3])
    insert_LoanTypes(path+ref[4])
    insert_LoanStatus(path+ref[5])
    insert_TransactionTypes(path+ref[6])
    insert_AddressTypes(path+ref[7])

    # Core tables
    core = "Addresses.csv Branches.csv Persons.csv Employees.csv Customers.csv"
    core = core.split()

    insert_Addresses(path+core[0])
    insert_Branches(path+core[1])
    insert_Persons(path+core[2])
    insert_Employees(path+core[3])
    insert_Customers(path+core[4])

    # Financial tables
    fin = "Accounts.csv Loans.csv LoanPayments_fixed.csv Transactions.csv"
    fin = fin.split()

    insert_Accounts(path+fin[0])
    insert_Loans(path+fin[1])
    insert_LoanPayments(path+fin[2])
    insert_Transactions(path+fin[3])

def fix_loanpaymentscsv():
    """Fixes LoanPayments.csv to meet the constraints of CHECK"""

    path = "./example_data/LoanPayments.csv"

    df = pd.read_csv(path)
    fixed_col = (df["principal"] + df["interest"]).round(2)
    df.drop(columns=["scheduled_amount"],inplace=True)
    df.insert(2,"scheduled_amount",fixed_col)
    
    to_path = "./example_data/LoanPayments_fixed.csv"
    df.to_csv(to_path,sep=",",index=False)

def fix_transactionscsv():
    """Fixes Transactions.csv to meet the foreign key constraints"""

    path = "./example_data/Transactions.csv"

    df = pd.read_csv(path)
    df.fillna("NULL",inplace=True)
    
    to_path = "./example_data/Transactions_fixed.csv"
    df.to_csv(to_path,sep=",",index=False)

def ifnull(value):
    if len(value) == 0:
        return "NULL"
    else:
        return value

def test(file):
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            if row[1] == "" or row[4] == "":
                print(f"Row {row[0]} is empty!")

def test2(file):
    q = """
    INSERT INTO LoanPayments(loan_id,scheduled_amount,principal,interest,actual_amount,scheduled_date,paid_date) VALUES (?,?,?,?,?,?,?)
    """
    db.execute(q,[1,5,2,3,4,"2024-12-12","2023-12-12"])

if __name__ == "__main__":
    start_time = process_time()
    insert_all()
    print(f"Time taken: {process_time() - start_time}")

    #fix_loanpaymentscsv()
    #test("./example_data/LoanPayments_fixed.csv")
    #test2("./example_data/LoanPayments_fixed.csv")

    #fix_transactionscsv()