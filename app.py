import weaviate
import json

client = weaviate.Client(
    url = "https://margulan.weaviate.network/v1",  # Replace with your endpoint
    additional_headers = {
        "X-OpenAI-Api-Key": "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"  # Replace with your API key
    }
)

# Schema for the index
class_obj = {
    "class": "Notion",
    "vectorizer": "text2vec-openai"
}

client.schema.create_class(class_obj)

# Import the JSON file
import requests
url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Configure a batch process
with client.batch as batch:
    batch.batch_size=100
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing id: {i+1}")

        properties = {
            "id": d["ID"],
            "name": d["Name"],
            "answer": d["Answer"],
        }

        client.batch.add_data_object(properties, "Notion")