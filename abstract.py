import requests
import pandas as pd

# Define the API endpoint and parameters
url = "https://api.crossref.org/works"
params = {
    "query.bibliographic": "ethics of generative ai",
    "rows": 1000  # Adjust the number of rows as needed
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Extract the relevant data
items = data['message']['items']
records = [
    {
        'Title': item['title'][0] if 'title' in item and item['title'] else 'N/A',
        'Abstract': item['abstract'] if 'abstract' in item else 'N/A'
    }
    for item in items
]

# Create a DataFrame
df = pd.DataFrame(records)

# Export to CSV
df.to_csv('abstracts.csv', index=False)

print("Data has been saved to abstracts.csv")
