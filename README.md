# Sentiment Analyzer Dashboard

An AI-powered web app that analyzes customer review sentiment using Google Gemini Flash. Built as part of an AI Engineer portfolio.

## Live Demo
[Link to your Streamlit deployment — add this on Day 7]

## Features
- **Single review analysis** — paste any customer review and get instant sentiment, confidence score, themes, and a one-line summary
- **Bulk CSV analysis** — upload a CSV of reviews and analyze all of them in one click
- **Visual dashboard** — sentiment distribution, confidence histogram, and top themes charts
- **Downloadable results** — export the full analysis as a CSV

## Tech Stack
| Layer | Tool |
|---|---|
| Frontend | Streamlit |
| AI Model | Google Gemini 2.5 Flash |
| Data processing | Pandas |
| Charts | Plotly Express |
| Deployment | Streamlit Community Cloud |

## How It Works
1. User submits a review (single or bulk CSV)
2. App sends each review to Gemini with a structured prompt
3. Gemini returns a JSON object with sentiment, confidence, themes, and aspects
4. Results are parsed, displayed as a table, and visualized as charts

## Prompt Engineering
The core of this project is a carefully engineered prompt that forces Gemini to return strict JSON output. The prompt specifies an exact schema, valid enum values for sentiment, and fallback behavior for edge cases.

## Reliability
API calls include automatic retry logic (3 attempts with 10s delay) and a safe fallback response if all retries fail — ensuring bulk analysis never crashes mid-batch.

## Local Setup
```bash
git clone 
cd sentiment-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GOOGLE_API_KEY=<gemini_api_key>
```

Run the app:
```bash
streamlit run app.py
```

## Project Structure
```
sentiment-dashboard/
|_ app.py
|_ gemini_core.py
|_ prompt.txt
|_ requirements.txt
|_ examples/
|  |_ sample_reviews.csv
|  |_ sentiment_results.csv
|_ README.md
```
