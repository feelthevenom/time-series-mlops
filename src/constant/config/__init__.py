"""
Constant Configurations for the project.
This module contains constant configurations used throughout the project.
It includes settings for the database, API keys, and other configurations.

"""
import os


data_dirr: str = "Dataset"
data_file_name: str = "retail_sales.csv"

os.makedirs('Artifact', exist_ok=True)

artifact_dir: str = "Artifact"
