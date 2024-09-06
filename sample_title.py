import requests
import pandas as pd

# Define the API endpoint and initial parameters
url = "https://api.crossref.org/works"
params = {
    "query": "ethics of generative ai",
    "rows": 1000,
    "offset": 0
}

all_titles = []

while True:
    # Make the API request
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract the relevant data
    items = data['message']['items']
    titles = [item['title'][0] for item in items if 'title' in item and item['title']]
    
    # Break the loop if no more items are returned
    if not items:
        break
    
    # Append the titles to the list
    all_titles.extend(titles)
    
    # Update the offset for the next request
    params['offset'] += params['rows']

# Create a DataFrame
df = pd.DataFrame(all_titles, columns=['Title'])

# Export to CSV
df.to_csv('titles.csv', index=False)

print("Data has been saved to titles.csv")
