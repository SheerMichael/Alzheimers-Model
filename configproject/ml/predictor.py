import os
import pickle
import pandas as pd
import numpy as np
from django.conf import settings

class AlzheimersPredictor:
    """Class for making Alzheimer's disease predictions using the loaded model"""
    
    def __init__(self):
        self.model = None
        self.load_model()
        
        # Define feature columns in the correct order expected by the model
        self.feature_columns = [
            'Age', 'Gender', 'Ethnicity', 'EducationLevel', 'BMI', 'Smoking',
            'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
            'FamilyHistoryAlzheimers', 'CardiovascularDisease', 'Diabetes', 'Depression',
            'HeadInjury', 'Hypertension', 'SystolicBP', 'DiastolicBP', 'CholesterolTotal',
            'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides', 'MMSE',
            'FunctionalAssessment', 'MemoryComplaints', 'BehavioralProblems', 'ADL',
            'Confusion', 'Disorientation', 'PersonalityChanges', 'DifficultyCompletingTasks',
            'Forgetfulness'
        ]
        
        # Define the target variable mapping
        self.target_mapping = {
            0: 'Negative',
            1: 'Positive',
            2: 'MCI'  # Mild Cognitive Impairment
        }
    
    def load_model(self):
        """Load the pickled model"""
        model_path = os.path.join(
            settings.BASE_DIR, 
            'ml', 
            'model_data', 
            'alzheimers_k_nearest_neighbors_model.pkl'
        )
        
        try:
            with open(model_path, 'rb') as file:
                self.model = pickle.load(file)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_data(self, input_data):
        """Preprocess the input data to match the model's expected format"""
        
        # Convert Django model instance to dictionary
        if hasattr(input_data, '__dict__'):
            data_dict = {
                'Age': input_data.age,
                'Gender': self._encode_gender(input_data.gender),
                'Ethnicity': input_data.ethnicity,
                'EducationLevel': input_data.education_level,
                'BMI': input_data.bmi,
                'Smoking': int(input_data.smoking),
                'AlcoholConsumption': self._encode_alcohol(input_data.alcohol_consumption),
                'PhysicalActivity': self._encode_activity(input_data.physical_activity),
                'DietQuality': self._encode_quality(input_data.diet_quality),
                'SleepQuality': self._encode_quality(input_data.sleep_quality),
                'FamilyHistoryAlzheimers': int(input_data.family_history_alzheimers),
                'CardiovascularDisease': int(input_data.cardiovascular_disease),
                'Diabetes': int(input_data.diabetes),
                'Depression': int(input_data.depression),
                'HeadInjury': int(input_data.head_injury),
                'Hypertension': int(input_data.hypertension),
                'SystolicBP': input_data.systolic_bp,
                'DiastolicBP': input_data.diastolic_bp,
                'CholesterolTotal': input_data.cholesterol_total,
                'CholesterolLDL': input_data.cholesterol_ldl,
                'CholesterolHDL': input_data.cholesterol_hdl,
                'CholesterolTriglycerides': input_data.cholesterol_triglycerides,
                'MMSE': input_data.mmse,
                'FunctionalAssessment': input_data.functional_assessment,
                'MemoryComplaints': int(input_data.memory_complaints),
                'BehavioralProblems': int(input_data.behavioral_problems),
                'ADL': input_data.adl,
                'Confusion': int(input_data.confusion),
                'Disorientation': int(input_data.disorientation),
                'PersonalityChanges': int(input_data.personality_changes),
                'DifficultyCompletingTasks': int(input_data.difficulty_completing_tasks),
                'Forgetfulness': int(input_data.forgetfulness)
            }
        else:
            # If it's already a dictionary
            data_dict = input_data
        
        # Convert to DataFrame with proper column order
        df = pd.DataFrame([data_dict])
        
        # Ensure all columns are in the correct order
        df = df[self.feature_columns]
        
        return df
    
    def predict(self, input_data):
        """Make a prediction using the loaded model"""
        if self.model is None:
            self.load_model()
        
        # Preprocess the data
        processed_data = self.preprocess_data(input_data)
        
        # Make prediction
        try:
            # Get class prediction
            prediction_class = self.model.predict(processed_data)[0]
            prediction_label = self.target_mapping.get(prediction_class, 'Unknown')
            
            # Get probability scores if available
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(processed_data)[0]
                prediction_probability = probabilities[prediction_class]
            else:
                prediction_probability = None
                
            return {
                'prediction': prediction_label,
                'probability': prediction_probability,
                'prediction_class': prediction_class
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                'prediction': 'Error',
                'probability': None,
                'error': str(e)
            }
    
    def _encode_gender(self, gender):
        """Encode gender to match training data format"""
        gender_map = {'M': 0, 'F': 1, 'O': 2}
        return gender_map.get(gender, 0)
    
    def _encode_alcohol(self, alcohol):
        """Encode alcohol consumption to match training data format"""
        alcohol_map = {'None': 0, 'Occasional': 1, 'Moderate': 2, 'Heavy': 3}
        return alcohol_map.get(alcohol, 0)
    
    def _encode_activity(self, activity):
        """Encode physical activity to match training data format"""
        activity_map = {'Low': 0, 'Moderate': 1, 'High': 2}
        return activity_map.get(activity, 0)
    
    def _encode_quality(self, quality):
        """Encode quality metrics to match training data format"""
        quality_map = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Excellent': 3}
        return quality_map.get(quality, 0)