
import json
import pandas as pd

def property_extractor(tender_object):
    publication_language = tender_object['publicationLanguages'][0]
    status = tender_object['publicationType']
    workspace_id = tender_object['publicationWorkspaceId']
    publication_date = tender_object['publicationDate']

    # Get description of  the samme language
    description_objects = tender_object['cpvAdditionalCodes']
    description_list = []
    for description_object in description_objects:
        for child in description_object['descriptions']:
            if child['language'] == publication_language:
                description_list.append(child['text'])

    # Find single category
    category = ""
    category_object = tender_object["cpvMainCode"]
    for child in category_object['descriptions']:
        if child['language'] == publication_language:
            category = child['text']

    # Get Description Paragraph
    description_paragraph = ""
    dossier = tender_object['dossier']['descriptions']
    for description_object in dossier:
        if description_object['language'] == publication_language:
            description_paragraph = description_object['text']

    # Get Posting Title 
    lots = tender_object['lots'][0]        
    titles = lots['titles']
    posting_title = ""
    for child in titles:
        if child['language'] == publication_language:
            posting_title = child['text']

    cleaned_tender = {
        "posting_title": posting_title,
        "category": category,
        "publication_date": publication_date,
        "publication_language": publication_language,
        "description_paragraph": description_paragraph,
        "description_list": description_list,
        "status": status,
        "workspace_id": workspace_id
    }
    return cleaned_tender

with open("/opt/airflow/data/raw/raw.json") as read_file:
    tender = json.load(read_file)
    tenders = tender['publications']
    tenders_df = pd.DataFrame(map(property_extractor, tenders))
    tenders_df.to_csv("/opt/airflow/data/processed/processed.csv", index=False)
    print(tenders_df)
