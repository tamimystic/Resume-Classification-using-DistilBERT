import os
import sys
import yaml
import json
import dill
from resume_classifier.logger import logging
from resume_classifier.exception import CustomException

def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys)

def save_object(file_path: str, obj: object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path: str) -> object:
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)

def load_json(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        raise CustomException(e, sys)