from groq import Groq
import os

import requests
import sqlite3

# Locations (latitude, longitude)
locations = {
    "Bosnia": (44.2, 17.9),
    "Copenhagen": (55.7, 12.6),
    "Aalborg": (57.0, 9.9)
}

# Create database
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    location TEXT,
    date TEXT,
    temperature REAL,
    windspeed REAL,
    precipitation REAL
)
""")

# Fetch weather data
for name, (lat, lon) in locations.items():
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=temperature_2m_max,precipitation_sum,windspeed_10m_max&"
        f"timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    date = data["daily"]["time"][0]
    temperature = data["daily"]["temperature_2m_max"][0]
    precipitation = data["daily"]["precipitation_sum"][0]
    windspeed = data["daily"]["windspeed_10m_max"][0]

    cursor.execute("""
    INSERT INTO weather VALUES (?, ?, ?, ?, ?)
    """, (name, date, temperature, windspeed, precipitation))

conn.commit()
conn.close()

print("Weather data stored successfully.")

# ── Generate poem with Groq ─────────────────────────────

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Get weather data
cursor = sqlite3.connect("weather.db").cursor()
cursor.execute("SELECT * FROM weather")
rows = cursor.fetchall()

# Create prompt
weather_text = ""
for row in rows:
    weather_text += f"{row[0]}: {row[2]}°C, wind {row[3]}, rain {row[4]}\n"

prompt = f"""
Write a short poetic comparison of the weather in these locations:

{weather_text}

Requirements:
- Compare the three places
- Say where it is nicest to be tomorrow
- Write in English and Bosnian
"""

# Call Groq
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

poem = response.choices[0].message.content

# Save poem to HTML
with open("docs/index.html", "w") as f:
    f.write(f"<html><body><h1>Weather Poem</h1><pre>{poem}</pre></body></html>")

print("\nPoem generated and saved to website.")
