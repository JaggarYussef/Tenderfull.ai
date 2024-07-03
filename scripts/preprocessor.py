import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Tender


def property_extractor(tender_object, existing_ids):
    try:
        publication_language = tender_object['publicationLanguages'][0]
        status = tender_object['publicationType']
        workspace_id = str(tender_object['publicationWorkspaceId'])
        publication_date = tender_object['publishedAt'][0]
        
        readable_id = 'tender_' + workspace_id.split('-')[0]
        if readable_id in existing_ids:
            print(f'Tender {readable_id} already exists.')
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
    except Exception as e:
        print(f"Error processing tender: {e}")
        return None


def get_existing_id(database_uri):
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        tenders_id_db = session.query(Tender.id).all()
        session.commit()
        ids_list = [item[0] for item in tenders_id_db]
        return ids_list
    except Exception as e:
        print(f"Error retrieving data: {e}")
        session.rollback() 
    finally:
        session.close()


def generate_clean_data(database_uri):
    try:
        ids_list = get_existing_id(database_uri)
        print(f"Existing IDs: {ids_list}")

        with open("/opt/airflow/data/raw/raw.json") as read_file:
            tender = json.load(read_file)
            tenders = tender['publications']
            processed_tenders = list(filter(None, map(lambda t: property_extractor(t, ids_list), tenders)))
            
            if not processed_tenders:
                print("No new tenders to process.")
                # Define the headers you expect in the DataFrame
                headers = [ "id","posting_title","category","publication_date","publication_language","description_paragraph","status","workspace_id"]  
                empty_df = pd.DataFrame(columns=headers)
                empty_df.to_csv("/opt/airflow/data/processed/processed.csv", index=False)
                return

            tenders_df = pd.DataFrame(processed_tenders)
            tenders_df.to_csv("/opt/airflow/data/processed/processed.csv", index=False)
            print(f"Number of new tenders processed: {len(tenders_df)}")
            print(f"Columns in tenders_df: {tenders_df.columns}")
            print(tenders_df['description_paragraph'])
    except Exception as e:
        print(f"Error in generate_clean_data: {e}")    

