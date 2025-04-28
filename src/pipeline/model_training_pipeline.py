from src.components.model_training import ModelTraining
from src.entity.config_entity import TrainingPipelineConfig, ModelTrainingConfig
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys

STAGE_NAME = "Model Training"

class ModelTrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.model_trainer_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)

    def start_model_training(self):
        try:
            # Run model training
            model_trainer = ModelTraining(
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