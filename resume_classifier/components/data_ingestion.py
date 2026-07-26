import os
import sys
import shutil
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import DataIngestionConfig
from resume_classifier.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f'Initiating Data Ingestion. Source data path: {self.config.source_data_path}')
            os.makedirs(os.path.dirname(self.config.local_data_path), exist_ok=True)
            shutil.copy2(self.config.source_data_path, self.config.local_data_path)
            logging.info(f'Data copied to: {self.config.local_data_path}')
            return DataIngestionArtifact(data_file_path=self.config.local_data_path)
        except Exception as e:
            raise CustomException(e, sys)