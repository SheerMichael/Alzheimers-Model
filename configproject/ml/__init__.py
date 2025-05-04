import os
import pickle
from django.conf import settings

# Compute the absolute path to your pickle - fixing the path
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml', 'model_data', 'alzheimers_k-nearest_neighbors_model.pkl')

# Load once when Django starts
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print(f"Model successfully loaded from {MODEL_PATH}")
except FileNotFoundError:
    model = None
    # Log a warning so you know if it's missing
    import logging
    logging.getLogger(__name__).warning(f"Pickle not found at {MODEL_PATH}")
except Exception as e:
    model = None
    import logging
    logging.getLogger(__name__).error(f"Error loading model: {str(e)}")