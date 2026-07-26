import os
import sys
import shutil
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import DataTransformationConfig
from resume_classifier.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from transformers import AutoTokenizer

class DataTransformation:

    def __init__(self, config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        self.config = config
        self.data_validation_artifact = data_validation_artifact

    def clean_text(self, text: str) -> str:
        return text

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info('Initiating Data Transformation.')
            os.makedirs(os.path.dirname(self.config.transformed_data_path), exist_ok=True)
            shutil.copy2(self.config.data_path, self.config.transformed_data_path)
            logging.info(f'Transformed data saved at: {self.config.transformed_data_path}')
            return DataTransformationArtifact(transformed_data_file_path=self.config.transformed_data_path)
        except Exception as e:
            raise CustomException(e, sys)