import os
import logging

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def setup_logging(log_file="scraper.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
