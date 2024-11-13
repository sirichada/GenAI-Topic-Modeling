import pandas as pd

node_df = pd.read_csv('citation_node.csv')
edge_df = pd.read_csv('citation_edge_screened.csv')

node_lookup = {doi: id for id, doi in zip(node_df['id'], node_df['doi'])}

edge_df['source'] = edge_df['source'].map(node_lookup)
edge_df['target'] = edge_df['target'].map(node_lookup)

edge_df.to_csv('citation_edge_mapped.csv', index=False)