import gensim
from gensim.models import KeyedVectors
import gzip
import shutil
import os
import numpy as np
import pandas as pd

from log_config import get_logger
from config import data_dir

# create logger instance
logger = get_logger()


# Extract the file from .gz format. Returns the path of the extracted file
def extract_file(compressed_file):
    try:
        logger.info('Preparing for extraction')
        
        # build compressed file path
        compressed_file_path = os.path.join(data_dir, 'raw', compressed_file)
        # build extracted file path
        extracted_file = compressed_file[:-3] # to remove .gz extension
        extracted_file_path = os.path.join(data_dir, 'extracted', extracted_file)
        
        # Extract the .gz file
        with gzip.open(compressed_file_path, 'rb') as f_in:
            with open(extracted_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        logger.info('File extraction was successful')
        
        return extracted_file_path
    except FileNotFoundError:
        logger.error('The compressed file was not found.')
        return False
    except Exception as e:
        logger.exception(e)
        return False

# loads the vectors from the binary file and saves them as a csv file.

def load_save_word2vec_vectors(extracted_file_path, limit=1000000):
    try:
        logger.info('Start loading vectors')

        # Load vectros with limit
        wv = KeyedVectors.load_word2vec_format(extracted_file_path, binary=True, limit=limit)

        # build path of vectors file
        vectors_file_path = os.path.join(data_dir, 'processed', 'vectors.csv')

        # Save vectors as csv
        wv.save_word2vec_format(vectors_file_path, binary=False)

        logger.info('Vectors were saved successfully in vectors.csv')

        return vectors_file_path
    except Exception as e:
        logger.exception(e)
        return False



def execute_load_embeddings(compressed_file):
    # Extract the file from .gz format. Returns the path of the extracted file
    extract_file_path = extract_file(compressed_file)
    # Stops the function in case of an error
    if extract_file_path is False:
        logger.error('Failed extracting the compossed file')
        return False

    # loads the vectors from the binary file and saves them as a csv file
    vectors_file_path = load_save_word2vec_vectors(extract_file_path)
    # stops the function in case of an error
    if vectors_file_path is False:
        logger.error('Failed to load vectors into a csv')
        return False

    return vectors_file_path    


if __name__ == '__main__':
    execute_load_embeddings('GoogleNews-vectors-negative300.bin.gz')
