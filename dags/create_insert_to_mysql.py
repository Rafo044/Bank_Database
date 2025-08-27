from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime
import os

from src.loaders import (
    insert_EmployeePositions,
    insert_CustomerTypes,
    insert_AccountTypes,
    insert_AccountStatus,
    insert_LoanTypes,
    insert_LoanStatus,
    insert_TransactionTypes,
    insert_AddressTypes,
    insert_Addresses,
    insert_Branches,
    insert_Persons,
    insert_Employees,
    insert_Customers,
    insert_Accounts,
    insert_Loans,
    insert_LoanPayments,
    insert_Transactions
)

# Path to CSV folder
CSV_PATH = "/opt/airflow/example_data/"
MYSQL_CONN_ID = "mysql_conn"

with DAG(
    dag_id="load_bank_data",
    start_date=datetime(2025, 8, 27),
    schedule_interval=None,
    catchup=False,
) as dag:

    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    # ---------- Reference tables ----------
    t_employee_positions = PythonOperator(
        task_id="employee_positions",
        python_callable=insert_EmployeePositions,
        op_kwargs={"file": os.path.join(CSV_PATH, "EmployeePositions.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_customer_types = PythonOperator(
        task_id="customer_types",
        python_callable=insert_CustomerTypes,
        op_kwargs={"file": os.path.join(CSV_PATH, "CustomerTypes.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_account_types = PythonOperator(
        task_id="account_types",
        python_callable=insert_AccountTypes,
        op_kwargs={"file": os.path.join(CSV_PATH, "AccountTypes.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_account_status = PythonOperator(
        task_id="account_status",
        python_callable=insert_AccountStatus,
        op_kwargs={"file": os.path.join(CSV_PATH, "AccountStatus.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_loan_types = PythonOperator(
        task_id="loan_types",
        python_callable=insert_LoanTypes,
        op_kwargs={"file": os.path.join(CSV_PATH, "LoanTypes.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_loan_status = PythonOperator(
        task_id="loan_status",
        python_callable=insert_LoanStatus,
        op_kwargs={"file": os.path.join(CSV_PATH, "LoanStatus.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_transaction_types = PythonOperator(
        task_id="transaction_types",
        python_callable=insert_TransactionTypes,
        op_kwargs={"file": os.path.join(CSV_PATH, "TransactionTypes.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_address_types = PythonOperator(
        task_id="address_types",
        python_callable=insert_AddressTypes,
        op_kwargs={"file": os.path.join(CSV_PATH, "AddressTypes.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    # Serial reference table execution
    ref_tasks = [
        t_employee_positions, t_customer_types, t_account_types,
        t_account_status, t_loan_types, t_loan_status,
        t_transaction_types, t_address_types
    ]
    start >> ref_tasks

    # ---------- Core tables ----------
    t_addresses = PythonOperator(
        task_id="addresses",
        python_callable=insert_Addresses,
        op_kwargs={"file": os.path.join(CSV_PATH, "Addresses.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_branches = PythonOperator(
        task_id="branches",
        python_callable=insert_Branches,
        op_kwargs={"file": os.path.join(CSV_PATH, "Branches.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_persons = PythonOperator(
        task_id="persons",
        python_callable=insert_Persons,
        op_kwargs={"file": os.path.join(CSV_PATH, "Persons.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_employees = PythonOperator(
        task_id="employees",
        python_callable=insert_Employees,
        op_kwargs={"file": os.path.join(CSV_PATH, "Employees.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_customers = PythonOperator(
        task_id="customers",
        python_callable=insert_Customers,
        op_kwargs={"file": os.path.join(CSV_PATH, "Customers.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    # Connect reference -> core
    for ref_task in ref_tasks:
        ref_task >> [t_addresses, t_branches, t_persons, t_employees, t_customers]

    # ---------- Financial tables ----------
    t_accounts = PythonOperator(
        task_id="accounts",
        python_callable=insert_Accounts,
        op_kwargs={"file": os.path.join(CSV_PATH, "Accounts.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_loans = PythonOperator(
        task_id="loans",
        python_callable=insert_Loans,
        op_kwargs={"file": os.path.join(CSV_PATH, "Loans.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_loan_payments = PythonOperator(
        task_id="loan_payments",
        python_callable=insert_LoanPayments,
        op_kwargs={"file": os.path.join(CSV_PATH, "LoanPayments.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    t_transactions = PythonOperator(
        task_id="transactions",
        python_callable=insert_Transactions,
        op_kwargs={"file": os.path.join(CSV_PATH, "Transactions.csv"), "mysql_conn_id": MYSQL_CONN_ID},
    )

    # Connect core -> financial
    core_tasks = [t_addresses, t_branches, t_persons, t_employees, t_customers]
    for core_task in core_tasks:
        core_task >> [t_accounts, t_loans, t_loan_payments, t_transactions]

    # End
    [t_accounts, t_loans, t_loan_payments, t_transactions] >> end
