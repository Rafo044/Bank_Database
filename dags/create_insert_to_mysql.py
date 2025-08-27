from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
from src.insert_functions import insert_Accounts
from src.insert_functions import insert_AccountTypes
from src.

def run_mysql_script(file_path, conn_id='mysql_conn'):
    hook = MySqlHook(mysql_conn_id=conn_id)
    with open(file_path, 'r') as f:
        sql = f.read()
    hook.run(sql)

with DAG(
    dag_id='bank_data_sql_scripts',
    start_date=datetime(2025, 8, 27),
    schedule=None ,
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    create_table = PythonOperator(
        task_id='create_table',
        python_callable=run_mysql_script,
        op_kwargs={'file_path': 'scripts/create_table.sql'}
    )

    insert_value = PythonOperator(
        task_id='insert_value',
        python_callable=run_mysql_script,
        op_kwargs={'file_path': 'scripts/insert_table.sql'}
    )

    start >> create_table >> insert_table >> end
