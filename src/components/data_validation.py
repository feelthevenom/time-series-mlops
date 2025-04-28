import sys
import os

import pandas as pd

from src.exception.exception import CustomException
from src.logging.logger import logging

logger = logging.getLogger(__name__)


from src.entity.artifact_entity import  DataValidationArtifact
from src.entity.config_entity import DataValidationConfig


from src.utils.helper import read_yaml_file, write_yaml_file

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig):
        
        self.data_validation_config = data_validation_config


    def is_columns_exist(self, schema_file_path: str, file_path: str)->bool:
        """
        Read both schema yaml file and feature store file csv data to validate the number of columns are same in both.
        Args:
            schema_file_path: (str) - define the schema file path
            file_path: (str) - pass the feature store file path 

        """
        try:
            logger.info("Entering column validation")
            schema = read_yaml_file(schema_file_path)
            logger.info("Reading the feature store dataFrame")
            df = pd.read_csv(file_path)
            # Schema are presented here with datatype
            columns = schema['columns']
            logger.info(f"columns in schemas are {columns} and length are {len(columns)}")

            columns_schema_status = True
            for schema in columns:
                for expected_col, expected_dtype in schema.items():
                    if expected_col not in df.columns:
                        columns_schema_status = False
                        logger.error(f"Column miss match in {file_path}")
                        break
                    if df[expected_col].dtype != expected_dtype:
                        columns_schema_status = False
                        logger.error(f"Column data type is miss matched in {file_path}")
                        break

            logger.info(f"Status of the schema columns are {columns_schema_status}")

            return columns_schema_status

        except Exception as e:
            raise CustomException(e, sys)
        
    def is_columns_same_train_test(self, train_file_path: str, test_file_path: str)->bool:
        """
        Read both train dataset and test dataset, compare both columns are same.
        Args:
            train_file_path (str): pass the training path from data ingestion class.
            test_file_path (str): pass the testing path from data ingestion class.
        """
        try:
            logger.info("Validating train and test ")
            logger.info("Reading the train and test dataFrame")

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            status = True

            # Check the Columns is train datafram are same
            if self.is_columns_exist(schema_file_path = self.data_validation_config.schema_file_path, file_path = train_file_path):
                logger.info("Both train file and schema columns are same")
            # Check the Columns is train datafram are same
            elif self.is_columns_exist(schema_file_path = self.data_validation_config.schema_file_path, file_path = train_file_path):
                logger.info("Both test file and shema columns are same ")
            # Check both train and test contains same number of columns 
            elif sorted(list(train_df.columns)) == sorted(list(test_df.columns)):
                logger.info("Both train and test contains same columns")
            else:
                logger.error("Missing or mismatch column names found in train or test")
                status =  False
                
            return status
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self):
        try:
            # Validate feature store column.
            self.is_columns_exist(schema_file_path= self.data_validation_config.schema_file_path, file_path = self.data_validation_config.feature_store_file_path)
            # Validate the train and test column and data type.
            validate_status = self.is_columns_same_train_test(train_file_path = self.data_validation_config.train_file_path, test_file_path = self.data_validation_config.test_file_path)

            logger.info(f"Validation status = {validate_status}")
            directory = os.path.dirname(self.data_validation_config.data_report_file_path)

            os.makedirs(directory, exist_ok=True)
            
            # Save the validation report
            write_yaml_file(file_path=self.data_validation_config.data_report_file_path, content=validate_status)

            return DataValidationArtifact(
                train_file_path = self.data_validation_config.train_file_path,
                test_file_path= self.data_validation_config.test_file_path,
                is_data_validated = validate_status
            )
        except Exception as e:
            raise CustomException(e, sys)