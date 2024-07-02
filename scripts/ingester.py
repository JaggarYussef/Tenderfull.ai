import pandas as pd
from sqlalchemy import create_engine
from .models import Base

def ingest_data(db_url):
    engine = create_engine(db_url)
    trasnformed_data = pd.read_csv("/opt/airflow/data/processed/processed.csv")


    try:
        trasnformed_data.to_sql('tenders', con=engine, if_exists='append', index=False)
    except Exception as e:
        print(f'Error ingesting data  due to {e}')