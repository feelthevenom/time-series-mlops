import sys
import os
from datetime import datetime

from src.exception.exception import CustomException
from src.logging.logger import logging

from src.constant import config

logger = logging.getLogger(__name__)

class TrainingPipelineConfig:
    def __init__(self, time_stamp = datetime.now()):
        time_stamp = time_stamp.strftime("%Y-%m-%d-%H-%M-%S")
        self.pipeline_name = f"Training_Pipeline_{time_stamp}"
        self.artifact_name = config.ARTIFACT_DIRR_NAME
        self.artifact_dir = os.path.join(self.artifact_name, time_stamp)
        self.timestamp: str=time_stamp

class DataingetionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Data Ingestion Configuration for ingesting the data from the source and saving it to the specified directory.

        """
        try:
            # Dataset Directry
            self.dataset_dir: str = os.path.join(config.DATA_DIRR, config.DATA_FILE_NAME)
            
            # Data Ingested Directry
            self.ingested_data_dirr_path: str = os.path.join(training_pipeline_config.artifact_dir,config.INGETION_DIRR_NAME)
            
            # Feature Directory
            self.feature_store_file_path: str = os.path.join(self.ingested_data_dirr_path, config.FEATURE_FILE_NAME)

            # Train Directory
            self.train_file_path: str = os.path.join(self.ingested_data_dirr_path, config.TRAINING_FILE_NAME)

            # Test Directory
            self.test_file_path: str = os.path.join(self.ingested_data_dirr_path, config.TESTING_FILE_NAME)

            
        except Exception as e:
            raise CustomException(e, sys)
        
class DatavalidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Data Validation configuation for validating the data
        
        """
        try:
            # Data Validation Directory to save the validated results
            self.validation_dirr: str = os.path.join(training_pipeline_config.artifact_dir, config.VALIDATION_DIRR_NAME)

            # Drift Report Directory to save the drift report
            self.drift_report_dirr_path: str = os.path.join(self.validation_dirr, config.DRIFT_REPORT_DIRR_PATH)

            # schema file path to validate the columns and data types
            self.schema_file_path: str = os.path.join(config.DATA_SCHEMA_DIRR_NAME, config.SCHEMA_FILE_NAME)

        except Exception as e:
            raise CustomException(e, sys)
        
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Data Transformation config for training the model.
        """
        try:
            # Preprocessed file path to save and load for training
            self.preprocessed_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.PREPROCESSED_FILE_DIRR ,config.PREPROCESS_FILE_NAME)
            self.window_size: str = config.WINDOW_SIZE

        except Exception as e:
            raise CustomException(e, sys)