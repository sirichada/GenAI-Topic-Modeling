import pandas as pd

# Read the node CSV (this contains existing DOIs)
node_csv = pd.read_csv('citation1_node.csv')  # This should have a column 'doi'

# Read the edge CSV (this contains 'source_doi' and 'target_doi')
edge_csv = pd.read_csv('citation1_edge_doi.csv')  # This should have columns 'source_doi' and 'target_doi'

# Extract unique target DOIs from the edge CSV
new_dois = edge_csv['target'].unique()

# Check if the 'doi' column exists in the node CSV and then add missing DOIs
existing_dois = node_csv['doi'].unique()

# Identify DOIs that are in the edge list but not in the node list
dois_to_add = [doi for doi in new_dois if doi not in existing_dois]

# Create a new DataFrame with the new DOIs to add to the node CSV
new_nodes = pd.DataFrame(dois_to_add, columns=['doi'])

# Optionally, add a default label (if your node CSV also has a 'label' column)
new_nodes['label'] = 'New Node'  # You can change the label as needed

# Append the new DOIs to the node CSV
updated_node_csv = pd.concat([node_csv, new_nodes], ignore_index=True)

# Save the updated node CSV to a new file
updated_node_csv.to_csv('updated_nodes.csv', index=False)

# Print the updated node CSV (optional)
print(updated_node_csv)
