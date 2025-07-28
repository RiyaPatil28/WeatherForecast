# Weather App

## Overview

This is a Flask-based weather application that provides real-time weather information for cities worldwide. The app integrates with the Open-Meteo API (completely free, no API key required) to fetch current weather data and forecasts. The application features a modern glassmorphism UI design with smooth animations and a premium aesthetic.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a clean three-tier architecture optimized for simplicity and maintainability:

1. **Presentation Layer**: HTML templates with Bootstrap CSS framework and custom glassmorphism styling
2. **Application Layer**: Flask web framework handling HTTP requests, routing, and business logic
3. **Data Layer**: External API integration with Open-Meteo geocoding and weather APIs

The architecture prioritizes ease of understanding and extension while maintaining clear separation of concerns through distinct modules for web handling and weather data processing.

## Key Components

### Flask Application (`app.py`)
- **Purpose**: Main web application entry point handling HTTP requests and responses
- **Key Features**: Route handling, form processing, error management, flash messaging system
- **Design Decision**: Uses Flask's built-in session management for user feedback and comprehensive error handling for API failures

### Weather Service (`weather_service.py`)
- **Purpose**: Abstraction layer for Open-Meteo API integration and data processing
- **Key Features**: Geocoding for city coordinates, weather data fetching, response formatting, structured error handling
- **Design Decision**: Separates API logic from web logic for better testability, maintainability, and single responsibility principle

### Frontend Templates
- **Base Template (`base.html`)**: Consistent layout foundation with Bootstrap dark theme, navigation, and flash message handling
- **Index Template (`index.html`)**: Main user interface for city search and weather data display
- **Design Decision**: Uses Bootstrap CDN with extensive custom CSS for weather-specific glassmorphism styling

### Static Assets (`style.css`)
- **Purpose**: Premium glassmorphism design system with 3D effects and smooth animations
- **Key Features**: Multi-layered gradients, backdrop filters, hover effects, responsive design
- **Design Decision**: Modern aesthetic prioritizing visual appeal and user experience

## Data Flow

1. **User Input**: User enters city name through glassmorphism search form
2. **Request Processing**: Flask route validates input and delegates to WeatherService
3. **Geocoding**: WeatherService queries Open-Meteo geocoding API to get city coordinates
4. **Weather Fetching**: Service uses coordinates to fetch current weather from Open-Meteo weather API
5. **Data Transformation**: Raw API response is processed and formatted for template consumption
6. **Response Rendering**: Weather data is rendered through Jinja2 templates with error handling
7. **Error Management**: API failures, invalid cities, or network issues trigger user-friendly flash messages

## External Dependencies

### APIs
- **Open-Meteo Geocoding API**: Free geocoding service for converting city names to coordinates
- **Open-Meteo Weather API**: Free weather data service providing current conditions and forecasts
- **Design Decision**: Chosen for being completely free with no API key requirements, reliable, and well-documented

### Frontend Libraries
- **Bootstrap 5.3**: CSS framework for responsive layout and dark theme
- **Font Awesome 6.4**: Icon library for weather symbols and UI elements
- **Google Fonts**: Poppins and JetBrains Mono for modern typography

### Python Libraries
- **Flask**: Lightweight web framework for HTTP handling
- **requests**: HTTP client library for API communications
- **logging**: Built-in Python logging for debugging and monitoring

## Deployment Strategy

### Development Setup
- **Entry Point**: `main.py` runs the Flask development server
- **Configuration**: Environment-based secret key with fallback for development
- **Debug Mode**: Enabled for development with comprehensive logging

### Production Considerations
- **WSGI Compatibility**: Flask app can be deployed with any WSGI server (Gunicorn, uWSGI)
- **Environment Variables**: Secret key should be set via `SESSION_SECRET` environment variable
- **Static Assets**: CSS and potential future assets served through Flask's static file handling
- **Error Handling**: Comprehensive error pages and logging for production monitoring

### Scalability Design
- **Stateless Architecture**: No database dependencies, allowing horizontal scaling
- **API Rate Limiting**: Open-Meteo has generous limits, but caching could be added if needed
- **Session Management**: Minimal session usage only for flash messages, reducing memory footprint