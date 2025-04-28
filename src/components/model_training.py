import os
import sys
import mlflow
import mlflow.tensorflow
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from src.logging.logger import logging
from src.exception.exception import CustomException
from src.entity.artifact_entity import ModelTrainingArtifact
from src.entity.config_entity import ModelTrainingConfig
from src.utils.helper import read_preprocessed_data

logger = logging.getLogger(__name__)

class ModelTraining:
    def __init__(self, model_training_config: ModelTrainingConfig):
        self.preprocessed_data = model_training_config.preprocessed_file_path
        self.window_size = model_training_config.window_size
        self.model_trained_path = model_training_config.train_model_file_path
        self.epochs = model_training_config.train_epoch
        self.batch_size = model_training_config.train_batch

    def load_preprocessed_data(self, file_path: str):
        X_train, y_train, ts_train, X_test, y_test, ts_test = read_preprocessed_data(file_path)
        return X_train, y_train, ts_train, X_test, y_test, ts_test

    def build_model(self, model_type, units, num_layers, activation, input_shape):
        model = Sequential()
        for i in range(num_layers):
            return_seq = i < num_layers - 1
            if model_type == "LSTM":
                model.add(LSTM(units, activation=activation, return_sequences=return_seq, input_shape=input_shape if i == 0 else None))
            elif model_type == "GRU":
                model.add(GRU(units, activation=activation, return_sequences=return_seq, input_shape=input_shape if i == 0 else None))
            elif model_type == "Dense":
                model.add(Dense(units, activation=activation, input_shape=input_shape if i == 0 else None))

        model.add(Dense(1))
        model.compile(optimizer=Adam(), loss="mse")
        return model

    def initiate_model_training(self):
        try:
            logger.info("Model training initiated!")

            X_train, y_train, ts_train, X_test, y_test, ts_test = self.load_preprocessed_data(file_path=self.preprocessed_data)

            # Enable MLflow autologging for automatic logging of model parameters, metrics, etc.
            mlflow.tensorflow.autolog()

            with mlflow.start_run(run_name="LSTM_Model_Training"):
                # Define model parameters (can also be loaded from config files)
                model_type = "LSTM"
                units = 50
                num_layers = 1
                activation = "relu"

                # Build the model
                model = self.build_model(model_type, units, num_layers, activation, input_shape=(self.window_size, 1))

                # Early stopping callback to prevent overfitting
                early_stopping = EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True)

                # Start training the model
                logger.info("Model training started.")
                history = model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, 
                                    validation_data=(X_test, y_test), callbacks=[early_stopping])

                # Save the model
                os.makedirs(os.path.dirname(self.model_trained_path), exist_ok=True)
                model.save(self.model_trained_path)
                logger.info(f"Model trained successfully and saved at {self.model_trained_path}")

                # Log additional metrics and model details to MLflow
                mlflow.log_metric("final_loss", history.history["loss"][-1])
                mlflow.log_metric("final_val_loss", history.history["val_loss"][-1])
                mlflow.log_param("model_type", model_type)
                mlflow.log_param("units", units)
                mlflow.log_param("num_layers", num_layers)
                mlflow.log_param("activation", activation)

            return ModelTrainingArtifact(
                train_model_path=self.model_trained_path,
                preprocessed_data=self.preprocessed_data
                )

        except Exception as e:
            raise CustomException(e, sys)
