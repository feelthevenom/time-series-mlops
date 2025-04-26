from dataclasses import dataclass


@dataclass
class DataingestionArtifact:
    feature_store_path: str
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    train_file_path: str
    test_file_path: str
    is_data_validated: bool = False
    
@dataclass
class DataTransformationArtifact:
    preprocessed_data_file: str
    window_size: int

@dataclass
class ModelTrainingArtifact:
    train_model_path: str
    preprocessed_data: str

@dataclass
class ModelEvaluationArtifact:
    model_evaluation_file_path: str
    is_model_accepted: bool


