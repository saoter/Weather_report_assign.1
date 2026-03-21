"""
fetch.py - Fetches weather data from Open-Meteo API
Stores data in SQLite database
"""

import requests
import sqlite3
import datetime
from config import LOCATIONS, WEATHER_VARIABLES, DB_PATH, OPEN_METEO_API, TIMEZONE

def get_api_url(lat, lon):
    """Build the Open-Meteo API URL for tomorrow's forecast"""
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    variables = ",".join(WEATHER_VARIABLES)
    
    url = (
        f"{OPEN_METEO_API}"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&daily={variables}"
        f"&start_date={tomorrow}"
        f"&end_date={tomorrow}"
        f"&timezone={TIMEZONE}"
    )
    return url

def fetch_weather():
    """Fetch weather data from Open-Meteo API for all locations"""
    results = []
    
    print("🌤️ Fetching weather data from Open-Meteo API...")
    
    for loc in LOCATIONS:
        url = get_api_url(loc["lat"], loc["lon"])
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            daily_data = data["daily"]
            
            weather_record = {
                "location": loc["name"],
                "date": daily_data["time"][0],
                "temperature_2m_max": daily_data["temperature_2m_max"][0],
                "precipitation_sum": daily_data["precipitation_sum"][0],
                "windspeed_10m_max": daily_data["windspeed_10m_max"][0],
                "relative_humidity_2m_max": daily_data["relative_humidity_2m_max"][0],
                "cloudcover": daily_data["cloudcover"][0],
            }
            results.append(weather_record)
            print(f"  ✅ {loc['name']}: {weather_record['temperature_2m_max']}°C")
            
        except Exception as e:
            print(f"  ❌ Error fetching {loc['name']}: {e}")
    
    return results

def save_to_db(weather_data):
    """Store weather data in SQLite database"""
    import os
    
    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            date TEXT,
            temperature_2m_max REAL,
            precipitation_sum REAL,
            windspeed_10m_max REAL,
            relative_humidity_2m_max REAL,
            cloudcover REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert new data
    for record in weather_data:
        cursor.execute(
            """INSERT INTO weather_data 
               (location, date, temperature_2m_max, precipitation_sum, windspeed_10m_max, relative_humidity_2m_max, cloudcover)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                record["location"],
                record["date"],
                record["temperature_2m_max"],
                record["precipitation_sum"],
                record["windspeed_10m_max"],
                record["relative_humidity_2m_max"],
                record["cloudcover"]
            )
        )
    
    conn.commit()
    conn.close()
    print("✅ Weather data saved to database!")

if __name__ == "__main__":
    weather_data = fetch_weather()
    if weather_data:
        save_to_db(weather_data)