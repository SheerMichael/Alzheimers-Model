import pickle
import os
import numpy as np
from django.conf import settings

def load_model():
    """Load the pickled Alzheimer's prediction model."""
    model_path = os.path.join(settings.BASE_DIR, 'ml', 'model_data', 'alzheimers_k-nearest_neighbors_model.pkl')
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_alzheimers(features):
    """
    Make predictions using the loaded model
    
    Args:
        features (list or numpy array): Features in the format expected by the model
        
    Returns:
        Prediction result from the model
    """
    model = load_model()
    # Convert features to numpy array if needed
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)
    return prediction[0]