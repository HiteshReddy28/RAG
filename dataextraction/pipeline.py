from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from utils.extract import uscis_extract 
import os


def extract_data(**kwargs):
    print(kwargs)
    # uscis_extract()
    print("Extracting data...")
    return {"data": "sample data"}


def transform_data(**kwargs):
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract_data')
    # Dummy function to simulate data transformation
    print(f"Transforming data: {extracted_data}")
    transformed_data = extracted_data["data"].upper()
    return {"transformed_data": transformed_data}

def load_data(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform_data')
    # Dummy function to simulate data loading
    print(f"Loading data: {transformed_data}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'data_extraction_pipeline',
    default_args=default_args,
    description='A simple data extraction pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
    )

extract_task >> transform_task >> load_task
