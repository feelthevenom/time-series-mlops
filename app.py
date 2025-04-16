from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformtion import DataTransformation
from src.components.model_training import ModelTrainging

from src.entity.config_entity import DataingetionConfig, DatavalidationConfig, TrainingPipelineConfig, DataTransformationConfig, ModelTrainingConfig


if __name__ == "__main__":


    training_pipeline_config = TrainingPipelineConfig()
    # Data ingetion Config
    data_ingestion_config = DataingetionConfig(training_pipeline_config=training_pipeline_config)
    # Data Ingestion
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)

    data_ingetion_artifact = data_ingestion.initiate_data_ingestion()

    # Data Validation
    data_validation_config = DatavalidationConfig(training_pipeline_config=training_pipeline_config)

    data_validation = DataValidation(data_validation_config=data_validation_config, data_ingetion_artifact = data_ingetion_artifact)

    data_validation_artifact = data_validation.initiate_data_validation()

    # Data transforming
    data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)

    data_transformation = DataTransformation(datavalidation_artifact=data_validation_artifact, datatranformation_config = data_transformation_config)

    data_transformation_artifact = data_transformation.initiate_data_transforamtion()

    # Model training
    model_training_config = ModelTrainingConfig(training_pipeline_config = training_pipeline_config) 

    model_training = ModelTrainging(datatransformation_artifcat= data_transformation_artifact, model_training_config = model_training_config)

    model_training.initiate_model_training()