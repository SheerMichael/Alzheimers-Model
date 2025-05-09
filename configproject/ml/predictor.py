import pandas as pd
import pickle
import os

class MCIPredictor:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'model_data', 'knn_mci_detector.pkl')
        with open(model_path, 'rb') as f:
            artifact = pickle.load(f)
        self.pipeline = artifact['model']
        self.threshold = artifact['threshold']
        self.required_features = artifact['feature_names']  # Not used here, but kept for reference

        # These are the raw input columns expected before one-hot encoding
        self.raw_columns = [
            'Age', 'BMI', 'SleepQuality', 'PhysicalActivity', 'DietQuality',
            'Gender', 'EducationLevel', 'Ethnicity', 'Smoking', 'AlcoholConsumption',
            'Diabetes', 'Hypertension', 'CardiovascularDisease', 'Depression',
            'HeadInjury', 'FamilyHistoryAlzheimers'
        ]

    def predict(self, data):
        df = pd.DataFrame([data])  # Single-row DataFrame
        missing = set(self.raw_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        df = df[self.raw_columns]  # Enforce correct column order
        proba = self.pipeline.predict_proba(df)[0, 1]
        pred = int(proba >= self.threshold)
        return pred, round(proba, 3)
