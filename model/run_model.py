import pandas as pd 
from sentence_transformers import SentenceTransformer

def  start_model():

    model  = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    tenders = pd.read_csv("/opt/airflow/data/processed/processed.csv").head(5)
    new_tenders = tenders



    user_input = {
        'id': [1, 2, 3],
        'query': [
            'De minigraver wordt ingezet op de gemeentelijke begraafplaats en zal gebruikt worden voor graafwerken en hijswerken. De inschrijver dient, voorafgaand het indienen van zijn offerte, een demo te geven over het aangeboden voertuig. De datum van die demo wordt afgesproken met de toezichter, Stefanie Houquet, medewerker team Technische Diensten, unit Groen',
            "Le présent marché public de fournitures pour le Service d'Incendie et d'Aide Médicale Urgente (SIAMU) de la Région de Bruxelles-Capitale porte sur l'achat de 9 systèmes de caméras optiques/thermiques pour auto échelles avec licences utilisateurs et service après-vente afférents. Le marché public comporte 3 postes : Poste 1 : Achat de 9 systèmes de caméras optiques/thermiques pour auto-échelles ; Poste 2 : Acquisition des licences pour l'utilisation des 9 systèmes de caméras ; Poste 3 : Prestation d'un service après-vente (après la période de garantie).",
            "Diagnostische benodigdheden Aankoop diagnostische schermenAankoop diagnostische schermen"
        ],
        'email': ['user1@example.com', 'user2@example.com', 'user3@example.com'],
        'score': [0.3000, 0.1, 0.2]
    }

    input_df = pd.DataFrame(user_input)



    new_tenders['description_paragraph']  = new_tenders['category'].astype('str') + '. ' + new_tenders['description_paragraph'].astype('str')
    print()

    tender_info=  new_tenders['description_paragraph'].values
    compare_sentence = input_df['query'].values

    embedding1= model.encode(tender_info)
    embedding2= model.encode(compare_sentence)

    scores = model.similarity(embedding1, embedding2)




    # Initialize the output DataFrame with correct column names
    output_df = pd.DataFrame(columns=["user_email", "tender_link", "score"])

    for i, tender in enumerate(scores):
        tender_id = tenders.iloc[i].id
        tender_link = tenders.iloc[i].workspace_id
        for j in range(len(tender)):
            similarity_score = tender[j]
            user_query_id = input_df.iloc[j].id
            user_email = input_df.iloc[j].email
            user_score = input_df.iloc[j].score
            if similarity_score >= user_score:
                url = f"https://www.publicprocurement.be/publication-workspaces/{tender_link}/general"
                new_row = {'user_email': user_email, "tender_link": url, "score": similarity_score}
                print(new_row)
                output_df = output_df.append(new_row, ignore_index=True)

    # Save the DataFrame to CSV after all rows have been added
    output_df.to_csv('/opt/airflow/data/transformed/contact.csv', index=False)

