from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_to_mongodb
from config.settings import settings
from loguru import logger
from src.utils.logging_config import logger

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract(**kwargs):
    logger.info("Starting Extract Phase")
    raw_data = extract_data(settings.INPUT_FILE, settings.FILE_TYPE)
    kwargs['ti'].xcom_push(key='raw_data', value=raw_data)
    logger.info("Extract Phase completed")

def transform(**kwargs):
    logger.info("Starting Transform Phase")
    ti = kwargs['ti']
    raw_data = ti.xcom_pull(task_ids='extract', key='raw_data')
    transformed_data = transform_data(raw_data)
    aux = transformed_data.head()
    logger.info(f"Sample payment methods: {aux['payment_method'].tolist()}")
    ti.xcom_push(key='transformed_data', value=transformed_data)
    logger.info("Transform Phase completed")

def load(**kwargs):
    logger.info("Starting Load Phase")
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform', key='transformed_data')
    load_result = load_to_mongodb(
        transformed_data,
        settings.MONGO_DB,
        settings.MONGO_COLLECTION
    )
    logger.info("Load Phase completed")
    return load_result

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Complete ETL pipeline with Airflow',
    schedule_interval=timedelta(days=1),  # Runs daily
    catchup=False,
    tags=['etl', 'production'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
        provide_context=True,
    )

    # Set task dependencies
    extract_task >> transform_task >> load_task