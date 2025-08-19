# Functions for adding data into the database.

import sqlite3
from database import DataBase

# ** ADD NORMALIZED INFORMATION **

# Add to EmployeePositions
def add_EmployeePositions(db: DataBase, employee_positions: list = ["Banker",
                                                                     "Analyst",
                                                                     "Manager",
                                                                     "Teller"]):
    """Employee positions"""

    database = connect_to_db(db)

    query = f"""
    INSERT INTO EmployeePositions(employee_position) VALUES (?)
    """

    for item in employee_positions:
        database.execute(query,[item])

# Add to CustomerTypes
def add_CustomerTypes(db: DataBase, customer_types: list = ["Individual",
                                                             "Business"]):
    """Customer types"""

    database = connect_to_db(db)

    query = f"""
    INSERT INTO CustomerTypes(customer_type) VALUES (?)
    """

    for item in customer_types:
        database.execute(query,[item])

# Add to AccountTypes
def add_AccountTypes(db: DataBase, account_types: list = ["Checking",
                                                           "Savings",
                                                           "Credit"]):
    """Account types"""

    database = connect_to_db(db)

    query = f"""
    INSERT INTO AccountTypes(account_type) VALUES (?)
    """

    for item in account_types:
        database.execute(query,[item])

# Add to AccountStatus
def add_AccountStatus(db: DataBase, account_status: list = ["Active",
                                                             "Suspended",
                                                             "Closed"]):
    """Account status"""

    database = connect_to_db(db)

    query = f"""
    INSERT INTO AccountStatus(account_status) VALUES (?)
    """

    for item in account_status:
        database.execute(query,[item])

# Add to LoanTypes
def add_LoanTypes(db: DataBase, loan_types: list = ["Checking",
                                                     "Savings",
                                                     "Credit"]):
    """Loan types"""

    database = connect_to_db(db)

    query = f"""
    INSERT INTO LoanTypes(loan_type) VALUES (?)
    """

    for item in loan_types:
        database.execute(query,[item])

# Add to LoanStatus
def add_loan_status(db: DataBase, loan_status: list = ["Active",
                                                       "Suspended",
                                                       "Closed"]):
    """Loan status"""

    database = connect_to_db(db)

    query = f"""
    INSERT INTO LoanStatus(loan_status) VALUES (?)
    """

    for item in loan_status:
        database.execute(query,[item])

# Add to TransactionTypes
def add_transaction_types(db, transaction_types: list = ["Deposit",
                                                         "Withdrawal",
                                                         "Transfer"]):
    """Transaction types"""

    query = f"""
    INSERT INTO LoanTypes(loan_type) VALUES (?)
    """

    database = connect_to_db(db)

    for item in transaction_types:
        database.execute(query,[item])

def connect_to_db(db: DataBase) -> sqlite3.Connection:
    """Connects to the given SQLite database."""

    database = sqlite3.connect(db.name)

    return database