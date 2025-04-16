"""
Constant Configurations for the project.
This module contains constant configurations used throughout the project.
It includes settings for the database, API keys, and other configurations.

"""
import os


SCHEMA_FILE_NAME: str = "schema.yaml"
WINDOW_SIZE=24



""""
Data Ingestion Configuration
"""
DATA_DIRR: str = "Dataset"
DATA_FILE_NAME: str = "retail_sales.csv"

os.makedirs('artifacts', exist_ok=True)

ARTIFACT_DIRR_NAME: str = "artifacts"
INGETION_DIRR_NAME: str = "data_ingestion"

FEATURE_FILE_NAME: str = "feature_store.csv"
TRAINING_FILE_NAME: str = "train.csv"
TESTING_FILE_NAME: str = "test.csv"

"""
Data validation Configuration
"""

VALIDATION_DIRR_NAME: str = "data_validation"
DRIFT_REPORT_DIRR_PATH: str = "drift detection report"
DATA_SCHEMA_DIRR_NAME: str = "data_schema"

"""
Data Transformation Configuration
"""

PREPROCESSED_FILE_DIRR: str = "Preprocessed"
PREPROCESS_FILE_NAME: str = "preprocess.npz"
