import os
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
        logger.debug(f"WeatherService initialized with API key length: {len(self.api_key) if self.api_key else 0}")
    
    def get_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch weather data for a given city from OpenWeatherMap API
        
        Args:
            city (str): Name of the city
            
        Returns:
            Dict: Weather data or None if request fails
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            logger.debug(f"Fetching weather data for city: {city}")
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_data(data)
            elif response.status_code == 404:
                logger.warning(f"City not found: {city}")
                return None
            elif response.status_code == 401:
                logger.error(f"Invalid API key: {response.text}")
                raise Exception("Invalid API key. Please check your OpenWeatherMap API key is correct and active.")
            else:
                logger.error(f"API request failed with status {response.status_code}: {response.text}")
                raise Exception(f"Weather API returned status code {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout while fetching weather data")
            raise Exception("Request timeout. Please try again.")
        except requests.exceptions.ConnectionError:
            logger.error("Connection error while fetching weather data")
            raise Exception("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            raise Exception("Network error occurred. Please try again.")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    def _format_weather_data(self, raw_data: Dict) -> Dict:
        """
        Format raw weather data from API into a more usable structure
        
        Args:
            raw_data (Dict): Raw data from OpenWeatherMap API
            
        Returns:
            Dict: Formatted weather data
        """
        try:
            main = raw_data.get('main', {})
            weather = raw_data.get('weather', [{}])[0]
            wind = raw_data.get('wind', {})
            sys = raw_data.get('sys', {})
            
            return {
                'city': raw_data.get('name', 'Unknown'),
                'country': sys.get('country', ''),
                'temperature': round(main.get('temp', 0)),
                'feels_like': round(main.get('feels_like', 0)),
                'description': weather.get('description', '').title(),
                'main': weather.get('main', ''),
                'humidity': main.get('humidity', 0),
                'pressure': main.get('pressure', 0),
                'wind_speed': wind.get('speed', 0),
                'wind_direction': wind.get('deg', 0),
                'icon': weather.get('icon', '01d'),
                'visibility': raw_data.get('visibility', 0) / 1000 if raw_data.get('visibility') else 0  # Convert to km
            }
        except Exception as e:
            logger.error(f"Error formatting weather data: {str(e)}")
            raise Exception("Error processing weather data")
    
    def get_weather_icon_url(self, icon_code: str) -> str:
        """
        Get the URL for weather icon from OpenWeatherMap
        
        Args:
            icon_code (str): Icon code from API response
            
        Returns:
            str: URL to weather icon
        """
        return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
