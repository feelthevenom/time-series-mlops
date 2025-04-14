from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataingetionConfig, DatavalidationConfig, TrainingPipelineConfig


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