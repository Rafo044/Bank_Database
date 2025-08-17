import sqlite3
import os
import os.path
from string import ascii_letters

class DataBase():

    def __init__(self, name: str = "example.db"):
        """Creates a new empty database."""

        self.name = name
        self.check_existance()
        self.__db = sqlite3.connect(name)
        self.__db.isolation_level = None # commit required without this

    def create_tables(self):
        """Creates all the tables of the database."""

        self.__db.executescript("""
                                                   
        -- People:  Persons, Employees, Customers,
        --          EmployeePositions, CustomerTypes

        CREATE TABLE Persons
        (
            person_id           INTEGER PRIMARY KEY,
            address_id          INTEGER REFERENCES Addresses(address_id),
            last_name           TEXT,
            first_name          TEXT,
            date_of_birth       DATE,
            email               TEXT,
            phone_number        TEXT,
            ssn                 TEXT
        );
        CREATE TABLE Employees
        (
            employee_id         INTEGER REFERENCES Persons(person_id),
            position_id         INTEGER REFERENCES EmployeePositions(position_id),
            branch_id           INTEGER REFERENCES Branches(branch_id)               
        );
        CREATE TABLE EmployeePositions
        (
            position_id         INTEGER PRIMARY KEY,
            employee_position   TEXT                 
        );
        CREATE TABLE Customers
        (
            customer_id         INTEGER REFERENCES Persons(person_id),
            type_id             INTEGER REFERENCES CustomerTypes(type_id)                  
        );
        CREATE TABLE CustomerTypes
        (
            type_id             INTEGER PRIMARY KEY,
            customer_type       TEXT                  
        );
                            
        -- Bank elements:   Branches, Accounts,
        --                  AccountTypes, AccountStatus,

        CREATE TABLE Branches
        (
            branch_id           INTEGER PRIMARY KEY,
            address_id          INTEGER REFERENCES Addresses(address_id),
            name                TEXT,
            code                TEXT,
            phone_number        TEXT
        );
        CREATE TABLE Accounts
        (
            account_id          INTEGER PRIMARY KEY,
            type_id             INTEGER REFERENCES AccountTypes(type_id),
            status_id           INTEGER REFERENCES AccountStatus(status_id),
            customer_id         INTEGER REFERENCES Customers(customer_id),
            branch_id           INTEGER REFERENCES Branches(branch_id),
            account_number      TEXT,
            balance             REAL,
            date_opened         DATE,
            date_closed         DATE               
        );
        CREATE TABLE AccountTypes
        (
            type_id             INTEGER PRIMARY KEY,
            account_type        TEXT                  
        );
        CREATE TABLE AccountStatus
        (
            status_id           INTEGER PRIMARY KEY,
            account_status      TEXT                  
        );
                            
        -- Cash flows:  Loans, LoanPayments, Transactions,
        --              LoanTypes, LoanStatus, TransactionTypes

        CREATE TABLE Loans
        (
            loan_id             INTEGER PRIMARY KEY,
            type_id             INTEGER REFERENCES LoanTypes(type_id),
            status_id           INTEGER REFERENCES LoanStatus(status_id),
            customer_id         INTEGER REFERENCES Customers(customer_id),
            amount              REAL,
            interest_rate       REAL,
            term                INTEGER,
            start_date          DATE,
            end_date            DATE                    
        );
        CREATE TABLE LoanPayments
        (
            loan_payment_id     INTEGER PRIMARY KEY,
            loan_id             INTEGER REFERENCES Loans(loan_id),
            payment_amount      REAL,
            principal           REAL,
            interest            REAL,
            paid_amount         REAL,
            scheduled_date      DATE,
            paid_date           DATE
        );
        CREATE TABLE Transactions
        (
            transaction_id      INTEGER PRIMARY KEY,
            type_id             INTEGER REFERENCES TransactionTypes(type_id),
            loan_payment_id     INTEGER REFERENCES LoanPayments(loan_payment_id),
            employee_id         INTEGER REFERENCES Employees(employee_id),
            from_account        INTEGER REFERENCES Accounts(account_id),
            to_account          INTEGER REFERENCES Accounts(account_id),
            amount              REAL,
            date                DATE                  
        );
        CREATE TABLE LoanTypes
        (
            type_id             INTEGER PRIMARY KEY,
            loan_type           TEXT                 
        );
        CREATE TABLE LoanStatus
        (
            status_id           INTEGER PRIMARY KEY,
            loan_status         TEXT                 
        );
        CREATE TABLE TransactionTypes
        (
            type_id             INTEGER PRIMARY KEY,
            transaction_type    TEXT                      
        );
                            
        -- Others:  Addresses (used for both people and branches)
                            
        CREATE TABLE Addresses
        (
            address_id          INTEGER PRIMARY KEY,
            street              TEXT,
            postal_code         TEXT,
            city                TEXT,
            country             TEXT                  
        );
                                """)

    def add_employee_positions(self, employee_positions: list = ["Banker",
                                                                 "Analyst",
                                                                 "Manager",
                                                                 "Teller"]):
        """Employee positions"""

        query = f"""
        INSERT INTO EmployeePositions(employee_position) VALUES (?)
        """

        for item in employee_positions:
            self.__db.execute(query,[item])

    def add_customer_types(self, customer_types: list = ["Individual",
                                                         "Business"]):
        """Customer types"""

        query = f"""
        INSERT INTO CustomerTypes(customer_type) VALUES (?)
        """

        for item in customer_types:
            self.__db.execute(query,[item])

    def add_account_types(self, account_types: list = ["Checking",
                                                       "Savings",
                                                       "Credit"]):
        """Account types"""

        query = f"""
        INSERT INTO AccountTypes(account_type) VALUES (?)
        """

        for item in account_types:
            self.__db.execute(query,[item])

    def add_account_status(self, account_status: list = ["Active",
                                                         "Suspended",
                                                         "Closed"]):
        """Account status"""

        query = f"""
        INSERT INTO AccountStatus(account_status) VALUES (?)
        """

        for item in account_status:
            self.__db.execute(query,[item])

    def add_loan_types(self, loan_types: list = ["Checking",
                                                 "Savings",
                                                 "Credit"]):
        """Loan types"""

        query = f"""
        INSERT INTO LoanTypes(loan_type) VALUES (?)
        """

        for item in loan_types:
            self.__db.execute(query,[item])

    def add_loan_status(self, loan_status: list = ["Active",
                                                   "Suspended",
                                                   "Closed"]):
        """Loan status"""

        query = f"""
        INSERT INTO LoanStatus(loan_status) VALUES (?)
        """

        for item in loan_status:
            self.__db.execute(query,[item])

    def add_transaction_types(self, transaction_types: list = ["Deposit",
                                                               "Withdrawal",
                                                               "Transfer"]):
        """Transaction types"""

        query = f"""
        INSERT INTO LoanTypes(loan_type) VALUES (?)
        """

        for item in transaction_types:
            self.__db.execute(query,[item])

    def __qmarks(self, l: list):
        """Returns a string of question marks based on list length."""

        return (len(l) * "?,")[:-1] # remove "," from the end

    def check_existance(self):
        """Checks whether a database exists with the given filename."""

        if os.path.exists(self.name):
            os.remove(self.name)

class Query():

    def __init__(self, db: DataBase):
        """Run queries on a database."""

        self.__db = sqlite3.connect(db.name)

    def add_test(self,number: int, string: str):
        """Add testing."""

        query = """
        INSERT INTO Example(number, string) VALUES (?,?)
        """
        id = self.__db.execute(query,[number,string])
        return id

    def query_test(self):
        """Query testing."""

        query = """
        SELECT * FROM Example
        """
        results = self.__db.execute(query).fetchall()
        return results

if __name__ == "__main__":
    
    db = DataBase()
    db.create_tables()

    db.add_employee_positions()
    db.add_customer_types()
    db.add_account_types()
    db.add_account_status()
    db.add_loan_types()
    db.add_loan_status()
    db.add_transaction_types()

    q = sqlite3.connect(db.name)
    query1 = """SELECT * FROM EmployeePositions"""

    values = q.execute(query1).fetchall()

    print(values)