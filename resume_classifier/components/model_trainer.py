import os
import sys
import shutil
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import ModelTrainerConfig
from resume_classifier.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

class ModelTrainer:

    def __init__(self, config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        self.config = config
        self.data_transformation_artifact = data_transformation_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info('Initiating Model Trainer.')
            os.makedirs(self.config.trained_model_path, exist_ok=True)
            source_dir = self.config.pretrained_model_path
            dest_dir = self.config.trained_model_path
            if os.path.exists(source_dir):
                for item in os.listdir(source_dir):
                    s = os.path.join(source_dir, item)
                    d = os.path.join(dest_dir, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                logging.info(f'Loaded pre-trained model and saved to: {dest_dir}')
            else:
                logging.error('Saved model directory not found!')
            return ModelTrainerArtifact(trained_model_file_path=dest_dir)
        except Exception as e:
            raise CustomException(e, sys)