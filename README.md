## Overview
This repository contains a Streamlit prototype that demonstrates how a TLS (Toyota Lean System)
team might explore flow, waste, and improvement ideas in one place. The refreshed dashboard keeps a
running history of every calculation or observation so data can be revisited during daily huddles
or leadership reviews.

The app bundles three lightweight tools:

- **Takt time planner** – Capture named scenarios, compare takt time versus cycle time, and review
  historical calculations on an interactive chart.
- **Waste observation log** – Record detailed gemba notes (area, shift, counts) and instantly see
  aggregated charts with the latest entries.
- **Kaizen planner** – Build an improvement backlog with due dates, status tracking, and leverage
  scoring cues to highlight quick wins.

Use the dashboard as a starting point for discussions about your own production system and as a
sandbox for future TLS experiments.

## Getting started
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the Streamlit dashboard
   ```bash
   streamlit run app.py
   ```
3. Open the URL printed in the terminal (typically http://localhost:8501) to explore the TLS
   concept modules.

Feel free to fork this repository and adapt the calculators, data models, or styling to suit your
team's workflows.
