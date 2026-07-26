from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    data_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool

@dataclass
class DataTransformationArtifact:
    transformed_data_file_path: str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool

@dataclass
class ModelPusherArtifact:
    saved_model_dir: str