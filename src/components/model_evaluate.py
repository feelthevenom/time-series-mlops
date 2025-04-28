
import os, sys
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelEvaluationArtifact

from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error

from src.utils.helper import read_preprocessed_data

logger = logging.getLogger(__name__)

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig):
        try:
            self.model_evaluation_config = model_evaluation_config
            self.preprocessed_data = self.model_evaluation_config.preprocessed_file_path
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def evaluate_model(self, model: str, X_test: np.ndarray, y_test: np.ndarray):
        try:
            """
            Reading the model and testing the model
            """
            model = load_model(model)
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            logger.info(f"Model evaluation completed. MSE: {mse}")
            return mse
        except Exception as e:
            raise CustomException(e, sys)
    def save_plot_predictions(self, model: str, X_test: np.ndarray, y_test: np.ndarray, ts_test: np.ndarray, model_evaluation_file_dirr: str):
        try:
            """
            Plotting the predictions with time stamp data from ts_test and y_test
            """

            directory = os.path.dirname(model_evaluation_file_dirr)

            os.makedirs(directory, exist_ok=True)

            # Changing to datetime format
            ts_test = pd.to_datetime(ts_test)

            # Plotting the predictions
            model = load_model(model) 
            y_pred = model.predict(X_test)
            plt.figure(figsize=(10, 5))
            plt.plot(ts_test, y_test, label='Actual')
            plt.plot(ts_test, y_pred, label='Predicted')
            plt.legend()
            plt.savefig(model_evaluation_file_dirr)
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_model_evaluation(self):
        try:
            logger.info("Model Evaluation started")

            model_train_file_path = self.model_evaluation_config.train_model_file_path

            model_evaluation_file_dirr = self.model_evaluation_config.model_evaluation_file_path
            _, _, _, X_test, y_test, ts_test = read_preprocessed_data(filepath=self.preprocessed_data)

            model_evaluation = self.evaluate_model(model=model_train_file_path, X_test=X_test, y_test=y_test)
            self.save_plot_predictions(model=model_train_file_path, X_test=X_test, y_test=y_test, ts_test=ts_test, model_evaluation_file_dirr=model_evaluation_file_dirr)

            if model_evaluation <= 25:
                return ModelEvaluationArtifact(
                    model_evaluation_file_path=model_evaluation_file_dirr,
                    is_model_accepted=True
                )
            else:
                return ModelEvaluationArtifact(
                    model_evaluation_file_path=model_evaluation_file_dirr,
                    is_model_accepted=False
                    )
            
        except Exception as e:
            raise CustomException(e, sys)
