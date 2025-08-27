-- People:  Persons, Employees, Customers,
--          EmployeePositions, CustomerTypes

CREATE TABLE Persons
(
    person_id           INTEGER PRIMARY KEY,
    address_id          INTEGER REFERENCES Addresses(address_id) NOT NULL,
    last_name           TEXT NOT NULL,
    first_name          TEXT NOT NULL,
    date_of_birth       DATE NOT NULL,
    email               TEXT UNIQUE,
    phone_number        TEXT UNIQUE NOT NULL,
    ssn                 TEXT UNIQUE NOT NULL
);
CREATE TABLE Employees
(
    employee_id         INTEGER PRIMARY KEY REFERENCES Persons(person_id) ON DELETE CASCADE,
    position_id         INTEGER REFERENCES EmployeePositions(position_id) NOT NULL,
    branch_id           INTEGER REFERENCES Branches(branch_id) NOT NULL              
);
CREATE TABLE EmployeePositions
(
    position_id         INTEGER PRIMARY KEY,
    employee_position   TEXT UNIQUE NOT NULL                 
);
CREATE TABLE Customers
(
    customer_id         INTEGER PRIMARY KEY REFERENCES Persons(person_id) ON DELETE CASCADE,
    type_id             INTEGER REFERENCES CustomerTypes(type_id) NOT NULL                 
);
CREATE TABLE CustomerTypes
(
    type_id             INTEGER PRIMARY KEY,
    customer_type       TEXT UNIQUE NOT NULL
);
                    
-- Bank elements:   Branches, Accounts,
--                  AccountTypes, AccountStatus,

CREATE TABLE Branches
(
    branch_id           INTEGER PRIMARY KEY,
    address_id          INTEGER REFERENCES Addresses(address_id) NOT NULL,
    branch_name         TEXT UNIQUE NOT NULL,
    swift_code          TEXT UNIQUE NOT NULL,
    phone_number        TEXT UNIQUE NOT NULL,

    CHECK (LENGTH(swift_code) = 8 OR LENGTH(swift_code) = 11) -- 8 for main office, 11 for branches
);
CREATE TABLE Accounts
(
    account_id          INTEGER PRIMARY KEY,
    type_id             INTEGER REFERENCES AccountTypes(type_id) NOT NULL,
    status_id           INTEGER REFERENCES AccountStatus(status_id) NOT NULL,
    customer_id         INTEGER REFERENCES Customers(customer_id) ON DELETE CASCADE NOT NULL,
    branch_id           INTEGER REFERENCES Branches(branch_id) NOT NULL,
    account_number      TEXT UNIQUE NOT NULL,
    balance             REAL NOT NULL,
    date_opened         DATE NOT NULL,
    date_closed         DATE,

    CHECK (date_closed IS NULL OR date_closed >= date_opened)
);
CREATE TABLE AccountTypes
(
    type_id             INTEGER PRIMARY KEY,
    account_type        TEXT UNIQUE NOT NULL
);
CREATE TABLE AccountStatus
(
    status_id           INTEGER PRIMARY KEY,
    account_status      TEXT UNIQUE NOT NULL,
    reason              TEXT -- Reason for status, e.g. closure
);

-- Cash flows:  Loans, LoanPayments, Transactions,
--              LoanTypes, LoanStatus, TransactionTypes

CREATE TABLE Loans
(
    loan_id             INTEGER PRIMARY KEY,
    type_id             INTEGER REFERENCES LoanTypes(type_id) NOT NULL,
    status_id           INTEGER REFERENCES LoanStatus(status_id) NOT NULL,
    customer_id         INTEGER REFERENCES Customers(customer_id) NOT NULL,
    amount              REAL NOT NULL,
    interest_rate       REAL NOT NULL,
    term                INTEGER NOT NULL, -- Loan term in months
    loan_start_date     DATE NOT NULL,
    loan_end_date       DATE NOT NULL, -- When the loan is paid in full

    CHECK (amount >= 0 AND term >= 0 AND loan_end_date > loan_start_date)
);
CREATE TABLE LoanPayments
(
    loan_payment_id     INTEGER PRIMARY KEY,
    loan_id             INTEGER REFERENCES Loans(loan_id) NOT NULL,
    scheduled_amount    REAL NOT NULL, -- Total scheduled payment amount (principal + interest)
    principal           REAL NOT NULL, -- Principal portion of the payment
    interest            REAL NOT NULL, -- Interest portion of the payment
    actual_amount       REAL, -- Actual total amount paid
    scheduled_date      DATE NOT NULL, -- Scheduled payment date
    paid_date           DATE, -- Actual payment date

    CHECK (scheduled_amount > 0)
    -- Constraint (scheduled_amount = principal + interest) does not work due to how computers store floating point numbers
    -- When inserting data into the table, scheduled_amount should be constructed from principal and interest for each entry separately
    -- i.e. INSERT INTO LoanPayments(scheduled_amount) VALUES ((principal + interest))
);
CREATE TABLE Transactions
(
    transaction_id      INTEGER PRIMARY KEY,
    type_id             INTEGER REFERENCES TransactionTypes(type_id) NOT NULL, -- Transaction type
    loan_payment_id     INTEGER REFERENCES LoanPayments(loan_payment_id), -- Used only if the transaction involves a loan
    employee_id         INTEGER REFERENCES Employees(employee_id), -- Used only if the transaction is done manually by an employee
    from_account_id     INTEGER REFERENCES Accounts(account_id) NOT NULL, -- The account from which the transaction is made
    to_account_id       INTEGER REFERENCES Accounts(account_id), -- Used only if the transaction is done to another account
    amount              REAL NOT NULL,
    transaction_date    DATE NOT NULL,

    CHECK (amount > 0)
    -- if type_id is "Loan payment", loan_payment_id must not be null
    -- if type_id is "Transfer", to_account_id must not be null
    -- These require subqueries which are not possible in sqlite CHECK
);
CREATE TABLE LoanTypes
(
    type_id             INTEGER PRIMARY KEY,
    loan_type           TEXT UNIQUE NOT NULL
);
CREATE TABLE LoanStatus
(
    status_id           INTEGER PRIMARY KEY,
    loan_status         TEXT UNIQUE NOT NULL
);
CREATE TABLE TransactionTypes
(
    type_id             INTEGER PRIMARY KEY,
    transaction_type    TEXT UNIQUE NOT NULL
);

-- Others:  Addresses, AddressTypes

CREATE TABLE Addresses
(
    address_id          INTEGER PRIMARY KEY,
    address_type_id     INTEGER REFERENCES AddressTypes(address_type_id) NOT NULL,
    street              TEXT NOT NULL,
    postal_code         TEXT NOT NULL,
    city                TEXT NOT NULL,
    country             TEXT NOT NULL
);
CREATE TABLE AddressTypes
(
    address_type_id INTEGER PRIMARY KEY,
    address_type    TEXT UNIQUE NOT NULL -- Distinguish between people, branches and other possible address types
);