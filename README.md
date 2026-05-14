# Cloud Kitchen PNL and Variance Analytics Dashboard

## Project Overview

This project analyzes cloud kitchen operational and financial performance using Python, Pandas, Streamlit, and Plotly.

The solution includes two interactive dashboards:

1. Kitchen Level PNL Dashboard
2. Variance Level PNL Dashboard

The dashboards provide insights into:
- Revenue trends
- EBITDA performance
- Store-level profitability
- Food variance analysis
- Revenue cohort analysis
- Operational efficiency

---

## Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Jupyter Notebook

---

## Project Structure

REBEL FOOD PROJECT/
│
├── data/
├── notebooks/
├── outputs/
├── app.py
├── variance_dashboard.py
├── requirements.txt
└── README.md

---

## Dashboard Features

### Kitchen Level Dashboard
- KPI summary cards
- Revenue trend analysis
- EBITDA trend analysis
- Top-performing stores
- Revenue composition analysis
- City-level revenue analysis
- Variance vs profitability analysis

### Variance Level Dashboard
- Variance category filtering
- Revenue cohort analysis
- Store count summaries
- Variance distribution visualization
- Detailed operational tables

---

## How to Run the Project

### Step 1 — Create Virtual Environment

python -m venv venv

### Step 2 — Activate Environment

Windows:
venv\Scripts\activate

### Step 3 — Install Dependencies

pip install -r requirements.txt

### Step 4 — Run Dashboard 1

streamlit run app.py

### Step 5 — Run Dashboard 2

streamlit run variance_dashboard.py

---

## Key Business Insights

- Revenue growth does not always guarantee profitability.
- Higher variance often correlates with lower EBITDA performance.
- Revenue cohorts demonstrate varying operational efficiency.
- Store-level analytics helps identify operational bottlenecks.

---

Cloud Kitchen Analytics Project
Built using Streamlit & Plotly
