from bs4 import BeautifulSoup
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('citation_edge.csv')

# Remove rows where 'Abstract' column has the value 'N/A'
df = df[~df['target_doi'].isin(['N/A']) & df['target_doi'].notna()]

df.to_csv('citation_edge_screened.csv', index=False)