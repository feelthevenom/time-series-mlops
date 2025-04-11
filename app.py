from src.components.data_ingetion import DataIngestion
from src.entity.config_entity import DataingetionConfig, TrainingPipelineConfig


if __name__ == "__main__":


    training_pipeline_config = TrainingPipelineConfig()
    # Data ingetion Config
    data_ingestion_config = DataingetionConfig(training_pipeline_config=training_pipeline_config)
    # Data Ingestion
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)

    df = data_ingestion.read_source_data()
    data_ingestion.split_data_into_train_test(df=df)