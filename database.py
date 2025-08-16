import sqlite3
import os
import os.path
from string import ascii_letters

class DataBase():

    def __init__(self, name: str = "example.db"):
        """Create a new database."""

        self.name = name
        self.check_existance()
        self.__db = sqlite3.connect(name)

    def create_tables(self):
        """Create all the tables of the database."""

        self.__db.executescript("""
                                                   
            -- People: (Persons, Employees, Customers)

            CREATE TABLE Persons
            (
                person_id       INTEGER PRIMARY KEY,
                address         TEXT, -- sep
                last_name       TEXT,
                first_name      TEXT,
                date_of_birth   DATE,
                email           TEXT,
                phone_number    TEXT,
                ssn             TEXT
            );
            CREATE TABLE Employees
            (
                employee_id     INTEGER REFERENCES Persons(person_id),
                position        TEXT, -- sep
                branch_id       INTEGER REFERENCES Branches(branch_id)               
            );
            CREATE TABLE Customers
            (
                customer_id     INTEGER REFERENCES Persons(person_id),
                type            TEXT -- sep                  
            );
                                
            -- Bank elements: (Branches, Accounts)

            CREATE TABLE Branches
            (
                branch_id       INTEGER PRIMARY KEY,
                address         TEXT, -- sep
                accounts_id     INTEGER REFERENCES Accounts(account_id),
                name            TEXT,
                code            TEXT,
                phone_number    TEXT
            );
            CREATE TABLE Accounts
            (
                account_id      INTEGER PRIMARY KEY,
                type            TEXT, -- sep
                status          TEXT, -- sep
                customer_id     INTEGER REFERENCES Customers(customer_id),
                account_number  TEXT,
                balance         REAL,
                date_opened     DATE,
                date_closed     DATE               
            );
                                
            -- Cash flows: (loans, LoanPayments, Transactions)

            CREATE TABLE Loans
            (
                loan_id         INTEGER PRIMARY KEY,
                type            TEXT, -- sep
                status          TEXT, -- sep
                customer_id     INTEGER REFERENCES Customers(customer_id),
                amount          REAL,
                interest_rate   REAL,
                term            INTEGER,
                start_date      DATE,
                end_date        DATE                    
            );
            CREATE TABLE LoanPayments
            (
                loan_payment_id INTEGER PRIMARY KEY,
                loan_id         INTEGER REFERENCES Loans(loan_id),
                scheduled_date  DATE,
                payment_amount  REAL,
                principal       REAL,
                interest        REAL,
                paid_amount     REAL,
                paid_date       DATE
            );
            CREATE TABLE Transactions
            (
                transaction_id  INTEGER PRIMARY KEY,
                type            TEXT, -- sep
                loan_payment_id INTEGER REFERENCES LoanPayments(loan_payment_id),
                account_id      INTEGER REFERENCES Accounts(account_id),
                employee_id     INTEGER REFERENCES Employees(employee_id),
                amount          REAL,
                date            DATE                  
            );
                                """)

    def check_existance(self):
        """Check whether a database exists with the given filename."""

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
    q = Query(db)

    for i, letter in enumerate(ascii_letters):
        q.add_test(int((i+1)*10),letter)

    print(q.query_test())