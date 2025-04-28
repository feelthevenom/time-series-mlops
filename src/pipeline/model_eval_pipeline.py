from src.components.model_evaluate import ModelEvaluation
from src.entity.config_entity import TrainingPipelineConfig, ModelEvaluationConfig, ModelTrainingConfig
from src.entity.artifact_entity import ModelTrainingArtifact
from src.exception.exception import CustomException
from src.logging.logger import logging
import sys

STAGE_NAME = "Model Evaluation"

class ModelEvaluationPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
        self.model_trainer_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)

    def start_model_evaluation(self):
        try:
            # Construct ModelTrainingArtifact with correct paths
            model_training_artifact = ModelTrainingArtifact(
                train_model_path=self.model_trainer_config.train_model_file_path,
                preprocessed_data=self.model_trainer_config.preprocessed_file_path if hasattr(self.model_trainer_config, 'preprocessed_file_path') else 'artifacts/Preprocessed/preprocess.npz'
            )
            # Run model evaluation
            model_evaluation = ModelEvaluation(
                model_evaluation_config=self.model_evaluation_config,
                model_training_artifact=model_training_artifact
            )
            model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation Pipeline Completed")
            logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")
    model_evaluation_pipeline = ModelEvaluationPipeline()
    model_evaluation_pipeline.start_model_evaluation()
    logging.info(f"{'='*20} {STAGE_NAME} {'='*20}")