import os
import yaml
import sys

from src.logging.logger import logging
from src.exception.exception import CustomException

logger = logging.getLogger(__name__)

def read_yaml_file(file_path: str)-> dict:
    """
    Read yaml file and return the content as a dictionary.
    Args:
        file_path (str): Path to the yaml file.
    """
    try:
        logger.info(f"Reading yaml file: {file_path}")
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
        logger.info(f"Yaml file content: {content}")
        
        return content
    except Exception as e:
        raise CustomException(e, sys)
    
