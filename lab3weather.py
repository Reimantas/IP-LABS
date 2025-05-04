import requests
import json

# OpenWeatherMap API settings
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
API_KEY = "a6402a5fb81f1dde26f71adccec1b59f"  
WEB_URL = "https://openweathermap.org/city/"

def get_weather(city):
    try:
        # Step 1: Get coordinates from city name
        geo_params = {
            "q": city,
            "appid": API_KEY,
            "limit": 1
        }
        geo_response = requests.get(GEOCODING_URL, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return {
                "city": city,
                "error": "City not found. Please check the city name."
            }

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        city_name = geo_data[0]["name"]

        # Step 2: Get weather data from One Call API
        weather_params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",  # Use Celsius
            "exclude": "minutely,hourly,alerts"  # Only current and daily
        }
        weather_response = requests.get(ONECALL_URL, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        # Extract weather information
        current = weather_data["current"]
        result = {
            "city": city_name,
            "temperature": current["temp"],
            "feels_like": current["feels_like"],
            "humidity": current["humidity"],
            "description": current["weather"][0]["description"].capitalize(),
            "icon": f"http://openweathermap.org/img/wn/{current['weather'][0]['icon']}@2x.png",
            "web_url": f"{WEB_URL}{geo_data[0].get('geoname_id', '')}"  # URL for browser
        }
        return result
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"Error: Invalid API key. Please check your OpenWeatherMap API key.")
        else:
            print(f"Error fetching weather data: {e}")
        return {
            "city": city,
            "error": "Could not fetch weather data. Please try again."
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {
            "city": city,
            "error": "Could not fetch weather data. Please try again."
        }

def weather_search(city):
    return get_weather(city)