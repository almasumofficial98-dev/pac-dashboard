# PAC Performance Dashboard

A full-stack modern interactive analytics dashboard designed specifically for PAC Performance metrics. This project blends a sleek SaaS aesthetic with deep analytical capabilities utilizing Streamlit, Plotly, Pandas, and an optional Flask API.

## Features

- **Modern UI Suite**: Dark theme, smooth transitions, animated counters, glassmorphism cards.
- **Dynamic Excel Data Loading**: Automatically fetches entire sheets from `PAC_Performance_Template.xlsx` and makes them available instantly.
- **Integrated API**: Bundled Flask endpoints serving Excel data as JSON. 
- **Analytics & Visualizations**: Interactive Heatmaps, Bar Charts, Line Charts, and Pie Charts using Plotly.

## Project Structure

```
pac-dashboard/
├── app/
│   ├── main.py                   # Streamlit Frontend application
│   ├── api.py                    # Flask API routing layer
│   ├── components/               # Python/Streamlit logic units
│   ├── utils/                    # Data logic
│   ├── static/                   # CSS and JavaScript
│   └── templates/                # HTML structural injection
├── data/
│   └── PAC_Performance_Template.xlsx # Source Excel dataset
├── requirements.txt
└── vercel.json
```

## Running Locally

### 1. Requirements

We recommend utilizing `uv` for lightning-fast Python dependency management. Make sure you have python 3.9+ installed natively.

```bash
# Setup a virtual environment with uv
uv venv

# Activate on Windows
.venv\Scripts\activate
# Activate on Mac/Linux
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Start Services

To launch the primary **Streamlit UI**:

```bash
streamlit run app/main.py
```
This initializes the SaaS dashboard.

To launch the **Flask JSON API** optionally:

```bash
flask --app app/api.py run --port 5000
```
This initializes routes like `http://127.0.0.1:5000/api/metrics`.

## Deployment

Deploying this app defaults to utilizing Vercel's Python backend for API features. The `vercel.json` provides standard Serverless routing. Streamlit deployment can easily leverage Streamlit Community Cloud or Azure/AWS container setups by directly targeting `app/main.py`.
