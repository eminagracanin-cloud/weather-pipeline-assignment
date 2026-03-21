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

# Clear old rows
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

# Read weather data
cursor.execute("SELECT * FROM weather")
rows = cursor.fetchall()
conn.close()

# Prepare weather display
weather_text = ""
weather_display = ""

for row in rows:
    location, date, temp, wind, rain = row

    if rain > 2:
        emoji = "🌧️"
    elif wind > 20:
        emoji = "🌬️"
    else:
        emoji = "☀️"

    weather_text += (
        f"{location}: temperature {temp}°C, "
        f"wind speed {wind} km/h, "
        f"precipitation {rain} mm.\n"
    )

    flag = "🇧🇦" if location == "Bosnia" else "🇩🇰"
    weather_display += f'<div class="weather-item">{flag} {location}: {temp}°C {emoji}</div>'

# Generate poem with Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

prompt = f"""
Write a short weather poem based on these locations:

{weather_text}

Rules:
- Compare Bosnia, Copenhagen, and Aalborg
- Say where it would be nicest to be tomorrow
- Write ONLY in these two sections and in this exact format
- Do NOT add any introduction
- Do NOT add any explanation
- Do NOT add any translation note
- Do NOT repeat the English text
- Do NOT include markdown symbols like **

Use exactly this structure:

English:
<only the English poem>

Bosanski:
<samo pjesma na bosanskom>
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

poem = response.choices[0].message.content.strip()

# Split poem into English and Bosnian sections
poem_en = poem
poem_bs = ""

if "Bosanski:" in poem:
    parts = poem.split("Bosanski:", 1)
    poem_en = parts[0].replace("English:", "").strip()
    poem_bs = parts[1].strip()

    if "Translated from Bosnian:" in poem_bs:
        poem_bs = poem_bs.split("Translated from Bosnian:")[0].strip()
else:
    poem_en = poem.replace("English:", "").strip()

# Save styled HTML page
html_content = f"""
<html>
<head>
    <title>Weather Poem</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(to right, #74ebd5, #ACB6E5);
            color: #333;
            text-align: center;
            padding: 40px;
        }}

        h1 {{
            font-size: 42px;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 20px;
            margin-bottom: 25px;
        }}

        .flag {{
            font-size: 40px;
            margin-bottom: 25px;
        }}

        .container {{
            max-width: 900px;
            margin: auto;
        }}

        .weather-box {{
            background: rgba(255,255,255,0.9);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            font-size: 18px;
        }}

        .weather-item {{
            margin: 8px 0;
            font-weight: bold;
        }}

        .poem-box {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            line-height: 1.8;
        }}

        .section-title {{
            font-size: 22px;
            margin-top: 20px;
            margin-bottom: 10px;
            font-weight: bold;
        }}

        .poem-text {{
            white-space: pre-line;
        }}

        hr {{
            margin: 25px 0;
            border: none;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌦️ Weather Poem 🌦️</h1>
        <div class="subtitle">Comparing Bosnia & Denmark</div>
        <div class="flag">🇧🇦 🇩🇰</div>

        <div class="weather-box">
            <h2>🌡️ Weather Tomorrow</h2>
            {weather_display}
        </div>

        <div class="poem-box">
            <div class="section-title">🇬🇧 English</div>
            <div class="poem-text">{poem_en}</div>

            <hr>

            <div class="section-title">🇧🇦 Bosanski</div>
            <div class="poem-text">{poem_bs}</div>
        </div>
    </div>
</body>
</html>
"""

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Weather data stored successfully.")
print("Poem generated and saved to website.")
