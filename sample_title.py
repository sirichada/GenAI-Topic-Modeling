import requests
import pandas as pd

# Define the API endpoint and parameters
url = "https://api.crossref.org/works"
params = {
    "query": "ethics of generative ai art",
    "rows": 1000  # Adjust the number of rows as needed
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Extract the relevant data
items = data['message']['items']
titles = [item['title'][0] for item in items if 'title' in item and item['title']]

# Create a DataFrame
df = pd.DataFrame(titles, columns=['Title'])

# Export to CSV
df.to_csv('titlesArt.csv', index=False)

print("Data has been saved to titlesArt.csv")