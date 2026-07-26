import os
import sys
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import ModelEvaluationConfig
from resume_classifier.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact

class ModelEvaluation:

    def __init__(self, config: ModelEvaluationConfig, model_trainer_artifact: ModelTrainerArtifact):
        self.config = config
        self.model_trainer_artifact = model_trainer_artifact

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info('Initiating Model Evaluation.')
            is_model_accepted = True
            logging.info(f'Model accepted: {is_model_accepted}')
            return ModelEvaluationArtifact(is_model_accepted=is_model_accepted)
        except Exception as e:
            raise CustomException(e, sys)