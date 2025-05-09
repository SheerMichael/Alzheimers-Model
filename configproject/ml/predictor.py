import os
import pickle
import numpy as np
import pandas as pd
from django.conf import settings

class MCIPredictor:
    """Class to load the MCI prediction model and make predictions"""

    def __init__(self):
        # Path to the pickled model dictionary
        model_path = os.path.join(settings.BASE_DIR, 'ml', 'model_data', 'knn_mci_detector.pkl')

        try:
            with open(model_path, 'rb') as f:
                model_bundle = pickle.load(f)

            # Expecting a dictionary with model, threshold, and feature_names
            self.model = model_bundle['model']
            self.threshold = model_bundle.get('threshold', 0.5)  # Default to 0.5 if not specified
            self.feature_names = model_bundle['feature_names']

            self.is_loaded = True
        except (FileNotFoundError, pickle.UnpicklingError, KeyError) as e:
            self.is_loaded = False
            self.error = str(e)

    def predict(self, data):
        """
        Make a prediction using the loaded model

        Args:
            data: Dictionary containing feature values

        Returns:
            Tuple of (prediction label (0/1), probability of positive class)
        """
        if not self.is_loaded:
            raise ValueError(f"Model failed to load: {self.error}")

        # Debug: print input data
        print("Cleaned input data:")
        for k, v in data.items():
            print(f"  {k}: {v}")

        # Ensure proper feature ordering
        try:
            input_row = [data[feature] for feature in self.feature_names]
        except KeyError as e:
            raise ValueError(f"Missing feature in input data: {e}")

        df = pd.DataFrame([input_row], columns=self.feature_names)

        # Debug: print dataframe being fed to model
        print("\n📄 DataFrame passed to model:")
        print(df)

        try:
            proba = self.model.predict_proba(df)[0][1]
            predicted_class = int(proba >= self.threshold)
        except Exception as e:
            print("Prediction error occurred")
            raise e

        return predicted_class, round(proba * 100, 2)  # Return probability as a percentage
