# 📊 AI-Powered Social Media Sentiment Analysis Pipeline

An end-to-end data pipeline that processes social media text, categorizes its sentiment using Large Language Models (LLMs), and visualizes the results through a modern React dashboard.

## 🚀 Overview

Social media data is inherently messy and full of nuance, sarcasm, and slang. Traditional ML models often struggle to classify this accurately. This project utilizes the **Google Gemini 2.5 Flash API** to contextually analyze raw text data and accurately categorize it into `Positive`, `Negative`, or `Neutral` sentiments.

### Key Features
* **LLM Integration:** Replaces traditional Naive Bayes/SVM approaches with Google's Gemini API for superior context understanding and sarcasm detection.
* **Automated Data Processing:** Python-based pipeline utilizing `pandas` for bulk CSV data manipulation and cleaning.
* **Rate-Limit Handling:** Custom implementation to elegantly handle API quota limits (429 Resource Exhausted) during bulk processing.
* **Interactive Frontend:** A responsive React dashboard utilizing `recharts` to visualize sentiment volume and distribution.

## 🛠️ Tech Stack
* **Data Processing & AI:** Python, Pandas, Google GenAI SDK
* **Frontend:** React.js, Recharts, CSS
* **APIs:** Google Gemini API

## ⚙️ Installation & Setup

### 1. Python Backend (Data Processing)
1. Clone the repository.
2. Install the required Python libraries:
   ```bash
   pip install google-genai pandas
