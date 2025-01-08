import pandas as pd
from bertopic import BERTopic
from bs4 import BeautifulSoup
import numpy as np

def load_and_process_data_with_topics(file_path, model_path):
    """
    Load data, clean text, load BERTopic model, and assign topics to documents
    
    Parameters:
    file_path (str): Path to the CSV file
    model_path (str): Path to the saved BERTopic model
    
    Returns:
    pandas.DataFrame: Original dataframe with added topic assignments
    """
    # Load the CSV file with error handling
    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None
    
    # Define the cleaning function
    def clean_html_xml(text):
        if pd.isna(text):
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
    
    # Get clean documents (non-empty only)
    docs = df['cleaned_text'].replace('', np.nan).dropna().tolist()
    
    # Load the model
    try:
        print("Loading BERTopic model...")
        topic_model = BERTopic.load(model_path)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Model file not found!")
        return None
    
    # Get topic assignments for all documents
    print("Assigning topics to documents...")
    topics, _ = topic_model.transform(docs)
    
    # Create a mapping of topic numbers to topic names
    topic_info = topic_model.get_topic_info()
    topic_names = dict(zip(topic_info['Topic'], topic_info['Name']))
    
    # Add topic assignments to the dataframe
    # First, create a mask for non-empty documents
    valid_docs_mask = df['cleaned_text'].replace('', np.nan).notna()
    
    # Initialize topic columns with NaN
    df['topic_number'] = np.nan
    df['topic_name'] = np.nan
    
    # Assign topics only to valid documents
    df.loc[valid_docs_mask, 'topic_number'] = topics
    df.loc[valid_docs_mask, 'topic_name'] = [topic_names.get(t, f"Topic_{t}") for t in topics]
    
    return df

# Usage example:
if __name__ == "__main__":
    # Load data and assign topics
    enriched_df = load_and_process_data_with_topics('6n_cleaned.csv', 'bertopic_model')
    
    # Save the enriched dataframe
    if enriched_df is not None:
        output_path = '6n_cleaned_with_topics.csv'
        enriched_df.to_csv(output_path, index=False)
        print(f"Saved enriched dataset to {output_path}")
        
        # Print a summary of topic distribution
        print("\nTopic Distribution:")
        topic_counts = enriched_df['topic_name'].value_counts()
        print(topic_counts)

enriched_df = load_and_process_data_with_topics('6n_cleaned.csv', 'bertopic_model')
enriched_df.to_csv('6n_cleaned_with_topics.csv', index=False)

