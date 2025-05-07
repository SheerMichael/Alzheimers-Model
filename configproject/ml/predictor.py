import os
import pickle
import logging
import pandas as pd
import numpy as np
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Externalize feature columns and encoding maps
FEATURE_COLUMNS = [
    'Age', 'Gender', 'EducationLevel', 'BMI', 'Smoking',
    'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
    'FamilyHistoryAlzheimers', 'CardiovascularDisease', 'Diabetes', 'Depression',
    'HeadInjury', 'Hypertension', 'SystolicBP', 'DiastolicBP', 'CholesterolTotal',
    'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides', 'MMSE',
    'FunctionalAssessment', 'MemoryComplaints', 'BehavioralProblems', 'ADL',
    'Confusion', 'Disorientation', 'PersonalityChanges', 'DifficultyCompletingTasks',
    'Forgetfulness'
]

# Encoding maps
GENDER_MAP = {'M': 0, 'F': 1, 'O': 2, None: 0}  # None as fallback
ALCOHOL_MAP = {'None': 0, 'Occasional': 1, 'Moderate': 2, 'Heavy': 3, None: 0}
ACTIVITY_MAP = {'Low': 0, 'Moderate': 1, 'High': 2, None: 0}
QUALITY_MAP = {'Poor': 0, 'Fair': 1, 'Good': 2, 'Excellent': 3, None: 0}

# Target variable mapping
TARGET_MAPPING = {
    0: 'Negative',
    1: 'Positive',
    2: 'MCI'  # Mild Cognitive Impairment
}


class AlzheimersPredictor:
    """Class for making Alzheimer's disease predictions using the loaded model"""
    
    # Cache the model as a class attribute
    _model = None
    
    @classmethod
    def get_model(cls):
        """Load model if not already loaded and return it"""
        if cls._model is None:
            model_path = os.path.join(
                settings.BASE_DIR, 
                'ml', 
                'model_data', 
                'alzheimers_k-nearest_neighbors_model.pkl'
            )
            
            try:
                with open(model_path, 'rb') as file:
                    cls._model = pickle.load(file)
                logger.info(f"Model loaded successfully from {model_path}")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise RuntimeError(f"Failed to load prediction model: {e}") from e
        
        return cls._model
    
    def __init__(self):
        """Initialize the predictor"""
        # Ensure model is loaded
        self.model = self.get_model()
    
    def preprocess_data(self, input_data):
        """Preprocess the input data to match the model's expected format"""
        
        # Convert Django model instance to dictionary
        if hasattr(input_data, '__dict__'):
            data_dict = {
                'Age': input_data.age,
                'Gender': self._encode_gender(input_data.gender),
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
        
        # Validate all required fields are present
        missing_fields = [field for field in FEATURE_COLUMNS if field not in data_dict]
        if missing_fields:
            raise ValueError(f"Missing required fields for prediction: {', '.join(missing_fields)}")
        
        # Convert to DataFrame with proper column order
        df = pd.DataFrame([data_dict])
        
        # Ensure all columns are in the correct order
        try:
            df = df[FEATURE_COLUMNS]
        except KeyError as e:
            logger.error(f"Missing columns in input data: {e}")
            raise ValueError(f"Input data missing required columns: {e}")
        
        return df
    
    def predict(self, input_data):
        """Make a prediction using the loaded model"""
        # Preprocess the data
        try:
            processed_data = self.preprocess_data(input_data)
        except Exception as e:
            logger.error(f"Error preprocessing data: {e}")
            raise ValueError(f"Failed to preprocess input data: {e}") from e
        
        # Make prediction
        try:
            # Get class prediction
            prediction_class = self.model.predict(processed_data)[0]
            prediction_label = TARGET_MAPPING.get(prediction_class, 'Unknown')
            
            # Get probability scores if available
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(processed_data)[0]
                prediction_probability = float(probabilities[prediction_class])
            else:
                prediction_probability = None
                
            return {
                'prediction': prediction_label,
                'probability': prediction_probability,
                'prediction_class': int(prediction_class)
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise RuntimeError(f"Error making prediction: {e}") from e
    
    def _encode_gender(self, gender):
        """Encode gender to match training data format"""
        return GENDER_MAP.get(gender, 0)
    
    def _encode_alcohol(self, alcohol):
        """Encode alcohol consumption to match training data format"""
        return ALCOHOL_MAP.get(alcohol, 0)
    
    def _encode_activity(self, activity):
        """Encode physical activity to match training data format"""
        return ACTIVITY_MAP.get(activity, 0)
    
    def _encode_quality(self, quality):
        """Encode quality metrics to match training data format"""
        return QUALITY_MAP.get(quality, 0)