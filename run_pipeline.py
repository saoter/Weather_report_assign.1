"""
run_pipeline.py - Alternative simple runner for the pipeline
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch import fetch_weather, save_to_db
from generate_poem import get_weather_from_db, make_poem_prompt, generate_groq_poem, write_html

def main():
    print("🌤️ Starting Weather Pipeline...\n")
    
    # Step 1: Fetch weather
    print("Step 1: Fetching weather data...")
    weather_data = fetch_weather()
    
    if weather_data:
        save_to_db(weather_data)
    else:
        print("❌ Failed to fetch weather data")
        return
    
    # Step 2: Generate poem and HTML
    print("\nStep 2: Generating poem and HTML...")
    weather = get_weather_from_db()
    
    if weather:
        prompt = make_poem_prompt(weather)
        poem = generate_groq_poem(prompt)
        write_html(poem, weather)
        print("\n✅ Pipeline completed successfully!")
    else:
        print("❌ Failed to retrieve weather from database")

if __name__ == "__main__":
    main()