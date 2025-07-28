# Weather App

## Overview

This is a Flask-based weather application that provides real-time weather information for cities worldwide. The app integrates with the OpenWeatherMap API to fetch current weather data and presents it through a clean, responsive web interface using Bootstrap with a dark theme.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple three-tier architecture:

1. **Presentation Layer**: HTML templates with Bootstrap CSS framework
2. **Application Layer**: Flask web framework handling HTTP requests and business logic
3. **Data Layer**: External API integration with OpenWeatherMap

The architecture prioritizes simplicity and maintainability, making it easy to understand and extend. The separation of concerns is maintained through distinct modules for web handling (`app.py`) and weather service logic (`weather_service.py`).

## Key Components

### Web Application (`app.py`)
- **Purpose**: Main Flask application handling HTTP requests and responses
- **Key Features**: Route handling, error management, flash messaging system
- **Design Decision**: Uses Flask's built-in session management for flash messages, providing user feedback for API failures or validation errors

### Weather Service (`weather_service.py`)
- **Purpose**: Abstraction layer for OpenWeatherMap API integration
- **Key Features**: API request handling, data formatting, error handling with specific exception types
- **Design Decision**: Separates API logic from web logic for better testability and maintainability

### Frontend Templates
- **Base Template (`base.html`)**: Provides consistent layout with Bootstrap dark theme
- **Index Template (`index.html`)**: Main interface for city search and weather display
- **Design Decision**: Uses Bootstrap CDN with custom CSS for weather-specific styling

### Static Assets (`style.css`)
- **Purpose**: Custom styling for weather-specific components
- **Key Features**: Weather card styling, hover effects, responsive design enhancements

## Data Flow

1. **User Input**: User enters city name through web form
2. **Request Processing**: Flask route validates input and calls WeatherService
3. **API Integration**: WeatherService makes HTTP request to OpenWeatherMap API
4. **Data Transformation**: Raw API response is formatted into display-friendly structure
5. **Response Rendering**: Processed data is passed to template for HTML generation
6. **Error Handling**: API failures or invalid cities trigger flash messages

## External Dependencies

### Core Dependencies
- **Flask**: Web framework for handling HTTP requests and templating
- **Requests**: HTTP library for API communication with OpenWeatherMap

### Frontend Dependencies (CDN)
- **Bootstrap**: CSS framework for responsive design and component styling
- **Font Awesome**: Icon library for weather and UI icons

### API Integration
- **OpenWeatherMap API**: External service providing weather data
- **Authentication**: Requires API key stored in environment variable `OPENWEATHER_API_KEY`
- **Rate Limits**: Subject to OpenWeatherMap's usage limitations

## Deployment Strategy

### Environment Configuration
- **Development**: Uses Flask's built-in development server with debug mode
- **Environment Variables**: 
  - `OPENWEATHER_API_KEY`: Required for API access
  - `SESSION_SECRET`: Optional, falls back to development key

### Hosting Requirements
- **Python Environment**: Requires Python with Flask and requests packages
- **Network Access**: Needs outbound HTTPS access to api.openweathermap.org
- **Port Configuration**: Configured to run on port 5000 with host binding to 0.0.0.0

### Error Handling Strategy
- **API Failures**: Graceful degradation with user-friendly error messages
- **Network Issues**: Timeout and connection error handling with retry suggestions
- **Invalid Input**: Client-side and server-side validation with flash messaging
- **HTTP Errors**: Custom 404 and 500 error handlers

The deployment strategy prioritizes simplicity and reliability, with comprehensive error handling to ensure good user experience even when external services fail.