from bs4 import BeautifulSoup
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('6n.csv')

# Remove rows where 'Abstract' column has the value 'N/A'
df = df[~df['Abstract'].isin(['N/A']) & df['Abstract'].notna()]

df.to_csv('6n_screened.csv', index=False)