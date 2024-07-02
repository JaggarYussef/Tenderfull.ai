import pandas as pd 
from sentence_transformers import SentenceTransformer

model  = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
tenders = pd.read_csv("/opt/airflow/data/processed/processed.csv")

sentence = ['De minigraafmachine wordt ingezet op de gemeentelijke begraafplaats en zal worden gebruikt voor graaf- en hijswerkzaamheden. De aanbieder moet, voordat hij zijn offerte indient, een demonstratie van het aangeboden voertuig geven. De datum van deze demonstratie wordt afgesproken met de toezichthouder, Stefanie Houquet, die werkt bij het team Technische Diensten, unit Groen.', 'De minigraafmachine wordt ingezet op de gemeentelijke begraafplaats en zal worden gebruikt voor graaf- en hijswerkzaamheden. De aanbieder moet, voordat hij zijn offerte indient, een demonstratie van het aangeboden voertuig geven. De datum van deze demonstratie wordt afgesproken met de toezichthouder, Stefanie Houquet, die werkt bij het team Technische Diensten, unit Groen.']
compare_sentence = ['De minigraver wordt ingezet op de gemeentelijke begraafplaats en zal gebruikt worden voor graafwerken en hijswerken.  De inschrijver dient, voorafgaand het indienen van zijn offerte, een demo te geven over het aangeboden voertuig.  De datum van die demo wordt afgesproken met de toezichter, Stefanie Houquet, medewerker team Technische Diensten, unit Groen '
                    , "Le présent marché public de fournitures pour le Service d’Incendie et d’Aide Médicale Urgente (SIAMU) de la Région de Bruxelles-Capitale porte sur l'achat de 9 systèmes de caméras optiques/thermiques pour auto échelles avec licences utilisateurs et service après-vente afférents.  Le marché public comporte 3 postes :  Poste 1 : Achat de 9 systèmes de caméras optiques/thermiques pour auto-échelles ; Poste 2 : Acquisition des licences pour l'utilisation des 9 systèmes de caméras ; Poste 3 : Prestation d'un service après-vente (après la période de garantie).,"]

embedding1= model.encode(sentence)
embedding2= model.encode(compare_sentence)

similarities = model.similarity(embedding1, embedding2)
print(similarities)