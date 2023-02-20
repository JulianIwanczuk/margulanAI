from config import API_KEY, connection
import json

client = connection()


# Schema configuration
class_obj = {
    "class": "Notion",
    "description": "Information from the notion database",  # description of the class
    "vectorizer": "text2vec-openai",
    "properties": [
        {
            "dataType": ["blob"],
            "description": "The ID seed",
            "name": "seed",
        },
        {
            "dataType": ["text"],
            "description": "The name",
            "name": "name",
        },
        {
            "dataType": ["string"],
            "description": "The answer",
            "name": "answer",
        },        
    ]
}

client.schema.create_class(class_obj)

# Load the data from github 
import requests
url = 'https://github.com/JulianIwanczuk/margulanAI/blob/main/notion-index.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Configure a batch process
with client.batch as batch:
    batch.batch_size=100
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "seed": d["seed"],
            "name": d["name"],
            "answer": d["answer"],
        }

        client.batch.add_data_object(properties, "Notion")