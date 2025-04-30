# dags/example_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("example_dag", start_date=datetime(2024, 1, 1), schedule="@daily", catchup=False) as dag:
    t1 = BashOperator(
        task_id="print_hello",
        bash_command="echo 'Hello, Airflow!'"
    )
