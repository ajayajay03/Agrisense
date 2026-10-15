# Optional trained model

The application operates immediately with a deterministic leaf-health classifier, keeping the project runnable without downloading a multi-hundred-MB artifact. To enable a PlantVillage TensorFlow classifier, place a compatible trained Keras model at `models/plant_disease.keras`. `ml_models/model_manager.py` loads it safely when present. The expected model input is a 224×224 RGB image and its output class order must match the labels used by the training pipeline.
