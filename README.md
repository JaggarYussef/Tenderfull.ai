# Tenderfull.ai

## Overview

This project aims to collect the latest tenders published on the BOSA website and match them with a user's natural language query using NLP techniques.

The project includes:

1. Collecting the latest tenders from the specified website.
2. Cleaning, processing, and validating the collected data.
3. Using a Sentence-Transformer model to generate similarity scores.
4. Notifying users based on these scores.

To orchestrate these tasks and ensure continuous runs every 15 minutes, Airflow is used. The environment includes several services such as PgAdmin, Airflow web server and scheduler, PostgreSQL, FastAPI, and Streamlit, all running as Docker services using Docker Compose, paving the way for eventual deployment.

## Project Workflow

### Fetcher Module

This module mimics the way the website requests data from an endpoint, producing a raw JSON object containing the latest 25 tenders.

```jsx
{
	"0": {
		"cpvAdditionalCodes": [
			{
				"code": "72413000-8",
				"descriptions": [
					{
						"language": "NL",
						"text": "Diensten voor het ontwerpen van websites"
					},
					{
						"language": "DE",
						"text": "Website-Gestaltung"
					},
					{
						"language": "EN",
						"text": "World wide web (www) site design services"
					},
					{
						"language": "FR",
						"text": "Services de conception de sites WWW (World Wide Web)"
					}
				]
			}
		],
....
		"dispatchDate": "2024-07-03",
		"dossier": {
			"accreditations": {},
			"descriptions": [
				{
					"language": "NL",
					"text": "Aantrekkelijke en gebruiksvriendelijke website voor het APEx project. VITO zoekt een communicatiepartner (expert web design, UX) voor de opmaak van een nieuwe website voor het ‘APEx - Application Propagation Environment(s)’ project. APEx moet enerzijds resultaten van (afgelopen) aardobservatieprojecten en -toepassingen ter beschikking stellen en anderzijds ook nieuwe projecten ondersteunen door bepaalde diensten (algoritmes, workflow, project website, etc.) aan te bieden die men eenvoudig kan integreren en aanpassen naar specifieke noden binnen het project. APEx is een project dat VITO uitvoert in opdracht van ESA. Deze website moet live zijn tegen 01/10/2024. Meer info over dit project (EN): https://remotesensing.vito.be/news/new-esa-apex-initiative-will-boost-reusability-eo-based-research-outcomes. We zoeken een communicatiepartner die ons kan bijstaan in de: - Opzet, structuur en navigatie van de website - Web design - Front-end development - Copywriting (meer specifieke info in de Technische Bepalingen)."
				}
			],
			"enterpriseCategories": [],
			"legalBasis": "D24",
			"number": "PPP04G-1093/4424/OV-website APEx-VITO 24",
			"procurementProcedureType": "NEG_WO_CALL_24",
			"referenceNumber": "PPP04G-1093/4424/OV-website APEx-VITO 24",
			"titles": [
				{
					"language": "NL",
					"text": "Opmaak van een nieuwe website voor het APEx project"
				}
			]
		},
		"insertionDate": "2024-07-03",
		"lots": [
			{
				"descriptions": [
					{
						"language": "NL",
						"text": "Aantrekkelijke en gebruiksvriendelijke website voor het APEx /.....
					}
				],
				"reservedExecution": [],
				"reservedParticipation": [],
				"titles": [
					{
						"language": "NL",
						"text": "Opmaak van een nieuwe website voor het APEx project"
					}
				]
			}
		],
....
		"procedureId": "455354f1-b03e-489a-8cc7-6fc2ccd7545a",
		"publicationDate": "2024-07-03",
		"publicationLanguages": [
			"NL"
		],
		"publicationReferenceNumbersBDA": [
			"PPP04G-1093/4424/OV-website APEx-VITO 24_002"
		],
		"publicationReferenceNumbersTED": [],
		"publicationType": "ACTIVE",
		"publicationWorkspaceId": "47197bd6-5b65-432f-8832-8179c70cf285",
		"publishedAt": [
			"2024-07-03T00:00:46.632224"
		],
		"referenceNumber": "PPP04G-1093/4424/OV-website APEx-VITO 24_002",
		"sentAt": [
			"2024-07-03T00:00:46.632224"
		],
		"tedPublished": false
	}
}

```

### Preprocessor Module

A crucial component where data cleaning, modeling, and validation occur to ensure no duplicate tenders are sent to the model and eventually to the user. This module extracts the following properties from the raw JSON file:

```json
{
  "id": "readable_id",
  "posting_title": "posting_title",
  "category": "category",
  "publication_date": "publication_date",
  "publication_language": "publication_language",
  "description_paragraph": "description_paragraph",
  "status": "status",
  "workspace_id": "workspace_id"
}
```

### Ingester Module

This transitional step saves the cleaned data and validates incoming tenders to ensure no duplicates are processed.

### Model Module

The core of the system, where the model compares tender information with user queries to generate similarity scores and ultimately notify the user.

### Model Choice

The project uses the `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` model, chosen for its performance across multiple categories. The performance metrics in English, Dutch, and cross-language contexts are detailed below.

### Schema:

### `tenders` Table

| Column Name           | Data Type   | Constraints                           | Default           |
| --------------------- | ----------- | ------------------------------------- | ----------------- |
| id                    | String      | Primary Key                           |                   |
| posting_title         | String      | Not Null                              |                   |
| category              | String      | Not Null                              |                   |
| publication_date      | DateTime    | Not Null                              |                   |
| publication_language  | String (2)  | Not Null                              |                   |
| description_paragraph | Text        | Not Null                              |                   |
| status                | String (20) | Not Null                              |                   |
| workspace_id          | String      | Not Null, Default = str(uuid.uuid4()) | str(uuid.uuid4()) |

### `user_input` Table

| Column Name | Data Type | Constraints          | Default |
| ----------- | --------- | -------------------- | ------- |
| id          | Integer   | Primary Key, Indexed |         |
| query       | Text      | Not Null             |         |
| email       | String    | Not Null             |         |
| score       | Float     | Not Null             |         |

These tables provide a clear representation of the schema for both the `tenders` and `user_input` models, including the data types, constraints, and default values where applicable.

### Model Choice

### English

| Model                                                       | Paragraph (P) | Sentence (S) | Random (R) |
| ----------------------------------------------------------- | ------------- | ------------ | ---------- |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | 0.411         | 1.0          | N/A        |
| sentence-transformers/LaBSE                                 | 0.272         | N/A          | 0.202      |
| sentence-transformers/all-MiniLM-L6-v2                      | 0.477         | 1.0          | 0.41       |
| BAAI/bge-m3                                                 | 0.526         | 1.0          | 0.281      |

### Dutch

| Model                                                       | Paragraph (P) | Sentence (S) | Random (R) |
| ----------------------------------------------------------- | ------------- | ------------ | ---------- |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | 0.628         | 1.0          | 0.06       |
| sentence-transformers/LaBSE                                 | 0.449         | 1.0          | 0.393      |
| sentence-transformers/all-MiniLM-L6-v2                      | 0.430         | 1.0          | 0.352      |
| BAAI/bge-m3                                                 | 0.492         | 1.0          | 0.306      |

### Cross-Language

| Model                                                       | Paragraph (P) | Sentence (S) | Random (R) |
| ----------------------------------------------------------- | ------------- | ------------ | ---------- |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | 0.573         | 0.92         | 0.55       |
| sentence-transformers/LaBSE                                 | 0.285         | 0.827        | 0.188      |
| sentence-transformers/all-MiniLM-L6-v2                      | 0.291         | 0.172        | 0.056      |
| BAAI/bge-m3                                                 | 0.492         | 0.90         | 0.288      |
