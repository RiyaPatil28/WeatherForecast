import os
import logging
from flask import Flask, render_template, request, flash
from weather_service import WeatherService

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize weather service
weather_service = WeatherService()

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city = None
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        
        app.logger.debug(f"Form submitted with city: '{city}' (length: {len(city)})")
        
        if not city or len(city) < 2:
            flash('Please enter a valid city name.', 'error')
        else:
            try:
                weather_data = weather_service.get_weather(city)
                if not weather_data:
                    flash(f'Could not find weather data for "{city}". Please check the city name and try again.', 'error')
            except Exception as e:
                app.logger.error(f"Error fetching weather data: {str(e)}")
                flash('Sorry, there was an error fetching the weather data. Please try again later.', 'error')
    
    return render_template('index.html', weather_data=weather_data, city=city)



@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {str(error)}")
    flash('An internal error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
