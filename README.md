# 📊 AI-Powered Social Media Sentiment & EDA Dashboard

A full-stack data analysis pipeline that performs Exploratory Data Analysis (EDA) on social media datasets, categorizes text sentiment using Large Language Models (LLMs), and serves the insights through a REST API to a modern React dashboard.

## 🚀 Overview

This project tackles the complexities of unstructured social media data (like tweets) by combining traditional data science techniques with modern Generative AI. It is broken down into four distinct modules:

1. **AI Sentiment Pipeline:** Uses the Google Gemini 2.5 Flash API to contextually understand slang, sarcasm, and nuance.
2. **Exploratory Data Analysis (EDA):** Analyzes metadata (dates, locations, active users) to uncover broader trends.
3. **Backend API:** A Flask server that bridges the Python analysis with the frontend.
4. **Interactive Dashboard:** A React web application for clean, real-time data visualization.

---

## 📂 Project Architecture & Files

### 1. `main.py` (AI Sentiment Analysis)
The core data processing script. 
* Loads raw CSV data using `pandas`.
* Cleans the text data (e.g., stripping URLs using RegEx) to prevent API errors.
* Iterates through the data and securely calls the **Google Gemini API** to classify sentiment as `Positive`, `Negative`, or `Neutral`.
* Implements custom rate-limiting (`time.sleep()`) to respect API free-tier quotas.
* Outputs the categorized data to a new file: `analyzed_social_data.csv`.

### 2. `analyze_all.py` (Exploratory Data Analysis)
A standalone EDA script that generates a 4-panel Seaborn/Matplotlib dashboard analyzing the dataset's metadata:
* **Time-Series Analysis:** Tweet volume over time.
* **Geospatial Data:** Top 10 user locations.
* **User Engagement:** Top 10 most active users.
* **Network Influence:** Distribution of user friend counts (handling corrupted data via `pd.to_numeric`).

### 3. `app.py` (Flask REST API)
A lightweight backend server that exposes the analyzed data to the web.
* Reads the processed `analyzed_social_data.csv`.
* Aggregates the sentiment counts.
* Serves the data securely via a GET endpoint (`/api/sentiment-data`) with CORS enabled.

### 4. `App.jsx` (React Frontend)
A responsive web dashboard built with React and `recharts`.
* Fetches live data from the Flask API on component mount.
* Visualizes the sentiment distribution using dynamic Bar and Pie charts.
* Handles loading states and backend connection errors gracefully.

---

## 🛠️ Tech Stack

**Data Science & AI:**
* Python 3
* Pandas (Data manipulation & cleaning)
* Matplotlib & Seaborn (Data visualization)
* Google GenAI SDK (LLM integration)

**Web Development:**
* Flask & Flask-CORS (Backend REST API)
* React.js (Frontend UI)
* Recharts (React charting library)

---

## ⚙️ Installation & Setup

### Prerequisites
You will need Node.js installed for the frontend, Python installed for the backend, and a free API key from Google AI Studio.

### 1. Backend Setup (Python)
1. Clone the repository.
2. Install the required Python dependencies:
   ```bash
   pip install pandas matplotlib seaborn flask flask-cors google-genai
