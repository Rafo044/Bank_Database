import csv
from airflow.providers.mysql.hooks.mysql import MySqlHook
from helper_functions import ifnull

# ==========================
# Helper function: generic insert
# ==========================
def _insert_csv(file: str, sql: str, mysql_conn_id='mysql_default', transform=None):
    hook = MySqlHook(mysql_conn_id=mysql_conn_id)
    with open(file) as csv_file:
        data = csv.reader(csv_file)
        next(data)
        for row in data:
            params = transform(row) if transform else row
            # convert ? placeholder to %s for MySQL
            sql_mysql = sql.replace('?', '%s')
            hook.run(sql_mysql, parameters=tuple(params))

# ==========================
# Reference tables
# ==========================
def insert_EmployeePositions(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO EmployeePositions(employee_position) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

def insert_CustomerTypes(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO CustomerTypes(customer_type) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

def insert_AccountTypes(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO AccountTypes(account_type) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

def insert_AccountStatus(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO AccountStatus(account_status,reason) VALUES (?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1], ifnull(row[2])])

def insert_LoanTypes(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO LoanTypes(loan_type) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

def insert_LoanStatus(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO LoanStatus(loan_status) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

def insert_TransactionTypes(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO TransactionTypes(transaction_type) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

def insert_AddressTypes(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO AddressTypes(address_type) VALUES (?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [row[1]])

# ==========================
# Core tables
# ==========================
def insert_Addresses(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Addresses(address_type_id,street,postal_code,city,country) VALUES (?,?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), row[2], row[3], row[4], row[5]])

def insert_Branches(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Branches(address_id,branch_name,swift_code,phone_number) VALUES (?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), row[2], row[3], row[4]])

def insert_Persons(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Persons(address_id,last_name,first_name,date_of_birth,email,phone_number,ssn) VALUES (?,?,?,?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), row[2], row[3], row[4], ifnull(row[5]), row[6], row[7]])

def insert_Employees(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Employees(employee_id,position_id,branch_id) VALUES (?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[0]), int(row[1]), int(row[2])])

def insert_Customers(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Customers(customer_id,type_id) VALUES (?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[0]), int(row[1])])

# ==========================
# Financial tables
# ==========================
def insert_Accounts(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Accounts(type_id,status_id,customer_id,branch_id,account_number,balance,date_opened,date_closed) VALUES (?,?,?,?,?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), int(row[2]), int(row[3]), int(row[4]), row[5], round(float(row[6]),2), row[7], ifnull(row[8])])

def insert_Loans(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Loans(type_id,status_id,customer_id,amount,interest_rate,term,loan_start_date,loan_end_date) VALUES (?,?,?,?,?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), int(row[2]), int(row[3]), round(float(row[4]),2), round(float(row[5]),2), int(row[6]), row[7], row[8]])

def insert_LoanPayments(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO LoanPayments(loan_id,scheduled_amount,principal,interest,actual_amount,scheduled_date,paid_date) VALUES (?,?,?,?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), round(float(row[3])+float(row[4]),2), round(float(row[3]),2), round(float(row[4]),2), ifnull(row[5]) if row[5] == "NULL" else round(float(row[5]),2), row[6], ifnull(row[7])])

def insert_Transactions(file, mysql_conn_id='mysql_default'):
    q = "INSERT INTO Transactions(type_id,loan_payment_id,employee_id,from_account_id,to_account_id,amount,transaction_date) VALUES (?,?,?,?,?,?,?)"
    _insert_csv(file, q, mysql_conn_id, lambda row: [int(row[1]), ifnull(row[2]) if row[2] == "NULL" else int(row[2]), ifnull(row[3]) if row[3] == "NULL" else int(row[3]), int(row[4]), ifnull(row[5]) if row[5] == "NULL" else int(row[5]), round(float(row[6]),2), row[7]])

# ==========================
# Wrapper
# ==========================
def insert_all(path="./example_data/", mysql_conn_id='mysql_default'):
    # Reference tables
    ref = "EmployeePositions.csv CustomerTypes.csv AccountTypes.csv AccountStatus.csv LoanTypes.csv LoanStatus.csv TransactionTypes.csv AddressTypes.csv"
    ref = ref.split()
    insert_EmployeePositions(path+ref[0], mysql_conn_id)
    insert_CustomerTypes(path+ref[1], mysql_conn_id)
    insert_AccountTypes(path+ref[2], mysql_conn_id)
    insert_AccountStatus(path+ref[3], mysql_conn_id)
    insert_LoanTypes(path+ref[4], mysql_conn_id)
    insert_LoanStatus(path+ref[5], mysql_conn_id)
    insert_TransactionTypes(path+ref[6], mysql_conn_id)
    insert_AddressTypes(path+ref[7], mysql_conn_id)

    # Core tables
    core = "Addresses.csv Branches.csv Persons.csv Employees.csv Customers.csv"
    core = core.split()
    insert_Addresses(path+core[0], mysql_conn_id)
    insert_Branches(path+core[1], mysql_conn_id)
    insert_Persons(path+core[2], mysql_conn_id)
    insert_Employees(path+core[3], mysql_conn_id)
    insert_Customers(path+core[4], mysql_conn_id)

    # Financial tables
    fin = "Accounts.csv Loans.csv LoanPayments.csv Transactions.csv"
    fin = fin.split()
    insert_Accounts(path+fin[0], mysql_conn_id)
    insert_Loans(path+fin[1], mysql_conn_id)
    insert_LoanPayments(path+fin[2], mysql_conn_id)
    insert_Transactions(path+fin[3], mysql_conn_id)
