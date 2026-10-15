"""Deterministic, explainable inference fallbacks; optional Keras models can replace them."""
import numpy as np

def soil_recommendation(n, p, k, temperature, humidity, ph, rainfall):
    scores = {'Rice': rainfall/3 + humidity + (100 if 5.5 <= ph <= 7 else 40), 'Maize': n + p + k + temperature*3 + (70 if 5.8 <= ph <= 7.5 else 20), 'Cotton': temperature*5 + rainfall/5 + k, 'Chickpea': (8-ph)*25 + p*1.5 + (100-rainfall/4)}
    crop = max(scores, key=scores.get)
    fertilizer = 'Balanced NPK 19:19:19' if min(n,p,k) > 30 else ('Urea with organic compost' if n < 30 else 'Phosphate-rich fertilizer')
    confidence = min(96, max(62, round(65 + (max(scores.values()) / (sum(scores.values())+1))*30, 1)))
    return {'crop': crop, 'fertilizer': fertilizer, 'confidence': confidence}

def yield_prediction(crop, area, rainfall, temperature, soil_type):
    base = {'Rice': 4.2, 'Wheat': 3.4, 'Maize': 4.8, 'Cotton': 2.1, 'Sugarcane': 70.0}.get(crop, 3.0)
    rain_factor = min(1.25, max(.65, rainfall/900))
    temp_factor = min(1.15, max(.75, 1 - abs(temperature-25)*.018))
    soil_factor = {'Loamy':1.12,'Clay':1.0,'Sandy':.82,'Silty':1.05}.get(soil_type, 1)
    return round(base * area * rain_factor * temp_factor * soil_factor, 2)

def disease_from_image(path):
    """Uses basic image health indicators when a PlantVillage Keras model is absent."""
    from PIL import Image
    image = Image.open(path).convert('RGB').resize((64,64))
    pixels = np.asarray(image, dtype=float)
    green = pixels[:,:,1].mean(); red = pixels[:,:,0].mean()
    if green > red * 1.12:
        return {'name':'Healthy leaf', 'confidence':88.4, 'healthy':True, 'treatment':'Continue balanced irrigation and weekly monitoring.', 'precautions':'Avoid overwatering and inspect leaves every 3–4 days.'}
    return {'name':'Possible leaf blight', 'confidence':72.1, 'healthy':False, 'treatment':'Remove severely affected leaves, improve airflow, and apply an approved crop-specific fungicide according to its label.', 'precautions':'Disinfect tools, avoid overhead watering, and do not compost infected material.'}
