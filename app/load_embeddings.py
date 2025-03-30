import gensim
from gensim.models import KeyedVectors
import gzip
import shutil
import os

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

"""
Extracts the compressed file to get the binary one. Then loads the vectors from the binary file and saves them as a csv file.
Requires name of the compressed file as an argument
"""
def load_save_word2vec_vectors(compressed_file, limit=1000000):
    try:
        # executes the funcion to extract the compressed file from .gz format
        input_path = extract_file(compressed_file)
        # exit the function if failes to extract the file
        if input_path is False:
            logger.error('Failed to extract the compressed file')
            return False
        
        logger.info('Start loading vectors')

        # Load vectros with limit
        wv = KeyedVectors.load_word2vec_format(input_path, binary=True, limit=limit)

        # build path of vectors file
        vectors_file_path = os.path.join(data_dir, 'processed', 'vectors.csv')

        # Save vectors as csv
        wv.save_word2vec_format(vectors_file_path)

        logger.info('Vectors were saved successfully in vectors.csv')

        return True
    except Exception as e:
        logger.exception(e)
        return False
    
if __name__ == '__main__':
    load_save_word2vec_vectors('GoogleNews-vectors-negative300.bin.gz')
    