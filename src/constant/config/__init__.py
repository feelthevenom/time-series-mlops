"""
Constant Configurations for the project.
This module contains constant configurations used throughout the project.
It includes settings for the database, API keys, and other configurations.

"""
import os


SCHEMA_FILE_NAME: str = "schema.yaml"
WINDOW_SIZE=24

INFLUX_URL = "http://storedata-db:8086"
INFLUX_TOKEN = "RahulSuperSecretToken2024"
INFLUX_ORG = "Rahul-Personal"
INFLUX_BUCKET = "TimeseriesRetailDB"
INFLUX_MEASUREMENT = "time_series_retail_sales"
INFLUX_FIELD = "sales"
""""
Data Ingestion Configuration
"""
DATA_DIRR: str = "Dataset"
DATA_FILE_NAME: str = "retail_sales.csv"

os.makedirs('artifacts', exist_ok=True)

ARTIFACT_DIRR_NAME: str = "artifacts"
INGESTION_DIRR_NAME: str = "data_ingestion"

FEATURE_FILE_NAME: str = "feature_store.csv"
TRAINING_FILE_NAME: str = "train.csv"
TESTING_FILE_NAME: str = "test.csv"

"""
Data validation Configuration
"""

VALIDATION_DIRR_NAME: str = "data_validation"
DRIFT_REPORT_DIRR_PATH: str = "drift detection report"
DATA_SCHEMA_DIRR_NAME: str = "data_schema"
DATA_REPORT_FILE_NAME: str = "data_report.yaml"

"""
Data Transformation Configuration
"""

PREPROCESSED_FILE_DIRR: str = "Preprocessed"
PREPROCESS_FILE_NAME: str = "preprocess.npz"

"""
Model traininig Configuration
"""

MODEL_TRAINED_FILE_DIRR: str = "Trained models"
MODEL_TRAINED_FILE_NAME: str = "model.keras"
TRAIN_EPOCHS: int = 20
TRAIN_BATCH_SIZE: int = 32

"""
Model Evaluation Configuration
"""

MODEL_EVALUATION_FILE_DIRR: str = "Model Evaluation"
MODEL_EVALUATION_FILE_NAME: str = "model_evaluation.png"


