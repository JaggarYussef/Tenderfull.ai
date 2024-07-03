from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from scripts.fetcher import data_fetcher
from scripts.preprocessor import generate_clean_data
from sqlalchemy import create_engine
from scripts.models import Base
from scripts.ingester import ingest_data as data_ingestion_funcion
import os

PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_HOST = os.getenv("POSTGRES_HOST")
PG_DB = os.getenv("POSTGRES_DB")
PG_PORT = os.getenv("POSTGRES_PORT")

timestamp = datetime.now().isoformat()
DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

tender_dag = DAG(
    dag_id= 'tender_dag',
    start_date= datetime(2024, 7, 1),
    schedule_interval='*/15 * * * *',
    catchup=False
)

with tender_dag:
        
        start_pipeline =  BashOperator(
                task_id= 'start_pipeline',
                bash_command='echo "Starting pipeline..."'
        )

        fetch_data = PythonOperator(
                task_id= 'fetch_data',
                python_callable= data_fetcher
        )

        process_data = PythonOperator(
                task_id= 'clean_data',
                python_callable= generate_clean_data,
                op_args=[DATABASE_URI]
        )

        data_ingestor_task = PythonOperator(
                task_id='data_ingestion',
                python_callable=data_ingestion_funcion,
                op_args=[DATABASE_URI]
        )



start_pipeline >>  fetch_data >> process_data 