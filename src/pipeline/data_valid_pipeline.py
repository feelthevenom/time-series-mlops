from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import TrainingPipelineConfig, DataingetionConfig, DatavalidationConfig
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys

STAGE_NAME = "Data Validation"

class DataValidationPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataingetionConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_validation_config = DatavalidationConfig(training_pipeline_config=self.training_pipeline_config)

    def start_data_validation(self):
        try:
            # Run data ingestion
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            # Run data validation
            data_validation = DataValidation(
                data_validation_config=self.data_validation_config,
                data_ingetion_artifact=data_ingestion_artifact
            )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Pipeline Completed")
            logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
        data_validation_pipeline = DataValidationPipeline()
        data_validation_pipeline.start_data_validation()
    except Exception as e:
        raise CustomException(e, sys)