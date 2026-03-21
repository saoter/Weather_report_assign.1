"""
Configuration file for Weather Pipeline
Edit this file with your locations and API keys
"""

# Your three locations (customize with YOUR actual coordinates)
LOCATIONS = [
    {
        "name": "Inaruwa",
        "lat": 27.1708,
        "lon": 87.2830
        # Inaruwa, Nepal
    },
    {
        "name": "Kathmandu",
        "lat": 27.7172,
        "lon": 85.3240
        # Kathmandu, Nepal - FIXED coordinates
    },
    {
        "name": "Aalborg",
        "lat": 57.0480,
        "lon": 9.9190
        # Aalborg, Denmark - FIXED coordinates
    }
]

# Weather variables to fetch
WEATHER_VARIABLES = [
    "temperature_2m_max",
    "precipitation_sum",
    "windspeed_10m_max",
    "relative_humidity_2m_max",
    "cloudcover"
]

# Database settings
DB_PATH = "data/weather.db"
DB_TABLE = "weather_data"

# API Settings
OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"
TIMEZONE = "auto"  # Use 'auto' to avoid timezone encoding issues

# Groq LLM Settings
GROQ_MODEL = "mixtral-8x7b-32768"
POEM_LANGUAGE_1 = "English"
POEM_LANGUAGE_2 = "Nepali"  # Changed for your locations
POEM_MAX_TOKENS = 512
POEM_TEMPERATURE = 0.8

# HTML Output settings
DOCS_PATH = "docs"
HTML_FILE = "docs/index.html"