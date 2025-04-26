from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformtion import DataTransformation
from src.components.model_training import ModelTraining
from src.components.model_evaluate import ModelEvaluation
from src.entity.config_entity import DataingetionConfig, DatavalidationConfig, TrainingPipelineConfig, DataTransformationConfig, ModelTrainingConfig, ModelEvaluationConfig


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_artifact = None
        self.data_validation_artifact = None
        self.data_transformation_artifact = None
        self.model_training_artifact = None

    def start_data_ingestion(self):
        """
        This function is used to start the data ingestion process.
        """
        if self.data_ingestion_artifact is None:
            data_ingestion_config = DataingetionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            self.data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        return self.data_ingestion_artifact

    def start_data_validation(self):
        """
        This function is used to start the data validation process.
        """
        if self.data_validation_artifact is None:
            data_validation_config = DatavalidationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_validation_artifact = DataValidation(
                data_validation_config=data_validation_config,
                data_ingetion_artifact=self.start_data_ingestion()
            ).initiate_data_validation()
        return self.data_validation_artifact

    def start_data_transformation(self):
        """
        This function is used to start the data transformation process.
        """
        if self.data_transformation_artifact is None:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_transformation_artifact = DataTransformation(
                datavalidation_artifact=self.start_data_validation(),
                datatranformation_config=data_transformation_config
            ).initiate_data_transforamtion()
        return self.data_transformation_artifact

    def start_model_training(self):
        """
        This function is used to start the model training process.
        """
        if self.model_training_artifact is None:
            model_training_config = ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)
            self.model_training_artifact = ModelTraining(
                datatransformation_artifact=self.start_data_transformation(),
                model_training_config=model_training_config
            ).initiate_model_training()
        return self.model_training_artifact

    def start_model_evaluation(self):
        """
        This function is used to start the model evaluation process.
        """
        model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
        model_evaluation = ModelEvaluation(
            model_evaluation_config=model_evaluation_config,
            model_training_artifact=self.start_model_training()
        )
        model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
        print(model_evaluation_artifact.is_model_accepted)

