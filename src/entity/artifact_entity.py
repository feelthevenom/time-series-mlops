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
    