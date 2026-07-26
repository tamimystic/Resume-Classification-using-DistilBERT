import os
import sys
import pandas as pd
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import DataValidationConfig
from resume_classifier.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact

class DataValidation:

    def __init__(self, config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        self.config = config
        self.data_ingestion_artifact = data_ingestion_artifact

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info('Initiating Data Validation.')
            os.makedirs(os.path.dirname(self.config.status_file), exist_ok=True)
            df = pd.read_parquet(self.data_ingestion_artifact.data_file_path)
            validation_status = True
            expected_cols = ['attention_mask', 'input_ids', 'label']
            for col in expected_cols:
                if col not in df.columns:
                    validation_status = False
                    break
            with open(self.config.status_file, 'w') as f:
                f.write(f'Validation status: {validation_status}')
            logging.info(f'Data Validation completed. Status: {validation_status}')
            return DataValidationArtifact(validation_status=validation_status)
        except Exception as e:
            raise CustomException(e, sys)