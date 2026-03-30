# this repo is awesome
# 🌤️ Automated Weather Poem Pipeline



An end-to-end MLOps project that combines APIs, databases, LLMs, and automation to create a daily weather poetry pipeline.

## 📋 Overview

This project fetches real-time weather forecasts for 3 locations, stores them in a SQLite database, generates creative bilingual poems using Groq LLM, and publishes results via GitHub Pages.

### Features

✅ **Open-Meteo API Integration** - Free weather data (no API key required)  
✅ **SQLite Database** - Persistent weather storage  
✅ **Groq LLM** - Bilingual poem generation (English + your language)  
✅ **GitHub Actions** - Daily automation at 20:00 Copenhagen time  
✅ **GitHub Pages** - Auto-published HTML results  
✅ **Analytics Dashboard** - Optional weather analytics  

## 📁 Project Structure

```
weather-pipeline/
├── .github/workflows/
│   └── pipeline.yml              # GitHub Actions workflow
├── data/
│   └── weather.db               # SQLite database (auto-created)
├── docs/
│   ├── index.html               # Main webpage (auto-generated)
│   └── dashboard.html           # Analytics dashboard (optional)
├── config.py                    # Configuration file
├── fetch.py                     # Weather data collection
├── generate_poem.py             # LLM poem generation
├── generate_dashboard.py        # Analytics dashboard
├── main.py                      # Pipeline orchestrator
├── run_pipeline.py              # Alternative runner
├── query.py                     # Database query tool
├── store_sql.py                 # Database operations
├── store_vector.py              # Vector embeddings (optional)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/weather-pipeline
cd weather-pipeline
pip install -r requirements.txt
```

### 2. Customize Locations

Edit `config.py` and update:
```python
LOCATIONS = [
    {"name": "Your Birthplace", "lat": YOUR_LAT, "lon": YOUR_LON},
    {"name": "Previous Home", "lat": YOUR_LAT, "lon": YOUR_LON},
    {"name": "Aalborg", "lat": 57.048, "lon": 9.919}
]
```

Find coordinates at: https://www.google.com/maps

### 3. Get Groq API Key

1. Visit: https://console.groq.com
2. Sign up (free)
3. Copy your API key

### 4. Add GitHub Secret

1. Go to your repo → Settings → Secrets and variables → Actions
2. Create new secret: `GROQ_API_KEY` = your key

### 5. Enable GitHub Pages

1. Settings → Pages
2. Source: `/docs` directory
3. Save

### 6. Run Locally (Optional)

```bash
python main.py
# Or
python run_pipeline.py
```

### 7. Push to GitHub

```bash
git add .
git commit -m "Initial setup"
git push
```

## 📊 Using the Tools

### View Weather Data

```bash
python query.py
```

Shows all weather records and statistics.

### Generate Dashboard

```bash
python generate_dashboard.py
```

Creates analytics dashboard at `docs/dashboard.html`.

### Manual Pipeline Run

```bash
python main.py
```

Executes the entire pipeline locally.

## ⏰ Automation Schedule

The GitHub Actions workflow runs automatically:
- **Time**: 20:00 Copenhagen time (19:00 UTC)
- **Frequency**: Every day
- **Trigger**: Can also be manually triggered

Edit `.github/workflows/pipeline.yml` to change the schedule:
```yaml
schedule:
  - cron: '0 19 * * *'  # Change this for different times
```

## 🎨 Customization

### Change Poem Languages

Edit `config.py`:
```python
POEM_LANGUAGE_1 = "English"
POEM_LANGUAGE_2 = "Hindi"  # Change to your language
```

### Add More Weather Variables

Edit `config.py`:
```python
WEATHER_VARIABLES = [
    "temperature_2m_max",
    "precipitation_sum",
    "windspeed_10m_max",
    "relative_humidity_2m_max",
    "cloudcover",
    # Add more: uv_index_max, snowfall_sum, etc.
]
```

### Change Database Location

Edit `config.py`:
```python
DB_PATH = "data/weather.db"  # Change path here
```

## 📚 API Documentation

### Open-Meteo API

- **Docs**: https://open-meteo.com/en/docs
- **No registration needed**
- **Free tier**: Unlimited calls
- **Rate limit**: 10,000 calls/day

Available variables:
- `temperature_2m_max` / `temperature_2m_min`
- `precipitation_sum`
- `windspeed_10m_max`
- `relative_humidity_2m_max`
- `cloudcover`
- `uv_index_max`
- `snowfall_sum`

### Groq API

- **Docs**: https://console.groq.com/docs
- **Free tier**: Sufficient for daily use
- **Model**: `mixtral-8x7b-32768`

## 🔧 Troubleshooting

### "No API key provided"
→ Add `GROQ_API_KEY` secret to GitHub Settings

### "Database error"
→ Delete `data/weather.db` and rerun

### "Workflow doesn't run"
→ Check `.github/workflows/pipeline.yml` syntax
→ Verify GitHub Actions is enabled

### "Poem not generating"
→ Check Groq API key is valid
→ Check internet connection
→ View GitHub Actions logs

## 📈 Next Steps

- **Add more locations** for wider coverage
- **Implement notifications** (email, Slack, etc.)
- **Create charts** for historical weather trends
- **Add machine learning** to predict best locations
- **Deploy Telegram bot** to share daily poems

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Feel free to fork, enhance, and share improvements!

---

**Made with ❤️ for the automated weather poetry pipeline**
