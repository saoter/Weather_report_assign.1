"""
generate_dashboard.py - Optional: Generate an analytics dashboard
"""

import sqlite3
from config import DB_PATH
from datetime import datetime
import json

def generate_dashboard():
    """Generate analytics dashboard"""
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        total_records = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT location, AVG(temperature_2m_max), MAX(temperature_2m_max), MIN(temperature_2m_max)
            FROM weather_data
            GROUP BY location
        """)
        temp_stats = cursor.fetchall()
        
        cursor.execute("""
            SELECT location, SUM(precipitation_sum)
            FROM weather_data
            GROUP BY location
        """)
        precip_stats = cursor.fetchall()
        
        conn.close()
        
        # Generate HTML dashboard
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Weather Analytics Dashboard</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .dashboard {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        .stats {{
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>📊 Weather Analytics Dashboard</h1>
    
    <div class="dashboard">
        <div class="card">
            <h2>Temperature Statistics</h2>
            <table>
                <tr><th>Location</th><th>Avg (°C)</th><th>Max (°C)</th><th>Min (°C)</th></tr>
                {"".join([f"<tr><td>{loc}</td><td>{avg:.1f}</td><td>{max_t:.1f}</td><td>{min_t:.1f}</td></tr>" 
                         for loc, avg, max_t, min_t in temp_stats])}
            </table>
        </div>
        
        <div class="card">
            <h2>Precipitation Summary</h2>
            <table>
                <tr><th>Location</th><th>Total (mm)</th></tr>
                {"".join([f"<tr><td>{loc}</td><td>{total:.1f}</td></tr>" 
                         for loc, total in precip_stats])}
            </table>
        </div>
    </div>
    
    <div class="card" style="margin-top: 20px;">
        <h2>Database Stats</h2>
        <p class="stats">Total Records: {total_records}</p>
        <p class="stats">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>"""
        
        with open("docs/dashboard.html", "w") as f:
            f.write(html)
        
        print("✅ Dashboard generated: docs/dashboard.html")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_dashboard()