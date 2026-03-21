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

# Optional: clear old rows so each run shows fresh data
cursor.execute("DELETE FROM weather")

# Fetch weather data
for name, (lat, lon) in locations.items():
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=temperature_2m_max,precipitation_sum,windspeed_10m_max&"
        f"timezone=auto"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        date = data["daily"]["time"][0]
        temperature = data["daily"]["temperature_2m_max"][0]
        precipitation = data["daily"]["precipitation_sum"][0]
        windspeed = data["daily"]["windspeed_10m_max"][0]

        cursor.execute("""
        INSERT INTO weather VALUES (?, ?, ?, ?, ?)
        """, (name, date, temperature, windspeed, precipitation))

    except Exception as e:
        print(f"Error fetching weather for {name}: {e}")

conn.commit()

# Read weather data for poem
cursor.execute("SELECT * FROM weather")
rows = cursor.fetchall()
conn.close()

# Generate poem with Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

weather_text = ""
for row in rows:
    weather_text += (
        f"{row[0]}: temperature {row[2]}°C, "
        f"wind speed {row[3]} km/h, "
        f"precipitation {row[4]} mm.\n"
    )

prompt = f"""
Write a short, creative weather poem comparing these three locations:

{weather_text}

Requirements:
- Compare Bosnia, Copenhagen, and Aalborg
- Say where it would be nicest to be tomorrow
- Write in two languages: English and Bosnian
- Keep it elegant and easy to read
- Format it with a clear English section and a clear Bosnian section
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

poem = response.choices[0].message.content

# Save styled HTML page
html_content = f"""
<html>
<head>
    <title>Weather Poem</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #74ebd5, #ACB6E5);
            color: #333;
            text-align: center;
            padding: 40px;
        }}

        h1 {{
            font-size: 40px;
            margin-bottom: 20px;
        }}

        .flag {{
            font-size: 40px;
            margin-bottom: 20px;
        }}

        .poem-box {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 850px;
            margin: auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: left;
            white-space: pre-wrap;
            line-height: 1.7;
        }}
    </style>
</head>
<body>
    <h1>🌦️ Weather Poem 🌦️</h1>
    <div class="flag">🇧🇦 Bosnia &nbsp;&nbsp; 🇩🇰 Denmark</div>
    <div class="poem-box">{poem}</div>
</body>
</html>
"""

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Weather data stored successfully.")
print("Poem generated and saved to website.")
