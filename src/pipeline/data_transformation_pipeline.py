from src.components.data_transformtion import DataTransformation
from src.entity.config_entity import TrainingPipelineConfig, DataTransformationConfig
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys

STAGE_NAME = "Data Transformation"

class DataTransformationPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)

    def start_data_transformation(self):
        try:
            # Run data transformation
            data_transformation = DataTransformation(
                datatranformation_config=self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transforamtion()
            logging.info(f"Data Transformation Pipeline Completed")
            logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
    data_transformation_pipeline = DataTransformationPipeline()
    data_transformation_pipeline.start_data_transformation()
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")