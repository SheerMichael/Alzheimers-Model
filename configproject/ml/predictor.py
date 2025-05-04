import numpy as np
from . import model

def predict(features):
    """
    Make predictions using the loaded Alzheimer's model
    
    Args:
        features (list or array): Input features for prediction
        
    Returns:
        The prediction result
    """
    if model is None:
        raise ValueError("Model is not loaded. Check logs for details.")
    
    # Convert features to numpy array and reshape for single prediction
    features_array = np.array(features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(features_array)
    
    # Get prediction probabilities if available
    try:
        probabilities = model.predict_proba(features_array)[0]
        return {
            'prediction': int(prediction[0]),
            'probability': float(max(probabilities))
        }
    except:
        # If predict_proba is not available
        return {
            'prediction': int(prediction[0])
        }