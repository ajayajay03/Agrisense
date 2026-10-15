import requests

WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'

def get_weather(latitude, longitude):
    """Fetch current conditions and five daily forecasts without an API key."""
    params = {'latitude': latitude, 'longitude': longitude, 'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code', 'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code', 'timezone': 'auto', 'forecast_days': 5}
    response = requests.get(WEATHER_URL, params=params, timeout=12)
    response.raise_for_status()
    return response.json()

def weather_label(code):
    return {0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',45:'Fog',51:'Light drizzle',61:'Rain',71:'Snow',80:'Rain showers',95:'Thunderstorm'}.get(code, 'Variable conditions')
