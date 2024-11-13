import pandas as pd

# Read the files
node_df = pd.read_csv('citation_node.csv')
edge_df = pd.read_csv('citation_edge_screened_no_dupes.csv')

# Create initial lookup dictionary from existing nodes
node_lookup = {doi: id for id, doi in zip(node_df['doi'], node_df['id'])}

# Find the next available ID number
next_id = node_df['id'].max() + 1

# Function to get or create ID for a DOI
def get_or_create_id(doi):
    global next_id
    if doi not in node_lookup:
        node_lookup[doi] = next_id
        next_id += 1
    return node_lookup[doi]

# Map existing IDs and create new ones for source and target
edge_df['source'] = edge_df['source'].apply(get_or_create_id)
edge_df['target'] = edge_df['target'].apply(get_or_create_id)

# Save the updated edge file
edge_df.to_csv('citation_edge_mapped.csv', index=False)

# Create new nodes dataframe with all DOIs
all_dois = list(node_lookup.keys())
all_ids = [node_lookup[doi] for doi in all_dois]

new_node_df = pd.DataFrame({
    'id': all_ids,
    'doi': all_dois
})

# Sort by ID to maintain order
new_node_df = new_node_df.sort_values('id').reset_index(drop=True)

# Save the updated node file
new_node_df.to_csv('citation_node_updated.csv', index=False)

# Print some statistics
print(f"Original number of nodes: {len(node_df)}")
print(f"New number of nodes: {len(new_node_df)}")
print(f"Number of new nodes added: {len(new_node_df) - len(node_df)}")