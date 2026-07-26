import os
import sys
import shutil
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import ModelPusherConfig
from resume_classifier.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact

class ModelPusher:

    def __init__(self, config: ModelPusherConfig, model_evaluation_artifact: ModelEvaluationArtifact, model_trainer_artifact: ModelTrainerArtifact):
        self.config = config
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info('Initiating Model Pusher.')
            os.makedirs(self.config.saved_model_path, exist_ok=True)
            if self.model_evaluation_artifact.is_model_accepted:
                source_dir = self.model_trainer_artifact.trained_model_file_path
                dest_dir = self.config.saved_model_path
                for item in os.listdir(source_dir):
                    s = os.path.join(source_dir, item)
                    d = os.path.join(dest_dir, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                logging.info(f'Model pushed to final directory: {dest_dir}')
            else:
                logging.info('Model not accepted, skipping push.')
            return ModelPusherArtifact(saved_model_dir=self.config.saved_model_path)
        except Exception as e:
            raise CustomException(e, sys)