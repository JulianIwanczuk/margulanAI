import weaviate
import json

client = weaviate.Client(
    url = "https://margulan.weaviate.network/",  # Replace with your endpoint
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
    # Batch import all Notion objects
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "id": d["id"],
            "name": d["name"],
            "answer": d["Answer"],
        }

        client.batch.add_data_object(properties, "question")  