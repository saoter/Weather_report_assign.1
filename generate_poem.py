"""
generate_poem.py - Generates bilingual poem using Groq LLM
Creates HTML output for GitHub Pages
"""

import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv  
from groq import Groq
from config import DB_PATH, GROQ_MODEL, POEM_LANGUAGE_1, POEM_LANGUAGE_2, POEM_MAX_TOKENS, POEM_TEMPERATURE, HTML_FILE

# Load environment variables from .env file
load_dotenv()  # ← Add this

def get_weather_from_db():
    """Fetch latest weather data from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT location, date, temperature_2m_max, temperature_2m_min, precipitation_sum, windspeed_10m_max, relative_humidity_2m_max
            FROM weather_data
            ORDER BY created_at DESC
            LIMIT 3
        """)
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return []

def make_poem_prompt(weather_data):
    """Create the prompt for the LLM"""
    info = ""
    for loc, date, temp_max, temp_min, prec, wind, humidity in weather_data:
        info += f"{loc} ({date}): Max {temp_max}°C, Min {temp_min}°C, {prec}mm rain, {wind}km/h wind, {humidity}% humidity\n"
    
    prompt = f"""Write a beautiful, creative poem comparing the weather in these 3 cities tomorrow.

{info}

The poem should be written in TWO languages:
1. First in {POEM_LANGUAGE_1}
2. Then in {POEM_LANGUAGE_2}

In the poem:
- Compare the weather conditions
- Highlight the temperature differences
- Mention precipitation and wind
- Suggest which location would be nicest to visit tomorrow
- Make it poetic and creative, not just factual

Format it clearly with language headers."""
    
    return prompt

def generate_groq_poem(prompt):
    """Generate poem using Groq API"""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print("❌ GROQ_API_KEY not found!")
            print("   Make sure you have .env file with: GROQ_API_KEY=gsk_...")
            raise ValueError("GROQ_API_KEY environment variable is not set")
        
        client = Groq(api_key=api_key)
        
        print("🤖 Generating poem with Groq LLM...")
        print(f"   Using model: {GROQ_MODEL}")
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a talented poetic assistant who creates beautiful, creative poems."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=POEM_MAX_TOKENS,
            temperature=POEM_TEMPERATURE,
        )
        
        poem = response.choices[0].message.content.strip()
        print("✅ Poem generated successfully!")
        return poem
        
    except Exception as e:
        print(f"❌ Error generating poem: {e}")
        return "Failed to generate poem. Please check your Groq API key."

def write_html(poem, weather_data):
    """Generate HTML output and save to docs/index.html"""
    
    os.makedirs("docs", exist_ok=True)
    
    # Format weather data for display
    weather_table_rows = ""
    for loc, date, temp_max, temp_min, prec, wind, humidity in weather_data:
        weather_table_rows += f"""
        <tr>
            <td><strong>{loc}</strong></td>
            <td>{temp_max}°C</td>
            <td>{temp_min}°C</td>
            <td>{prec}mm</td>
            <td>{wind}km/h</td>
            <td>{humidity}%</td>
        </tr>
        """
    
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌤️ Weather Poem</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
            animation: fadeIn 0.8s ease-in;
        }}
        
        header h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .poem-container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: slideUp 0.8s ease-out;
        }}
        
        .poem-container h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .poem-text {{
            font-size: 1.05em;
            line-height: 1.8;
            color: #333;
            white-space: pre-wrap;
            font-style: italic;
        }}
        
        .weather-container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            animation: slideUp 0.8s ease-out 0.2s backwards;
        }}
        
        .weather-container h3 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background: #f5f5f5;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌤️ Weather Poem for Tomorrow</h1>
            <p>Generated by AI and Real-Time Weather Data</p>
        </header>
        
        <div class="poem-container">
            <h2>✨ Today's Poetic Forecast</h2>
            <div class="poem-text">{poem}</div>
        </div>
        
        <div class="weather-container">
            <h3>📊 Weather Data</h3>
            <table>
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>Max Temp (°C)</th>
                        <th>Min Temp (°C)</th>
                        <th>Precipitation (mm)</th>
                        <th>Wind Speed (km/h)</th>
                        <th>Humidity (%)</th>
                    </tr>
                </thead>
                <tbody>
                    {weather_table_rows}
                </tbody>
            </table>
            <p><small>📅 Last updated: {updated_at} | Data from Open-Meteo API</small></p>
        </div>
        
        <div class="footer">
            <p>🤖 Automated Weather Pipeline with GitHub Actions | ⚡ Updates daily at 20:00 Copenhagen time</p>
        </div>
    </div>
</body>
</html>"""
    
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ HTML generated and saved to {HTML_FILE}")

if __name__ == "__main__":
    weather = get_weather_from_db()
    
    if not weather:
        print("❌ No weather data found. Run fetch.py first!")
    else:
        prompt = make_poem_prompt(weather)
        poem = generate_groq_poem(prompt)
        write_html(poem, weather)
        print("🎉 Pipeline complete!")