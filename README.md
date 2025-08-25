# Bank Database

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

A relational database of a retail bank's entities and their relationships built in Python and SQLite. A prepopulated database is also available, which contains AI-generated mock data.

## Schema & Description

The database models a bank's customers, employees and branches and the interactions between them, such as accounts, loans and various types of transactions. The schema also contains several reference tables of normalized information to allow greater detail.

![Entity-Relationship diagram picture.](C:\Users\Niklas\bank-database\ER_diagram.png)

**Core tables:**
- Addresses
- Branches
- Persons
- Employees
- Customers

**Financial tables:**
- Accounts
- Loans
- LoanPayments
- Transactions

**Reference tables:**
- AccountTypes
- AccountStatus
- EmployeePositions
- CustomerTypes
- AddressTypes
- LoanTypes
- LoanStatus
- TransactionTypes
## Requirements & Usage

Depending on the purpose of use, the following options are available:

1. The database schema in sql-format is found in `sql/schema.sql`.
2. The python code for creating a new empty database is in `src/database.py`.
	- This file also comes with the schema built-in.
3. The `bank_database.db` in the repository's root is a prepopulated database with tens of thousands of records.
	- A database tool is required to open .db files and perform queries. 
		- DBeaver is available for free: https://dbeaver.io/
## Example Queries

> [!info]
> The following queries are based on the AI-generated mock data.

Check the number of customers and their average account balances by customer type:
```sql
SELECT CT.customer_type,
       COUNT(C.customer_id) AS customer_count,
       ROUND(AVG(A.balance),2) AS average_balance
FROM CustomerTypes CT JOIN Customers C ON CT.type_id = C.type_id
JOIN Accounts A ON C.customer_id = A.customer_id
WHERE A.date_closed IS NULL
GROUP BY CT.customer_type;
```

| customer_type | customer_count | average_balance |
| ------------- | -------------- | --------------- |
| Business      | 821            | 25604.05        |
| Retail        | 763            | 25384.01        |
| VIP           | 916            | 24404.51        |

Check the contact information of customers whose accounts have been closed due to suspicious activity:
```sql
SELECT DISTINCT C.customer_id,
       P.last_name, P.first_name,
       P.phone_number, P.email,
A.street, A.postal_code, A.city, A.country
FROM Addresses A JOIN Persons P ON A.address_id = P.address_id
JOIN Customers C ON P.person_id = C.customer_id
JOIN Accounts Ac ON C.customer_id = Ac.customer_id
JOIN AccountStatus AcS ON Ac.status_id = AcS.status_id
WHERE AcS.reason = "Suspicious Activity"
ORDER BY C.customer_id;
```

| customer_id          | last_name            | first_name           | phone_number           | email                          | street                         | postal_code          | city                 | country               |
| -------------------- | -------------------- | -------------------- | ---------------------- | ------------------------------ | ------------------------------ | -------------------- | -------------------- | --------------------- |
| 2                    | Key                  | Caleb                | (357)828-0876          | renee89@santos.biz             | 058 Anthony Ramp               | 67893                | New Josetown         | Saint Kitts and Nevis |
| 4                    | Rodriguez            | Jennifer             | 998.259.6287           | amy25@romero.com               | 984 Amanda Cliff Suite 247     | 02737                | Jasonport            | Saint Barthelemy      |
| 8                    | Bishop               | Joan                 | 659-355-2523           | scottrodgers@collier.com       | 90452 Stacey Station Suite 056 | 85982                | North Kevinmouth     | Zimbabwe              |
| 9                    | Woodard              | Paul                 | 001-496-015-7772x76905 | bergerjohn@baldwin-leblanc.org | 255 Kirk Island                | 70720                | Mitchellmouth        | Belize                |
| 10                   | Hogan                | Sharon               | +1-875-935-9997x565    | medinaseth@gmail.com           | 62022 Oconnell Curve Apt. 331  | 54439                | Nelsonmouth          | Brunei Darussalam     |
| <center>...</center> | <center>...</center> | <center>...</center> | <center>...</center>   | <center>...</center>           | <center>...</center>           | <center>...</center> | <center>...</center> | <center>...</center>  |
| 1189                 | Kennedy              | Geoffrey             | 001-771-837-4326x50954 | andrea83@yahoo.com             | 812 Wright Bridge              | 19044                | Julianfurt           | San Marino            |
| 1195                 | Norman               | Allison              | 3256319239             | emily08@harris.info            | 3689 Velasquez Isle Suite 856  | 09046                | Port Michael         | Botswana              |
| 1196                 | Ramos                | David                | 762-049-5829x9304      | eugene75@hotmail.com           | 0585 Garcia Falls Suite 554    | 30699                | Mcintyreside         | Sri Lanka             |
| 1198                 | Diaz                 | Ryan                 | +1-226-159-2672x6220   | robert30@yahoo.com             | 4351 Austin Hill Suite 743     | 14715                | Smithmouth           | Denmark               |
| 1200                 | Turner               | George               | 463.579.9589x419       | robertallen@meyer-cain.com     | 430 Carr Freeway Apt. 133      | 09896                | East Mark            | India                 |

Count the proportion of defaults on loans each branch has experienced:
```sql
SELECT B2.branch_id,
       B2.branch_name,
       COUNT(L2.loan_id) AS total_loans,
       total_defaults,
       ROUND(CAST(total_defaults AS FLOAT) / CAST(COUNT(L2.loan_id) AS FLOAT),4) AS proportion
FROM LoanStatus LS2 JOIN Loans L2 ON LS2.status_id = L2.status_id
JOIN Customers C2 ON L2.customer_id = C2.customer_id
JOIN Accounts A2 ON C2.customer_id = A2.customer_id
JOIN Branches B2 ON A2.branch_id = B2.branch_id
JOIN (
   SELECT B1.branch_id AS B1_id,
          COUNT(L1.loan_id) AS total_defaults
   FROM LoanStatus LS1 JOIN Loans L1 ON LS1.status_id = L1.status_id
   JOIN Customers C1 ON L1.customer_id = C1.customer_id
   JOIN Accounts A1 ON C1.customer_id = A1.customer_id
   JOIN Branches B1 ON A1.branch_id = B1.branch_id
   WHERE LS1.loan_status = "Default"
   GROUP BY B1.branch_id, B1.branch_name
) ON B1_id = B2.branch_id
GROUP BY B2.branch_id, B2.branch_name
ORDER BY B2.branch_id;
```

|branch_id|branch_name|total_loans|total_defaults|proportion|
|---------|-----------|-----------|--------------|----------|
|1|Lake Nicholasmouth Branch|60|21|0.35|
|2|Port Marissaside Branch|66|26|0.3939|
|3|North Carlos Branch|52|18|0.3462|
|4|North Cherylport Branch|50|22|0.44|
|5|Alexandriamouth Branch|50|16|0.32|
|6|Davidsonfurt Branch|55|23|0.4182|
|7|North Jessica Branch|71|27|0.3803|
|8|Coleton Branch|56|19|0.3393|
|9|Davilaland Branch|60|23|0.3833|
|10|West Juliestad Branch|53|20|0.3774|
|11|New Victor Branch|55|21|0.3818|
|12|Daltonbury Branch|54|18|0.3333|
