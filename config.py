"""
Configuration file for Weather Pipeline
Edit this file with your locations and API keys
"""

# Your three locations
LOCATIONS = [
    {
        "name": "Inaruwa",
        "lat": 27.1708,
        "lon": 87.2830
    },
    {
        "name": "Kathmandu",
        "lat": 27.7172,
        "lon": 85.3240
    },
    {
        "name": "Aalborg",
        "lat": 57.0480,
        "lon": 9.9190
    }
]

# ✅ VALID weather variables for Open-Meteo DAILY forecast
# Removed: cloudcover (not available for daily)
WEATHER_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "windspeed_10m_max",
    "relative_humidity_2m_max"
]

# Database settings
DB_PATH = "data/weather.db"
DB_TABLE = "weather_data"

# API Settings
OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"
TIMEZONE = "auto"

# Groq LLM Settings
GROQ_MODEL = "mixtral-8x7b-32768"
POEM_LANGUAGE_1 = "English"
POEM_LANGUAGE_2 = "Nepali"
POEM_MAX_TOKENS = 512
POEM_TEMPERATURE = 0.8

# HTML Output settings
DOCS_PATH = "docs"
HTML_FILE = "docs/index.html"