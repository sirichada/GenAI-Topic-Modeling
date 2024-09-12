import requests
import csv

# Define the API URL
url = "https://api.crossref.org/works"
params = {
    'rows': 1000,  # Request 1000 samples per page
    'mailto': 'sirichada.w@gmail.com',
    'select': 'DOI,title,abstract',
    'query': 'ethics generative AI'
}

# Define the number of results needed
total_results_needed = 3000
results_per_page = params['rows']
total_pages = total_results_needed // results_per_page
remainder = total_results_needed % results_per_page

# Define the CSV file path
csv_file_path = 'crossref_data.csv'

# Write data to CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['DOI', 'Title', 'Abstract'])

    for page in range(total_pages + 1):
        # Update the offset parameter for pagination
        params['offset'] = page * results_per_page
        
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the relevant information
        works = data.get('message', {}).get('items', [])
        
        # Write each row of data
        for work in works:
            doi = work.get('DOI', 'N/A')
            title = work.get('title', ['N/A'])[0]
            abstract = work.get('abstract', 'N/A')
            writer.writerow([doi, title, abstract])
        
        # Break the loop if we have collected the required number of results
        if page == total_pages and remainder:
            break

print(f'Data saved to {csv_file_path}')
