import requests

url = "https://api.crossref.org/works"
params = {
    "order": "asc",
    "sort": "relevance",
    "filter": "type:journal-article",
    "select": "DOI,title,abstract",
    "query.bibliographic": "generative ai ethics",
    "rows": 5  # Limit the number of results returned
}

response = requests.get(url, params=params)
data = response.json()

# Process the returned data
for item in data.get('message', {}).get('items', []):
    print(f"DOI: {item.get('DOI')}")
    print(f"Title: {item.get('title')}")
    print(f"Abstract: {item.get('abstract')}")
    print()
