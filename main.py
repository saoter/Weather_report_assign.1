"""
main.py - Main entry point for running the entire pipeline
Run this to execute: fetch -> generate poem -> create dashboard
"""

import subprocess
import sys

def run_pipeline():
    """Execute the complete pipeline"""
    print("=" * 60)
    print("🌤️  WEATHER POEM PIPELINE - STARTING")
    print("=" * 60)
    
    # Step 1: Fetch weather
    print("\n[1/3] Fetching weather data...")
    try:
        result = subprocess.run([sys.executable, "fetch.py"], check=True)
        print("✅ Weather fetching completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in fetch.py: {e}")
        return False
    
    # Step 2: Generate poem
    print("\n[2/3] Generating poem with Groq LLM...")
    try:
        result = subprocess.run([sys.executable, "generate_poem.py"], check=True)
        print("✅ Poem generation completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in generate_poem.py: {e}")
        return False
    
    # Step 3: Generate dashboard (optional)
    print("\n[3/3] Generating dashboard...")
    try:
        result = subprocess.run([sys.executable, "generate_dashboard.py"], check=True)
        print("✅ Dashboard generated!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Dashboard generation skipped: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📍 View your results:")
    print("   - Open: docs/index.html in your browser")
    print("   - Or push to GitHub and visit your GitHub Pages site")
    
    return True

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)