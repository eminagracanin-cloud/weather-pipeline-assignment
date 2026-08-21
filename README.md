# 🌦️ Automated Weather Data Pipeline

An automated end-to-end data pipeline that collects real-time weather data, persists it in a local database, uses an LLM to generate weather-inspired content, and automatically publishes the results to a live website.

The project demonstrates how **data ingestion, storage, AI integration, workflow automation, and deployment** can be combined into a fully automated pipeline.

---

## 🔗 Live Project

🌐 **Live Website:**  
https://eminagracanin-cloud.github.io/weather-data-pipeline/

💻 **GitHub Repository:**  
https://github.com/eminagracanin-cloud/weather-data-pipeline

---

## 🏗️ Architecture

```text
Open-Meteo API
      │
      ▼
 Python Ingestion
      │
      ▼
SQLite Database
      │
      ▼
   Groq LLM
      │
      ▼
Website Generation
      │
      ▼
 GitHub Pages

      ▲
      │
GitHub Actions
Daily Automation
```

---

## ⚙️ How It Works

The pipeline automatically:

1. **Fetches weather data** from the Open-Meteo API for multiple locations.
2. **Processes and stores the data** in a SQLite database.
3. **Uses an LLM** through the Groq API to generate bilingual weather-inspired content based on the latest conditions.
4. **Updates the website** with newly generated results.
5. **Deploys the updated output** through GitHub Pages.
6. **Runs automatically** using a scheduled GitHub Actions workflow.

This allows the entire workflow to execute without manual intervention.

---

## 📍 Locations

The pipeline currently processes weather data for:

- 🇧🇦 Bosnia and Herzegovina
- 🇩🇰 Copenhagen
- 🇩🇰 Aalborg

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Pipeline logic and data processing |
| **SQLite** | Local data persistence |
| **Open-Meteo API** | Weather data source |
| **Groq API** | LLM-powered content generation |
| **GitHub Actions** | Workflow scheduling and automation |
| **GitHub Pages** | Deployment and hosting |

---

## 🤖 Automation

The workflow is scheduled through **GitHub Actions** and runs automatically every day.

Each execution retrieves fresh weather data, processes the latest observations, generates updated content, and publishes the result to the website.

---

## 📁 Project Structure

```text
weather-data-pipeline/
│
├── .github/
│   └── workflows/       # Automated GitHub Actions workflow
│
├── docs/                # Generated GitHub Pages website
│
├── fetch.py             # Main pipeline logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🎯 What This Project Demonstrates

This project demonstrates practical experience with:

- Building automated **data pipelines**
- Working with external **REST APIs**
- Data ingestion and persistence
- Python-based workflow development
- Integrating **LLMs into data workflows**
- Scheduled automation with **GitHub Actions**
- Automated website generation
- Continuous deployment with **GitHub Pages**
- Designing an end-to-end workflow from data source to deployed output

---

## 💡 Key Takeaway

Rather than being a standalone analysis or notebook, this project is designed as an **automated system**: data is collected, processed, transformed with an LLM, and published without requiring manual execution.
