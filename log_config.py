import logging

"""
To create a logger that can log messages to both the console and an optional log file. The logger is used accros the application
"""


def get_logger(log_file_path='log_file.log'):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # Set the logger level to INFO

    # Remove existing handlers to prevent duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Display INFO and ERROR only
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Create file handler if needed
    if log_file_path:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)  # Log INFO and ERROR to file
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)

    return logger