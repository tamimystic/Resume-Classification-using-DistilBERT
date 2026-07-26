import os
import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from resume_classifier.exception import CustomException
from resume_classifier.logger import logging

class PredictionPipeline:

    def __init__(self):
        self.model_path = os.path.join('final_models')
        self.labels_path = os.path.join('labels', 'labels.json')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            with open(self.labels_path, 'r') as f:
                self.labels = json.load(f)
        except Exception as e:
            logging.error('Failed to load model or labels.')
            raise CustomException(e, sys)

    def predict(self, text: str) -> str:
        try:
            inputs = self.tokenizer(text, padding='max_length', truncation=True, max_length=512, return_tensors='pt')
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=-1).item()
            return self.labels[predicted_class_id]
        except Exception as e:
            raise CustomException(e, sys)