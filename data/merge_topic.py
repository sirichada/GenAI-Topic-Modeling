import pandas as pd

# Read the first CSV (containing 'id' and 'label')
first_csv = pd.read_csv('citation_node_updated.csv')

# Read the second CSV (containing 'id')
second_csv = pd.read_csv('exported_data.csv')

# Merge the dataframes based on the 'id' column
merged_csv = pd.merge(first_csv, second_csv, on='label', how='left')

# Save the merged result to a new CSV file
merged_csv.to_csv('merged_result2.csv', index=False)

