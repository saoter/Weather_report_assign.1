"""
query.py - Query and inspect the weather database
"""

import sqlite3
from tabulate import tabulate
from config import DB_PATH

def view_all_weather():
    """Display all weather records"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT location, date, temperature_2m_max, precipitation_sum, 
                   windspeed_10m_max, relative_humidity_2m_max, cloudcover, created_at
            FROM weather_data
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            headers = ["Location", "Date", "Temp (°C)", "Rain (mm)", "Wind (km/h)", "Humidity (%)", "Cloud (%)", "Created At"]
            print("\n📊 All Weather Records:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No weather records found in database.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def view_latest_weather():
    """Display latest weather for each location"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT location, date, temperature_2m_max, precipitation_sum, 
                   windspeed_10m_max, relative_humidity_2m_max, cloudcover
            FROM weather_data
            WHERE (location, created_at) IN (
                SELECT location, MAX(created_at) 
                FROM weather_data 
                GROUP BY location
            )
            ORDER BY location
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            headers = ["Location", "Date", "Temp (°C)", "Rain (mm)", "Wind (km/h)", "Humidity (%)", "Cloud (%)"]
            print("\n📊 Latest Weather for Each Location:")
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No weather records found in database.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def database_stats():
    """Show database statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT location) FROM weather_data")
        total_locations = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT DATE(date)) FROM weather_data")
        total_dates = cursor.fetchone()[0]
        
        conn.close()
        
        print("\n📈 Database Statistics:")
        print(f"   Total Records: {total_records}")
        print(f"   Unique Locations: {total_locations}")
        print(f"   Unique Dates: {total_dates}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("🌤️ WEATHER DATABASE QUERY TOOL")
    print("=" * 80)
    
    view_latest_weather()
    view_all_weather()
    database_stats()























































































































































































































































































































































































    