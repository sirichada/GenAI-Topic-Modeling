import pandas as pd
from bertopic import BERTopic
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from itertools import combinations

def load_and_process_data(file_path, model_path):
    """
    Load data, clean text, and load BERTopic model
    
    Parameters:
    file_path (str): Path to the CSV file
    model_path (str): Path to the saved BERTopic model
    
    Returns:
    tuple: (cleaned_docs, topic_model)
    """
    # Load the CSV file with error handling
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None, None
    
    # Define the cleaning function
    def clean_html_xml(text):
        if pd.isna(text):  # Handle NaN values
            return ""
        try:
            soup = BeautifulSoup(str(text), 'html.parser')
            return soup.get_text().strip()
        except Exception as e:
            print(f"Error cleaning text: {e}")
            return ""
    
    # Clean the abstracts
    print("Cleaning text data...")
    df['cleaned_text'] = df['Abstract'].apply(clean_html_xml)
    
    # Remove empty strings and get clean documents
    docs = df['cleaned_text'].replace('', np.nan).dropna().tolist()
    
    # Load the saved model
    try:
        print("Loading BERTopic model...")
        topic_model = BERTopic.load(model_path)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Model file not found. Creating new model...")
        # Initialize new model if saved model doesn't exist
        vectorizer_model = CountVectorizer(stop_words="english")
        topic_model = BERTopic(vectorizer_model=vectorizer_model)
        
    return docs, topic_model

# load_and_process_data('6n_cleaned.csv', 'bertopic_model')

def create_topic_network_csvs():
    # Correctly unpack the return values from load_and_process_data
    docs, topic_model = load_and_process_data('6n_cleaned.csv', 'bertopic_model')

    if topic_model is None:
        print("Error: BERTopic model could not be loaded.")
        return None, None

    # Run topic modeling if not already done
    topics, probs = topic_model.transform(docs)

    # Create node table
    topic_info = topic_model.get_topic_info()

    # Filter out topic -1 (outliers) if it exists
    topic_info = topic_info[topic_info['Topic'] != -1]

    # Create nodes dataframe
    nodes_df = pd.DataFrame({
        'id': topic_info['Topic'],
        'size': topic_info['Count'],
        'label': topic_info['Name']  # Contains representative words
    })

    # Create edge table
    # Initialize dictionary to store co-occurrences
    topic_pairs = {}

    # For each document, look at its topic distribution
    for doc_probs in probs:
        # Get indices of topics with non-zero probability
        present_topics = np.where(doc_probs > 0.05)[0]  # threshold of 0.05

        # Create edges between all pairs of present topics
        for t1, t2 in combinations(present_topics, 2):
            if t1 != -1 and t2 != -1:  # Skip outlier topic
                # Use sorted tuple as key to avoid duplicates
                pair = tuple(sorted([t1, t2]))
                # Add the product of probabilities to the weight
                weight = doc_probs[t1] * doc_probs[t2]
                topic_pairs[pair] = topic_pairs.get(pair, 0) + weight

    # Create edges dataframe
    edges_df = pd.DataFrame([
        {'source': pair[0], 
         'target': pair[1], 
         'weight': weight}
        for pair, weight in topic_pairs.items()
    ])

    # Normalize edge weights to [0,1]
    if not edges_df.empty:
        edges_df['weight'] = edges_df['weight'] / edges_df['weight'].max()

    # Save to CSV
    nodes_df.to_csv('topic_nodes.csv', index=False)
    edges_df.to_csv('topic_edges.csv', index=False)

    return nodes_df, edges_df

# Create the CSV files
nodes_df, edges_df = create_topic_network_csvs()
print("\nNodes table preview:")
print(nodes_df.head())
print("\nEdges table preview:")
print(edges_df.head())