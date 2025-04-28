from src.components.data_ingetion import DataIngestion
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from src.exception.exception import CustomException

from src.logging.logger import logging
import sys

STAGE_NAME = "Data Ingestion"

class DataIngestionPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)

    def start_data_ingestion(self):
        try:
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            return self.data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e, sys)
    
if __name__ == "__main__":
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.start_data_ingestion()
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
