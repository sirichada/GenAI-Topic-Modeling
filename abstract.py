import requests
import pandas as pd

# Define the API endpoint and parameters
url = "https://api.crossref.org/works"
params = {
    "filter": "type:journal-article",
    "query.bibliographic": (
        "Generative AI OR artificial intelligence OR GenAI "
        "AND "
        "Ethics OR concerns OR impact OR effect "
        "AND "
        "Art OR Artist OR creator"
    ),
    "sort": "relevance",
    "rows": 1000
}


# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    print(data)  # Check the response content

    # Extract the relevant data if the response contains 'message' and 'items'
    if 'message' in data and 'items' in data['message']:
        items = data['message']['items']
        records = [
            {
                'DOI': item['DOI'] if 'DOI' in item else 'N/A',
                'Title': item['title'][0] if 'title' in item and item['title'] else 'N/A',
                'Abstract': item['abstract'] if 'abstract' in item else 'N/A'
            }
            for item in items
        ]

        # Create a DataFrame
        df = pd.DataFrame(records)

        # Export to CSV
        df.to_csv('6.csv', index=False)

        print("Data has been saved to 6.csv")
    else:
        print("Error: 'message' or 'items' not found in the response")
else:
    print(f"Error: Failed to retrieve data. Status code: {response.status_code}")
    print(response.text)  # Print the error message or response content
