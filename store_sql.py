"""
store_sql.py - Advanced database operations and migrations
"""

import sqlite3
from datetime import datetime
from config import DB_PATH

class WeatherDatabase:
    """Database manager for weather data"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def connect(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def initialize(self):
        """Initialize database with schema"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                date TEXT NOT NULL,
                temperature_2m_max REAL,
                precipitation_sum REAL,
                windspeed_10m_max REAL,
                relative_humidity_2m_max REAL,
                cloudcover REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS poems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                poem_text TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
    
    def insert_weather(self, location, date, temp, precip, wind, humidity, cloud):
        """Insert a weather record"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO weather_data 
            (location, date, temperature_2m_max, precipitation_sum, 
             windspeed_10m_max, relative_humidity_2m_max, cloudcover)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (location, date, temp, precip, wind, humidity, cloud))
        
        conn.commit()
        conn.close()
    
    def insert_poem(self, poem_text):
        """Insert a generated poem"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO poems (poem_text)
            VALUES (?)
        """, (poem_text,))
        
        conn.commit()
        conn.close()
    
    def get_latest_weather(self, location=None):
        """Get latest weather record(s)"""
        conn = self.connect()
        cursor = conn.cursor()
        
        if location:
            cursor.execute("""
                SELECT * FROM weather_data
                WHERE location = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (location,))
        else:
            cursor.execute("""
                SELECT * FROM weather_data
                ORDER BY created_at DESC
                LIMIT 3
            """)
        
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_latest_poem(self):
        """Get latest generated poem"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT poem_text, generated_at FROM poems
            ORDER BY generated_at DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        return result
    
    def clear_old_data(self, days=30):
        """Clear weather data older than N days"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM weather_data
            WHERE created_at < datetime('now', '-' || ? || ' days')
        """, (days,))
        
        deleted_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_rows

if __name__ == "__main__":
    db = WeatherDatabase()
    db.initialize()