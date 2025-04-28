from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformtion import DataTransformation
from src.components.model_training import ModelTraining
from src.entity.config_entity import TrainingPipelineConfig, DataingetionConfig, DatavalidationConfig, DataTransformationConfig, ModelTrainingConfig
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys

STAGE_NAME = "Model Training"

class ModelTrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataingetionConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_validation_config = DatavalidationConfig(training_pipeline_config=self.training_pipeline_config)
        self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
        self.model_trainer_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)

    def start_model_training(self):
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
            # Run data transformation
            data_transformation = DataTransformation(
                datavalidation_artifact=data_validation_artifact,
                datatranformation_config=self.data_transformation_config
            )
            data_transformation_artifact = data_transformation.initiate_data_transforamtion()
            # Run model training
            model_trainer = ModelTraining(
                datatransformation_artifact=data_transformation_artifact,
                model_training_config=self.model_trainer_config
            )
            model_training_artifact = model_trainer.initiate_model_training()
            logging.info(f"Model Training Pipeline Completed")
            logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
            return model_training_artifact
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
    model_training_pipeline = ModelTrainingPipeline()
    model_training_pipeline.start_model_training()
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")