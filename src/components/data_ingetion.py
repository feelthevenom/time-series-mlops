import sys
import os
import pandas as pd

from src.exception.exception import CustomException
from src.logging.logger import logging
from src.entity.config_entity import DataingetionConfig
from src.constant import config

from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self, data_ingestion_config: DataingetionConfig):
        self.data_ingestion_config = data_ingestion_config
        
    def read_source_data(self):
        try:
            self.dataset_dir = self.data_ingestion_config.dataset_dir
            logger.info(f"Reading dataset from {self.dataset_dir}.")
            df = pd.read_csv(self.dataset_dir)
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
            df.set_index('Date', inplace=True)

            logger.info(f"Dataset shape: {df.shape}.")
            logger.info(f"Dataset columns: {df.columns}.")
            logger.info(f"Dataset read successfully.")

            os.makedirs(self.data_ingestion_config.ingested_data_dirr_path, exist_ok=True)

            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=True)
            logger.info(f"Feature store file saved at {self.data_ingestion_config.feature_store_file_path}.")
            return df
        
        except Exception as e:
            raise CustomException(e, sys)

    def split_data_into_train_test(self, df: pd.DataFrame):
        try:
            logger.info(f"Splitting data into train and test sets.")

            train, test = train_test_split(df, test_size=0.2, shuffle=False)
            logger.info(f"Train shape: {train.shape}.")
            logger.info(f"Test shape: {test.shape}.")
            logger.info(f"Data split successfully.")
            
            os.makedirs(self.data_ingestion_config.ingested_data_dirr_path, exist_ok=True)
            
            train.to_csv(self.data_ingestion_config.train_file_path, index=True)
            test.to_csv(self.data_ingestion_config.test_file_path, index=True)
            
        
        except Exception as e:
            raise CustomException(e, sys)