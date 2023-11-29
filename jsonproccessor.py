import json

def replace_escaped_quote(text):
    # Replace every instance of \" with "
    return text.replace(r'\"', '"')

# Load the JSON file
with open('libraryofheaven.json', 'r') as file:
    data = json.load(file)

# Process each chapter
processed_data = {chapter: replace_escaped_quote(text) for chapter, text in data.items()}

# Write the changes back to the JSON file
with open('libraryofheaven.json', 'w') as file:
    json.dump(processed_data, file, indent=4)
