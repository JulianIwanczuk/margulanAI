import weaviate

API_KEY = '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'
cluster = weaviate.Client("https://margulan.weaviate.network/")


# Connects to Weaviate 

def connection(
    client=cluster,
    additional_headers={
        "X-OpenAI-Api-Key": API_KEY
    }):
    return weaviate.Client(
        url=cluster.url,  
        additional_headers=additional_headers
    )

# Deletes the class in your vector database
    
def delete_class(class_name):
    client = connection()
    client.schema.delete_class(class_name)
    schema = client.schema.get()
    print(json.dumps(schema, indent=4))
    query = search(["Example"], 2)
    print(query)

def search(near_text_concepts, limit):
    client = connection()
    nearText = {"concepts": near_text_concepts}

    result = (
        client.query
        .get("Notion", ["seed", "name", "answer"])
        .with_near_text(nearText)
        .with_limit(limit)
        .do()
    )

    return json.dumps(result, indent=4)


# Upload your file and transform it to a vector database

def index_upload():
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

    # Load the data from GitHub 
    url = 'https://github.com/JulianIwanczuk/margulanAI/blob/main/notion-index.json?raw=true'
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

            batch.add_data_object(properties, "Notion")

    print("Index upload complete!")

    
    
