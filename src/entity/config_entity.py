import sys
import os
from datetime import datetime

from src.exception.exception import CustomException
from src.logging.logger import logging

from src.constant import config

logger = logging.getLogger(__name__)

class TrainingPipelineConfig:
    def __init__(self, time_stamp = datetime.now()):
        self.artifact_name = config.ARTIFACT_DIRR_NAME
        self.artifact_dir = os.path.join(self.artifact_name)
        self.timestamp: str = time_stamp.strftime("%Y-%m-%d-%H-%M-%S")

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Data Ingestion Configuration for ingesting the data from the source and saving it to the specified directory.
        """
        try:
            # InfluxDB URL
            self.influxdb_url: str = config.INFLUX_URL
            # InfluxDB Token
            self.influxdb_token: str = config.INFLUX_TOKEN
            # InfluxDB Organization
            self.influxdb_org: str = config.INFLUX_ORG
            # InfluxDB Bucket
            self.influxdb_bucket: str = config.INFLUX_BUCKET
            # InfluxDB Measurement
            self.influxdb_measurement: str = config.INFLUX_MEASUREMENT
            # InfluxDB Field
            self.influxdb_field: str = config.INFLUX_FIELD
            # Dataset Directory
            self.dataset_dir: str = os.path.join(config.DATA_DIRR, config.DATA_FILE_NAME)
            # Data Ingested Directory
            self.ingested_data_dir_path: str = os.path.join(training_pipeline_config.artifact_dir, config.INGESTION_DIRR_NAME)
            # Feature Directory
            self.feature_store_file_path: str = os.path.join(self.ingested_data_dir_path, config.FEATURE_FILE_NAME)
            # Train Directory
            self.train_file_path: str = os.path.join(self.ingested_data_dir_path, config.TRAINING_FILE_NAME)
            # Test Directory
            self.test_file_path: str = os.path.join(self.ingested_data_dir_path, config.TESTING_FILE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Data Validation configuration for validating the data
        """
        try:
            # Ingested data dir path
            self.ingested_data_dir_path: str = os.path.join(training_pipeline_config.artifact_dir, config.INGESTION_DIRR_NAME)
            # Feature Directory
            self.feature_store_file_path: str = os.path.join(self.ingested_data_dir_path, config.FEATURE_FILE_NAME)
            # Train Directory
            self.train_file_path: str = os.path.join(self.ingested_data_dir_path, config.TRAINING_FILE_NAME)
            # Test Directory
            self.test_file_path: str = os.path.join(self.ingested_data_dir_path, config.TESTING_FILE_NAME)
            # Data Report file path to save the data report
            self.data_report_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.VALIDATION_DIRR_NAME, config.DATA_REPORT_FILE_NAME)
            # Data Validation Directory to save the validated results
            self.validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, config.VALIDATION_DIRR_NAME)
            # Drift Report Directory to save the drift report
            self.drift_report_dir_path: str = os.path.join(self.validation_dir, config.DRIFT_REPORT_DIRR_PATH)
            # schema file path to validate the columns and data types
            self.schema_file_path: str = os.path.join(config.DATA_SCHEMA_DIRR_NAME, config.SCHEMA_FILE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Data Transformation config for training the model.
        """
        try:
            # Data Report file path to save the data report
            self.data_report_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.VALIDATION_DIRR_NAME, config.DATA_REPORT_FILE_NAME)
            # Preprocessed file path to save and load for training
            self.preprocessed_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.PREPROCESSED_FILE_DIRR, config.PREPROCESS_FILE_NAME)
            # Window size for the model
            self.window_size: int = config.WINDOW_SIZE
            # Train Directory
            self.train_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.INGESTION_DIRR_NAME, config.TRAINING_FILE_NAME)
            # Test Directory
            self.test_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.INGESTION_DIRR_NAME, config.TESTING_FILE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

class ModelTrainingConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            # Preprocessed file path to save and load for training
            self.preprocessed_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.PREPROCESSED_FILE_DIRR, config.PREPROCESS_FILE_NAME)
            # Model Trained File Path to save the model
            self.train_model_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.MODEL_TRAINED_FILE_DIRR, config.MODEL_TRAINED_FILE_NAME)
            # Train Epochs
            self.train_epoch: int = config.TRAIN_EPOCHS
            # Train Batch Size
            self.train_batch: int = config.TRAIN_BATCH_SIZE
            # Window Size
            self.window_size: int = config.WINDOW_SIZE
        except Exception as e:
            raise CustomException(e, sys)

class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            # Preprocessed file path to save and load for training
            self.preprocessed_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.PREPROCESSED_FILE_DIRR, config.PREPROCESS_FILE_NAME)
            # Model Trained File Path to save the model
            self.train_model_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.MODEL_TRAINED_FILE_DIRR, config.MODEL_TRAINED_FILE_NAME)
            # Model Evaluation File Path to save the model evaluation
            self.model_evaluation_file_path: str = os.path.join(training_pipeline_config.artifact_dir, config.MODEL_EVALUATION_FILE_DIRR, config.MODEL_EVALUATION_FILE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

