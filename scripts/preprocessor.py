
import json
import pandas as pd
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tender
import time

import os

PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_HOST = os.getenv("POSTGRES_HOST")
PG_DB = os.getenv("POSTGRES_DB")
PG_PORT = os.getenv("POSTGRES_PORT")

# timestamp = datetime.now().isoformat()
DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'


        
def property_extractor(tender_object, existing_ids):
    publication_language = tender_object['publicationLanguages'][0]
    status = tender_object['publicationType']
    workspace_id = str(tender_object['publicationWorkspaceId'])
    publication_date = tender_object['publishedAt'][0]
    

    readable_id = 'tender_' + workspace_id.split('-')[0]
    if readable_id in existing_ids:
        print('exists')
        return None 


    # Posting Title 
    lots = tender_object['lots'][0]
    titles = lots['titles']
    posting_title = ""
    for child in titles:
        if child['language'] == publication_language:
            posting_title = child['text']


    # Unify all descriptive values
    description_objects = tender_object['cpvAdditionalCodes']
    description_list = []
    for description_object in description_objects:
        for child in description_object['descriptions']:
            if child['language'] == publication_language:
                description_list.append(child['text'])


    dossier = tender_object['dossier']['descriptions']
    for description_object in dossier:
        if description_object['language'] == publication_language:
            description_list.append(description_object['text'])

    description_paragraph = " ".join(description_list)
    description_paragraph = description_paragraph + posting_title


    # single category
    category = ""
    category_object = tender_object["cpvMainCode"]
    for child in category_object['descriptions']:
        if child['language'] == publication_language:
            category = child['text']



    unique_id = uuid.uuid4()
    unique_id_str = str(unique_id)
    
    cleaned_tender = {
        "id": readable_id,
        "posting_title": posting_title,
        "category": category,
        "publication_date": publication_date,
        "publication_language": publication_language,
        "description_paragraph": description_paragraph,
        "status": status,
        "workspace_id": workspace_id
    }
    return cleaned_tender


def get_existing_id():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query all tender IDs
        tenders_id_db = session.query(Tender.id).all()

        # Commit the transaction
        session.commit()
        
        # Print the IDs
        # print(tenders_id_db)
        ids_list = [item[0] for item in tenders_id_db]
        return ids_list

    except Exception as e:
        # Handle exceptions (e.g., database errors)
        print(f"Error: {e}")
        session.rollback()  # Rollback changes on error

    finally:
        session.close()  # Close the session


def generate_clean_data():
    try:
        ids_list = get_existing_id()
        print(ids_list)

        with open("/opt/airflow/data/raw/raw.json") as read_file:
            tender = json.load(read_file)
            tenders = tender['publications']
            
            # Filter out None values
            processed_tenders = list(filter(None, map(lambda t: property_extractor(t, ids_list), tenders)))
            
            if not processed_tenders:
                print("No new tenders to process.")
                return

            tenders_df = pd.DataFrame(processed_tenders)
            tenders_df.to_csv("/opt/airflow/data/processed/processed.csv", mode="a", header=False, index=False)
            print(f"Number of new tenders processed: {len(tenders_df)}")
            print(f"Columns in tenders_df: {tenders_df.columns}")
            print(tenders_df['description_paragraph'])
    except Exception as e:
        print(f"Error in generate_clean_data: {e}")    

generate_clean_data()
 

generate_clean_data()