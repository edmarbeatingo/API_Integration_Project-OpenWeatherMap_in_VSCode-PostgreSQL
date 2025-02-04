import requests
import json
from datetime import datetime

def get_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        weather_data = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_data
    else:
        return {'error': data.get('message', 'Failed to retrieve data')}

if __name__ == "__main__":
    city = "London"
    api_key = "a99000ba8dd160ef090516f7c455d498"
    weather_data = get_weather_data(city, api_key)
    print(json.dumps(weather_data, indent=4))