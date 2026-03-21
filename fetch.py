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
