# TLS Concept Production 2.0

## Overview
This repository contains a Streamlit prototype that demonstrates how a TLS (Toyota Lean System)
team might explore flow, waste, and improvement ideas in one place. The app bundles three
lightweight tools:

- **Takt time calculator** – Align production cadence with customer demand and review capacity.
- **Waste tracker** – Capture gemba observations for the seven classic wastes and surface the
  biggest opportunities.
- **Kaizen planner** – Record continuous improvement ideas, estimate effort/impact, and spot
  quick wins.

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
