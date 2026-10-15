"""Optional TensorFlow model loader for a PlantVillage-compatible .keras file."""
from pathlib import Path
MODEL_PATH=Path(__file__).resolve().parents[1] / 'models' / 'plant_disease.keras'
def load_plant_model():
    """Load a locally supplied trained Keras model; returns None for reliable heuristic fallback."""
    if not MODEL_PATH.exists(): return None
    import tensorflow as tf
    return tf.keras.models.load_model(MODEL_PATH)
