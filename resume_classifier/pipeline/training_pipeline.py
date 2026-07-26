import sys
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException
from resume_classifier.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from resume_classifier.components.data_ingestion import DataIngestion
from resume_classifier.components.data_validation import DataValidation
from resume_classifier.components.data_transformation import DataTransformation
from resume_classifier.components.model_trainer import ModelTrainer
from resume_classifier.components.model_evaluation import ModelEvaluation
from resume_classifier.components.model_pusher import ModelPusher

class TrainingPipeline:

    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            logging.info('Starting Training Pipeline')
            data_ingestion_config = DataIngestionConfig()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            data_validation_config = DataValidationConfig()
            data_validation = DataValidation(config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            if not data_validation_artifact.validation_status:
                raise Exception('Data Validation Failed')
            data_transformation_config = DataTransformationConfig()
            data_transformation = DataTransformation(config=data_transformation_config, data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            model_trainer_config = ModelTrainerConfig()
            model_trainer = ModelTrainer(config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            model_evaluation_config = ModelEvaluationConfig()
            model_evaluation = ModelEvaluation(config=model_evaluation_config, model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_config = ModelPusherConfig()
                model_pusher = ModelPusher(config=model_pusher_config, model_evaluation_artifact=model_evaluation_artifact, model_trainer_artifact=model_trainer_artifact)
                model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info('Training Pipeline Completed Successfully')
        except Exception as e:
            raise CustomException(e, sys)
if __name__ == '__main__':
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()