import sys
import os

import pandas as pd

from src.exception.exception import CustomException
from src.logging.logger import logging

logger = logging.getLogger(__name__)


from src.entity.artifact_entity import DataingestionArtifact
from src.entity.config_entity import DatavalidationConfig

from src.utils.helper import read_yaml_file

class DataValidation:
    def __init__(self, data_validation_config: DatavalidationConfig):
        
        self.data_validation_config = data_validation_config

    def is_columns_exist(self, schema_file_path: str, df: pd.DataFrame)->bool:
        try:
            schema = read_yaml_file(schema_file_path)
            columns = schema['columns']
            print(columns)
        except Exception as e:
            raise CustomException(e, sys)