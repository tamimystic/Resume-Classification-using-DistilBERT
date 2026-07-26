from dataclasses import dataclass
import os

@dataclass
class DataIngestionConfig:
    root_dir: str = os.path.join('artifacts', 'data_ingestion')
    source_data_path: str = os.path.join('dataset', 'dataset.parquet')
    local_data_path: str = os.path.join('artifacts', 'data_ingestion', 'dataset.parquet')

@dataclass
class DataValidationConfig:
    root_dir: str = os.path.join('artifacts', 'data_validation')
    data_path: str = os.path.join('artifacts', 'data_ingestion', 'dataset.parquet')
    status_file: str = os.path.join('artifacts', 'data_validation', 'status.txt')

@dataclass
class DataTransformationConfig:
    root_dir: str = os.path.join('artifacts', 'data_transformation')
    data_path: str = os.path.join('artifacts', 'data_ingestion', 'dataset.parquet')
    tokenizer_name: str = 'distilbert-base-uncased'
    transformed_data_path: str = os.path.join('artifacts', 'data_transformation', 'transformed_data.parquet')

@dataclass
class ModelTrainerConfig:
    root_dir: str = os.path.join('artifacts', 'model_trainer')
    pretrained_model_path: str = 'saved_model'
    trained_model_path: str = os.path.join('artifacts', 'model_trainer', 'model')

@dataclass
class ModelEvaluationConfig:
    root_dir: str = os.path.join('artifacts', 'model_evaluation')
    model_path: str = os.path.join('artifacts', 'model_trainer', 'model')
    data_path: str = os.path.join('artifacts', 'data_transformation', 'transformed_data.parquet')

@dataclass
class ModelPusherConfig:
    root_dir: str = os.path.join('artifacts', 'model_pusher')
    saved_model_path: str = os.path.join('final_models')