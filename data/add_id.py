import pandas as pd

node_df = pd.read_csv('citation2_node.csv')
edge_df = pd.read_csv('citation2_edge.csv')

node_lookup = {label: id for id, label in zip(node_df['id'], node_df['label'])}

edge_df['source'] = edge_df['source'].map(node_lookup)
edge_df['target'] = edge_df['target'].map(node_lookup)

edge_df.to_csv('citation2_edge_mapped.csv', index=False)