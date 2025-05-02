from src.components.model_evaluate import ModelEvaluation
from src.entity.config_entity import TrainingPipelineConfig, ModelEvaluationConfig
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys
import os
STAGE_NAME = "Model Evaluation"

print("Starting model evaluation pipeline...")

class ModelEvaluationPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)

    def start_model_evaluation(self):
        try:
            print("Checking model and preprocessed file existence...")
            print("Model path:", self.model_evaluation_config.train_model_file_path)
            print("Preprocessed path:", self.model_evaluation_config.preprocessed_file_path)
            print("Model exists:", os.path.exists(self.model_evaluation_config.train_model_file_path))
            print("Preprocessed exists:", os.path.exists(self.model_evaluation_config.preprocessed_file_path))
            # Run model evaluation
            model_evaluation = ModelEvaluation(
                model_evaluation_config=self.model_evaluation_config
            )
            model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation Pipeline Completed")
            logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
        except Exception as e:
            print("Exception occurred:", e)
            raise CustomException(e, sys)

if __name__ == "__main__":
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
    model_evaluation_pipeline = ModelEvaluationPipeline()
    model_evaluation_pipeline.start_model_evaluation()
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")