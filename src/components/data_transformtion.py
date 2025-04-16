import sys
import os
import pandas as pd

from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from src.entity.config_entity import DataTransformationConfig

from src.utils.helper import create_sequences, write_preprocess_data_file

logger = logging.getLogger(__name__)

class DataTransformation:
    def __init__(self, datavalidation_artifact: DataValidationArtifact,
                 datatranformation_config: DataTransformationConfig):
        
        self.datatranformation_config = datatranformation_config
        self.datavalidation_artifact = datavalidation_artifact

    def read_dataframe(self, file_path: str) -> pd.DataFrame:
        """
        Read the csv of train and test and convert to data Frame.
        Args:
            file_path (str): File path of csv file
        """
        try:
            # Read the csv data
            df = pd.read_csv(file_path)
            # Covnert into valid timestamp
            # df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
            #Convert the Data timestamp data into index for the data Frame.
            df.set_index('Date', inplace=True)

            return df

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_data_into_npz(self, train_file_path:str, test_file_path: str, window_size: int, preprocessed_file_path: str):
        """
        Read the csv file of train and test to preprocess the data to train time series data.
        Args:
            train_file_path (str): train csv file path
            test_file_path (str): test csv file path
        """
        try:
            logger.info("Reading the train csv data")
            train_df = self.read_dataframe(train_file_path)

            logger.info("Reading the test csv data")
            test_df = self.read_dataframe(test_file_path)

            # Creating sequence to train the model and test
            logger.info("Trying to create sequence for the data")
            train_X, train_y, train_ts = create_sequences(train_df['Sales'].values, train_df.index, window_size)
            test_X, test_y, test_ts = create_sequences(test_df['Sales'].values, test_df.index, window_size)

            X_train, X_test = train_X, test_X
            y_train, y_test = train_y, test_y
            ts_train, ts_test = train_ts, test_ts


            write_preprocess_data_file(preprocessed_file_path, 
                       X_train, y_train, ts_train, 
                       X_test, y_test, ts_test)
            logger.info(f"Preprocessing the train and test data is success and saved in path = {preprocessed_file_path}")
            
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transforamtion(self):
        try:
            logger.info(self.datavalidation_artifact.is_data_validated)
            if self.datavalidation_artifact.is_data_validated:

                self.preprocess_data_into_npz(
                    train_file_path= self.datavalidation_artifact.train_file_path,
                    test_file_path= self.datavalidation_artifact.test_file_path,
                    window_size= self.datatranformation_config.window_size,
                    preprocessed_file_path= self.datatranformation_config.preprocessed_file_path
                )
                return DataTransformationArtifact(
                    preprocessed_data_file = self.datatranformation_config.preprocessed_file_path
                )
            else:
                logger.error("Data is not validated please check data before pre processing the data.")
                exit(1)
    
        except Exception as e:
            raise CustomException(e, sys)