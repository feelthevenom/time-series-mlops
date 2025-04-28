import os
import yaml
import sys
import numpy as np

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
    
def write_yaml_file(file_path: str, content: dict):
    """
    Write a dictionary into a yaml file.
    Args:
        file_path (str): Path to the yaml file.
        content (dict): Dictionary to write into the yaml file.
    """
    try:
        logger.info(f"Writing yaml file: {file_path}")
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
        logger.info(f"Yaml file content: {content}")
    except Exception as e:
        raise CustomException(e, sys)
    
def write_preprocess_data_file(filepath: str, X_train: np, y_train, ts_train: np, X_test: np, y_test: np, ts_test: np):
    """
    Saves the preprocess of both train and test data into npz format.
    Args: 
        filepath (str): Path of the preprocessed data.
        X_train (np): input train numpy array.
        y_train (np): output label train  numpy array.
        X_test (np): input test numpy array.
        y_test (np): output label test  numpy array.
    """
    directory = os.path.dirname(filepath)

    os.makedirs(directory, exist_ok=True)

    np.savez(filepath,
             X_train=X_train,
             y_train=y_train,
             ts_train=ts_train,
             X_test=X_test,
             y_test=y_test,
             ts_test=ts_test)
    
def read_preprocessed_data(filepath: str):
    """
    Read the saved preprocessed data for training and testing.
    Args:
        filepath (str): saved preprocessed file path.
    """
    data = np.load(filepath, allow_pickle=True)
    return (data['X_train'], data['y_train'], data['ts_train'],
            data['X_test'], data['y_test'], data['ts_test'])

def create_sequences(data: str, index: int, window_size: int):
    """
    Preprocess sequence to train the time series
    Args:
        data (str): pass the data to be preprocesses.
        index (int): total number data to processes.
        window_size (int): number sample to be predicted before.
    """
    X, y, timestamps = [], [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
        timestamps.append(index[i + window_size])
    return np.array(X), np.array(y), np.array(timestamps)