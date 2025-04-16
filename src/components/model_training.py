import os
import sys

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

from src.logging.logger import logging
from src.exception.exception import CustomException

from src.entity.artifact_entity import ModelTrainingArtifact, DataTransformationArtifact
from src.entity.config_entity import ModelTrainingConfig

from src.utils.helper import read_preprocessed_data

logger = logging.getLogger(__name__)

class ModelTrainging:
    def __init__(self, datatransformation_artifcat: DataTransformationArtifact,
                        model_training_config: ModelTrainingConfig):
        
        self.preprocessed_data = datatransformation_artifcat.preprocessed_data_file

        self.window_size = datatransformation_artifcat.window_size

        self.model_trained_path = model_training_config.train_model_file_path

        self.epochs = model_training_config.train_epoch

        self.batch_size = model_training_config.train_batch

    def load_preproccesed_data(self, file_path: str):
        X_train, y_train, ts_train, X_test, y_test, ts_test = read_preprocessed_data(file_path)

        return X_train, y_train, ts_train, X_test, y_test, ts_test


    def initiate_model_training(self):
        try:
            logger.info("Model training Initiated!")

            X_train, y_train, ts_train, X_test, y_test, ts_test = self.load_preproccesed_data( file_path = self.preprocessed_data)

            model = Sequential([
                LSTM(50, activation='relu', input_shape=(self.window_size, 1)),
                Dense(1)
            ])

            model.compile(optimizer='adam', loss='mse')

            logger.info("Model trianing started")

            model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_data=(X_test, y_test))

            model_path = os.path.dirname(self.model_trained_path)

            os.makedirs(model_path, exist_ok= True)
            model.save(self.model_trained_path)
            logger.info(f"Model trained successfull and saved in {self.model_trained_path}")

        except Exception as e:
            raise CustomException(e, sys)