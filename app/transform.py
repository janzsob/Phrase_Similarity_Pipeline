import numpy as np
import pandas as pd
import os

from log_config import get_logger
from config import data_dir


# create logger instance
logger = get_logger()


# Loads word vectors from a CSV file into a dictionary
def load_vectors_from_csv_into_dict(vectors_file_path):
    try:
        logger.info('Loading vectros into a dictionary')
        
        word_vectors = {}

        with open(vectors_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(" ")  # Split on space
                word = parts[0]  # First part is the word
                try:
                    vector = np.array(parts[1:], dtype=np.float32)  # Convert rest to float
                    word_vectors[word] = vector
                except ValueError as e:
                    print(f"Skipping line due to error: {e}")  # Handle format errors
        
        logger.info('Vectors were successfully loaded into a dictionary')
        
        return word_vectors
    except FileNotFoundError:
        logger.error('Path of Vectors.csv was not found')
        return False
    except Exception as e:
        logger.exception(e)
        return False
    
# retrieves the embedding for a given word. If the word is not present in the dictionary, it returns a zero vector
def get_word_embedding(word, word_vectors):
    return word_vectors.get(word, np.zeros_like(list(word_vectors.values())[0]))

# Assign Word2Vec embeddings to each word in the phrase.
def process_phrase(phrase, word_vectors):
    words = phrase.split()  # Split the phrase into individual words
    embeddings = []
    
    for word in words:
        embedding = get_word_embedding(word, word_vectors)
        embeddings.append(embedding)

    return embeddings


def read_phrases_csv():
    try:
        # build the path of phrases.csv
        file_path = os.path.join(data_dir, 'processed', 'phrases.csv')

        # read the file
        df = pd.read_csv(file_path,  encoding='ISO-8859-1')
        
        return df
    except Exception as e:
        logger.exception(e)
        return False


def execture_transform(vectors_file_path):
    try:
        # Loads word vectors from a CSV file into a dictionary
        word_vectors = load_vectors_from_csv_into_dict(vectors_file_path)
        # stops the function on case of an error
        if word_vectors is False:
            logger.error('Failed to load vectors into a dictionary')
            return False
        
        # Reads phrases.csv
        df = read_phrases_csv()
        # in case of an error
        if df is False:
            logger.error('Failed to read phrases.csv')
            return False
        
        phrase_embeddings = {}
        
        for phrase in df['Phrases']:
            # Assigning embeddings to phrases
            embeddings = process_phrase(phrase, word_vectors)
            phrase_embeddings[phrase] = embeddings

        logger.info("All phrases were processed successfully.")

        return phrase_embeddings

    except Exception as e:
        logger.exception(e)
        return False

if __name__ == '__main__':
    vectors_file_path = os.path.join(data_dir, 'processed', 'vectors.csv')
    phrase_embeddings = execture_transform(vectors_file_path)
    print(phrase_embeddings)