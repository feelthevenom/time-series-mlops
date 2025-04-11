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
        try:
            logger.info(f"Data Ingestion Configuration is setting up.")

            # Dataset Directry
            self.dataset_dir = os.path.join(config.DATA_DIRR, config.DATA_FILE_NAME)
            
            # Data Ingested Directry
            self.ingested_data_dirr_path = os.path.join(training_pipeline_config.artifact_dir,config.INGETION_DIRR_NAME)
            
            # Feature Directory
            self.feature_store_file_path = os.path.join(self.ingested_data_dirr_path, config.FEATURE_FILE_NAME)

            # Train Directory
            self.train_file_path = os.path.join(self.ingested_data_dirr_path, config.TRAINING_FILE_NAME)

            # Test Directory
            self.test_file_path = os.path.join(self.ingested_data_dirr_path, config.TESTING_FILE_NAME)

            
        except Exception as e:
            raise CustomException(e, sys)