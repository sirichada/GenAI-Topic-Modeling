import requests
import pandas as pd
import time
from urllib.parse import quote
import json

def get_references_from_doi(doi, email):
    """
    Fetch references for a given DOI using Crossref API
    """
    # Handle invalid DOIs
    if pd.isna(doi):
        print("Skipping invalid DOI: Empty value")
        return []
        
    # Encode DOI for URL
    encoded_doi = quote(doi.strip())
    
    # Crossref API endpoint
    url = f"https://api.crossref.org/works/{encoded_doi}"
    
    # Headers with email (good practice for Crossref API)
    headers = {
        'User-Agent': f'PythonScript/1.0 (mailto:{email})'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract references if they exist
        references = data.get('message', {}).get('reference', [])
        
        # Extract DOIs from references
        ref_dois = []
        for ref in references:
            ref_doi = ref.get('DOI')
            if ref_doi:
                ref_dois.append(ref_doi.lower())  # normalize DOIs to lowercase
        
        # If no references found, return N/A
        if not ref_dois:
            return ['N/A']
                
        return ref_dois
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching references for DOI {doi}: {str(e)}")
        return ['N/A']
    
    except json.JSONDecodeError:
        print(f"Error parsing JSON response for DOI {doi}")
        return ['N/A']

def read_dois_from_csv(input_file):
    """
    Read DOIs from a CSV file with 'DOI' column
    """
    try:
        # Read CSV file
        df = pd.read_csv(input_file)
        
        # Check if 'DOI' column exists
        if 'DOI' not in df.columns:
            raise ValueError("CSV file must contain a column named 'DOI'")
        
        # Get DOIs and remove any leading/trailing whitespace
        dois = df['DOI'].str.strip().tolist()
        
        return dois
        
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []

def create_citation_network(input_file, email, output_file='citation_edge.csv'):
    """
    Create a citation network from DOIs in a CSV file
    """
    # Read DOIs from input file
    input_dois = read_dois_from_csv(input_file)
    
    if not input_dois:
        print("No DOIs found in input file")
        return None
    
    print(f"Found {len(input_dois)} DOIs in input file")
    
    # Initialize empty lists for source and target DOIs
    source_dois = []
    target_dois = []
    
    # Process each input DOI
    total_dois = len(input_dois)
    for idx, doi in enumerate(input_dois, 1):
        print(f"Processing DOI {idx}/{total_dois}: {doi}")
        
        # Get references for current DOI
        references = get_references_from_doi(doi, email)
        
        # Add edges to network (or N/A if no references)
        if references == ['N/A']:
            source_dois.append(doi)
            target_dois.append('N/A')
        else:
            for ref_doi in references:
                source_dois.append(doi)
                target_dois.append(ref_doi)
        
        # Rate limiting - be nice to Crossref API
        time.sleep(1)
    
    # Create DataFrame
    network_df = pd.DataFrame({
        'source_doi': source_dois,
        'target_doi': target_dois
    })
    
    # Save to CSV
    network_df.to_csv(output_file, index=False)
    print(f"Citation network saved to {output_file}")
    
    return network_df

# Example usage
if __name__ == "__main__":
    # Input CSV file containing DOIs
    input_file = "6n_screened.csv"
    
    # Your email address for Crossref API
    email = "swattan@cmkl.ac.th"
    
    # Create citation network
    network_df = create_citation_network(input_file, email)
    
    if network_df is not None:
        # Print some basic statistics
        print(f"\nNetwork Statistics:")
        print(f"Number of edges: {len(network_df)}")
        print(f"Unique source DOIs: {len(network_df['source_doi'].unique())}")
        print(f"Number of DOIs with no citations: {len(network_df[network_df['target_doi'] == 'N/A'])}")