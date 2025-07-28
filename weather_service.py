import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        # Using Open-Meteo API - completely free, no API key required
        self.geocoding_url = 'https://geocoding-api.open-meteo.com/v1/search'
        self.weather_url = 'https://api.open-meteo.com/v1/forecast'
        logger.debug("WeatherService initialized with Open-Meteo API (no API key required)")
    
    def get_weather(self, city: str) -> Optional[Dict]:
        """
        Fetch weather data for a given city using Open-Meteo API
        
        Args:
            city (str): Name of the city
            
        Returns:
            Dict: Weather data or None if request fails
        """
        try:
            # Step 1: Get coordinates for the city using geocoding
            logger.debug(f"Fetching coordinates for city: {city}")
            geocoding_params = {
                'name': city,
                'count': 5,  # Get multiple results to find the best match
                'language': 'en',
                'format': 'json'
            }
            
            geocoding_response = requests.get(self.geocoding_url, params=geocoding_params, timeout=10)
            
            if geocoding_response.status_code != 200:
                logger.error(f"Geocoding request failed with status {geocoding_response.status_code}")
                raise Exception("Failed to get location coordinates")
            
            geocoding_data = geocoding_response.json()
            
            if not geocoding_data.get('results'):
                logger.warning(f"City not found: {city}")
                return None
            
            # Select the best location match
            # Prioritize locations with higher population or admin level
            results = geocoding_data['results']
            location = self._select_best_location(results, city)
            if not location:
                logger.warning(f"No suitable location found for: {city}")
                return None
                
            latitude = location['latitude']
            longitude = location['longitude']
            
            # Step 2: Get weather data using coordinates
            logger.debug(f"Fetching weather data for coordinates: {latitude}, {longitude}")
            weather_params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': 'true',
                'hourly': 'relative_humidity_2m,surface_pressure,visibility',
                'timezone': 'auto'
            }
            
            weather_response = requests.get(self.weather_url, params=weather_params, timeout=10)
            
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                return self._format_weather_data(weather_data, location)
            else:
                logger.error(f"Weather API request failed with status {weather_response.status_code}: {weather_response.text}")
                raise Exception(f"Weather API returned status code {weather_response.status_code}")
                
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
    
    def _format_weather_data(self, raw_data: Dict, location: Dict) -> Dict:
        """
        Format raw weather data from Open-Meteo API into a more usable structure
        
        Args:
            raw_data (Dict): Raw data from Open-Meteo API
            location (Dict): Location data from geocoding API
            
        Returns:
            Dict: Formatted weather data
        """
        try:
            current = raw_data.get('current_weather', {})
            hourly = raw_data.get('hourly', {})
            
            # Get current hour data for humidity and pressure
            current_humidity = 0
            current_pressure = 0
            current_visibility = 0
            
            if hourly:
                current_humidity = hourly.get('relative_humidity_2m', [0])[0]
                current_pressure = hourly.get('surface_pressure', [0])[0]
                current_visibility = hourly.get('visibility', [0])[0] / 1000 if hourly.get('visibility') else 0
            
            # Map weather codes to descriptions
            weather_code = current.get('weathercode', 0)
            description, main, icon = self._get_weather_description(weather_code)
            
            return {
                'city': location.get('name', 'Unknown'),
                'country': location.get('country_code', ''),
                'region': location.get('admin1', ''),  # State/Province
                'temperature': round(current.get('temperature', 0)),
                'feels_like': round(current.get('temperature', 0)),  # Open-Meteo doesn't provide feels_like in basic plan
                'description': description,
                'main': main,
                'humidity': round(current_humidity),
                'pressure': round(current_pressure),
                'wind_speed': round(current.get('windspeed', 0) / 3.6, 1),  # Convert km/h to m/s
                'wind_direction': current.get('winddirection', 0),
                'icon': icon,
                'visibility': round(current_visibility, 1)
            }
        except Exception as e:
            logger.error(f"Error formatting weather data: {str(e)}")
            raise Exception("Error processing weather data")
    
    def _get_weather_description(self, weather_code: int) -> tuple:
        """
        Map Open-Meteo weather codes to descriptions and icons
        
        Args:
            weather_code (int): Weather code from Open-Meteo API
            
        Returns:
            tuple: (description, main_type, icon_code)
        """
        weather_map = {
            0: ("Clear sky", "Clear", "01d"),
            1: ("Mainly clear", "Clear", "01d"),
            2: ("Partly cloudy", "Clouds", "02d"),
            3: ("Overcast", "Clouds", "03d"),
            45: ("Fog", "Mist", "50d"),
            48: ("Depositing rime fog", "Mist", "50d"),
            51: ("Light drizzle", "Drizzle", "09d"),
            53: ("Moderate drizzle", "Drizzle", "09d"),
            55: ("Dense drizzle", "Drizzle", "09d"),
            56: ("Light freezing drizzle", "Drizzle", "09d"),
            57: ("Dense freezing drizzle", "Drizzle", "09d"),
            61: ("Slight rain", "Rain", "10d"),
            63: ("Moderate rain", "Rain", "10d"),
            65: ("Heavy rain", "Rain", "10d"),
            66: ("Light freezing rain", "Rain", "10d"),
            67: ("Heavy freezing rain", "Rain", "10d"),
            71: ("Slight snow fall", "Snow", "13d"),
            73: ("Moderate snow fall", "Snow", "13d"),
            75: ("Heavy snow fall", "Snow", "13d"),
            77: ("Snow grains", "Snow", "13d"),
            80: ("Slight rain showers", "Rain", "09d"),
            81: ("Moderate rain showers", "Rain", "09d"),
            82: ("Violent rain showers", "Rain", "09d"),
            85: ("Slight snow showers", "Snow", "13d"),
            86: ("Heavy snow showers", "Snow", "13d"),
            95: ("Thunderstorm", "Thunderstorm", "11d"),
            96: ("Thunderstorm with slight hail", "Thunderstorm", "11d"),
            99: ("Thunderstorm with heavy hail", "Thunderstorm", "11d"),
        }
        
        return weather_map.get(weather_code, ("Unknown", "Unknown", "01d"))
    
    def _select_best_location(self, results: list, search_city: str) -> Optional[Dict]:
        """
        Select the best location from geocoding results
        Prioritize by population and admin level
        """
        if not results:
            return None
            
        # Sort by admin level and population (prefer cities over villages)
        def location_score(location):
            # Prefer locations with higher population
            population = location.get('population', 0)
            
            # Prefer cities over rural areas
            admin_level = location.get('admin1', '') # State/Province level
            feature_class = location.get('feature_class', '')
            
            score = population
            
            # Boost score for populated places
            if feature_class == 'P':  # Populated place
                score += 10000
                
            # Boost score if it has admin divisions (cities vs villages)
            if admin_level:
                score += 5000
                
            return score
        
        # Sort results by score and return the best match
        sorted_results = sorted(results, key=location_score, reverse=True)
        logger.debug(f"Selected location: {sorted_results[0].get('name')} in {sorted_results[0].get('admin1', '')}, {sorted_results[0].get('country_code', '')}")
        return sorted_results[0]
    
    def get_weather_icon_url(self, icon_code: str) -> str:
        """
        Get the URL for weather icon (using OpenWeatherMap icons for consistency)
        
        Args:
            icon_code (str): Icon code 
            
        Returns:
            str: URL to weather icon
        """
        return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
