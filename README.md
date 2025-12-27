## Overview
This repository contains a Streamlit prototype that demonstrates how the Client facility concept team
might explore flow, waste, and improvement ideas in one place. The refreshed dashboard keeps a
running history of every calculation or observation so data can be revisited during daily huddles
or leadership reviews.

This initiative integrates learnings from AI/AR installation optimization research to envision a 
future where real-time AI guidance, HoloLens visualization, and Lean manufacturing principles work 
together to streamline automotive production processes.

The app bundles four lightweight tools:

- **Takt time planner** – Capture named scenarios, compare takt time versus cycle time, and review
  historical calculations on an interactive chart.
- **Waste observation log** – Record detailed gemba notes (area, shift, counts) and instantly see
  aggregated charts with the latest entries.
- **Kaizen planner** – Build an improvement backlog with due dates, status tracking, and leverage
  scoring cues to highlight quick wins.
- **AR HUD concepts** – Explore heads-up display overlays for Flow Driver shuttles, PPO installs,
  and FQA final assurance to brief experience designers. Now enhanced with technical implementation 
  details including HoloLens 2 integration, FastAPI backend architecture, and AI-assisted workflows.

Use the dashboard as a starting point for discussions about your own production system and as a
sandbox for future Client experiments.

### Plan the next iteration

Review the [project roadmap](docs/roadmap.md) for a curated list of high-value improvements to
implement next—covering data persistence, deeper analytics, AR prototyping support, operational
readiness, and research activities. Update it as milestones are completed so the team stays aligned
on what to push to the repository next.

## Getting started
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the Streamlit dashboard
   ```bash
   streamlit run app.py
   ```
3. Open the URL printed in the terminal (typically http://localhost:8501) to explore the Client
   concept modules.

### Explore the design blueprint

The `docs/` directory contains the UI/UX architecture that guides the Streamlit implementation.
Use it as a reference when extending the dashboard or collaborating with designers:

- [`docs/ui-ux/dashboard-design.md`](docs/ui-ux/dashboard-design.md) – Personas, information
  architecture, and layout decisions.
- [`docs/ui-ux/ar-hud-concepts.md`](docs/ui-ux/ar-hud-concepts.md) – Concept art brief for AR heads-
  up displays tailored to each facility workflow, now including technical implementation with 
  HoloLens 2, FastAPI backend, and Docker deployment.
- [`docs/ai-assisted-workflows.md`](docs/ai-assisted-workflows.md) – AI integration strategy for 
  real-time guidance, visual quality inspection, predictive analytics, and automated waste detection.

Feel free to fork this repository and adapt the calculators, data models, or styling to suit your
team's workflows. Contributions that add additional documentation artefacts (wireframes, research
insights, deployment runbooks) are welcome.
