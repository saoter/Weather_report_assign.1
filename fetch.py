"""
fetch.py - Fetches weather data from Open-Meteo API with error handling
"""

import requests
import sqlite3
import datetime
import time
from config import LOCATIONS, WEATHER_VARIABLES, DB_PATH

# Timeout settings
REQUEST_TIMEOUT = 10  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds

def get_api_url(lat, lon):
    """Build the Open-Meteo API URL"""
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    variables = ",".join(WEATHER_VARIABLES)
    
    # IMPORTANT: Use timezone=auto to avoid encoding issues
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&daily={variables}"
        f"&start_date={tomorrow}"
        f"&end_date={tomorrow}"
        f"&timezone=auto"  # Changed from Europe/Copenhagen to auto
    )
    
    return url

def fetch_weather_with_retry(location, lat, lon, attempts=RETRY_ATTEMPTS):
    """Fetch weather with retry logic"""
    
    for attempt in range(1, attempts + 1):
        try:
            url = get_api_url(lat, lon)
            
            print(f"  🔄 Fetching {location} (attempt {attempt}/{attempts})...")
            
            # Add timeout to prevent hanging
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            
            # Check for HTTP errors
            response.raise_for_status()
            
            data = response.json()
            daily_data = data["daily"]
            
            record = {
                "location": location,
                "date": daily_data["time"][0],
                "temperature_2m_max": daily_data["temperature_2m_max"][0],
                "precipitation_sum": daily_data["precipitation_sum"][0],
                "windspeed_10m_max": daily_data["windspeed_10m_max"][0],
                "relative_humidity_2m_max": daily_data["relative_humidity_2m_max"][0],
                "cloudcover": daily_data["cloudcover"][0],
            }
            
            print(f"  ✅ {location}: {record['temperature_2m_max']}°C")
            return record
            
        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout on attempt {attempt}. Retrying in {RETRY_DELAY}s...")
            if attempt < attempts:
                time.sleep(RETRY_DELAY)
            continue
            
        except requests.exceptions.HTTPError as e:
            print(f"  ❌ HTTP Error {e.response.status_code}: {e.response.reason}")
            print(f"     Response: {e.response.text[:200]}")
            break
            
        except requests.exceptions.ConnectionError as e:
            print(f"  ❌ Connection Error: {str(e)[:100]}")
            if attempt < attempts:
                print(f"     Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            continue
            
        except Exception as e:
            print(f"  ❌ Unexpected error: {str(e)[:100]}")
            break
    
    print(f"  ❌ Failed to fetch {location} after {attempts} attempts")
    return None

def fetch_weather():
    """Fetch weather data for all locations"""
    results = []
    
    print("🌤️ Fetching weather data from Open-Meteo API...")
    print(f"   Timeout: {REQUEST_TIMEOUT}s | Retries: {RETRY_ATTEMPTS}\n")
    
    for loc in LOCATIONS:
        weather_record = fetch_weather_with_retry(
            location=loc["name"],
            lat=loc["lat"],
            lon=loc["lon"],
            attempts=RETRY_ATTEMPTS
        )
        
        if weather_record:
            results.append(weather_record)
        
        # Small delay between requests to avoid rate limiting
        time.sleep(0.5)
    
    return results

def save_to_db(weather_data):
    """Store weather data in SQLite database"""
    import os
    
    if not weather_data:
        print("⚠️ No weather data to save!")
        return
    
    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    try:
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
        print(f"\n✅ {len(weather_data)} weather record(s) saved to database!")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    weather_data = fetch_weather()
    print("=" * 60)
    
    if weather_data:
        save_to_db(weather_data)
    else:
        print("\n⚠️ No weather data was successfully fetched!")