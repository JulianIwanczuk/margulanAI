import json

# Path to the JSON file
file_path = 'notion-index.json'

# Properties to extract
properties = ['id', '!Name', '!Answer']

# Load the JSON file
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract the specified properties for each object
results = []
for obj in data:
    result = {}
    for prop in properties:
        if prop == 'id':
            if 'id' in obj:
                result[prop] = obj['id']
        elif prop == '!Name':
            if 'properties' in obj and '!Name' in obj['properties']:
                name = obj['properties']['!Name']['title'][0]['plain_text']
                result[prop] = name
        elif prop == '!Answer':
            if 'properties' in obj and '!Answer' in obj['properties']:
                answer = obj['properties']['!Answer']['rich_text'][0]['plain_text']
                result[prop] = answer
    results.append(result)

# Save the results to a new JSON file
output_path = 'result.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

# Print a success message
print(f"Extracted the properties {', '.join(properties)} from the file {file_path}.")
print(f"The results have been saved to {output_path}.")
