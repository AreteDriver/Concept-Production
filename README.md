# Concept-Production

**Operational dashboard for lean manufacturing concepts** — Takt time planning, waste observation logging, and Kaizen backlog management in a single Streamlit app.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)

---

## What It Is

Concept-Production is a Streamlit prototype for production floor teams to explore flow, waste, and improvement ideas in one place. The dashboard keeps a running history of every calculation or observation for revisiting during daily huddles or leadership reviews.

**Bundled Tools**:
- **Takt Time Planner** — Capture named scenarios, compare takt vs. cycle time, review historical calculations
- **Waste Observation Log** — Record gemba notes (area, shift, counts), see aggregated charts
- **Kaizen Planner** — Build improvement backlog with due dates, status tracking, leverage scoring
- **AR HUD Concepts** — Explore heads-up display overlays for Flow Driver shuttles, PPO installs, and FQA

---

## Problem / Solution / Impact

**Problem**: Production teams juggle spreadsheets for takt time, separate logs for waste observations, and ad-hoc lists for improvement ideas. Data lives in silos and gets stale.

**Solution**: Concept-Production provides:
- Unified dashboard for lean manufacturing metrics
- Session-persistent history of all calculations
- Quick-win identification via impact/effort scoring
- AR HUD concept briefs for future tooling discussions

**Impact** (Intended Outcomes):
- Reduce context-switching between tools during daily standups
- Preserve calculation history for trend analysis and coaching sessions
- Surface quick wins in Kaizen backlog with leverage scoring
- Provide shared artifact for cross-functional process improvement

---

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Install

```bash
git clone https://github.com/AreteDriver/Concept-Production.git
cd Concept-Production
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
# Open http://localhost:8501
```

---

## Architecture

```
[Streamlit UI]
      |
      v
[Session State]  ←── Takt History, Waste Log, Improvement Ideas
      |
      v
[Pandas DataFrames]  ←── Aggregation, Charting
      |
      v
[Altair/Plotly Charts]
```

### Project Structure

```
Concept-Production/
├── app.py              # Main Streamlit application
├── docs/
│   ├── roadmap.md      # Feature prioritization
│   └── ui-ux/          # Design documentation
├── requirements.txt    # Dependencies (streamlit, pandas)
└── LICENSE
```

---

## AI Operating Model

This project demonstrates operational tooling patterns rather than AI integration. However, future iterations could incorporate:

| Layer | Planned Implementation |
|-------|------------------------|
| **Structured Outputs** | Export takt/waste data to JSON for external analysis pipelines |
| **Validation / Safety Rails** | Authentication hooks before production pilot (see roadmap) |
| **Retry / Fallback** | Session state persistence avoids data loss during browser refresh |
| **Telemetry** | Usage analytics (Mixpanel/PostHog) planned for adoption tracking |

---

## Key Decisions

See [docs/adr/0001-initial-architecture.md](docs/adr/0001-initial-architecture.md) for the architecture decision record.

**Summary of Key Decisions**:
1. **Streamlit for Rapid Prototyping** — Fast iteration over building custom web stack
2. **Session State Persistence** — Keep history within session; database persistence planned
3. **Lean Waste Categories Hardcoded** — Standard 7 wastes baked in for consistency
4. **AR HUD as Concept Tab** — Exploration space for future tooling, not full implementation

---

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for detailed priorities.

- [ ] SQLite/SQLAlchemy for persistence between sessions
- [ ] Authentication hooks for production data protection
- [ ] Import/export templates for historical spreadsheets
- [ ] Takt vs. cycle variance charts with control limits
- [ ] Impact vs. effort matrix visualization for Kaizen prioritization
- [ ] WebXR mockups for AR HUD concepts

---

## Demo

<!-- TODO: Add demo GIF showing takt calculator and waste log -->
*Demo placeholder: Record calculating takt time and logging a waste observation*

---

## Contributing

Fork this repository and adapt calculators, data models, or styling to suit your team's workflows.

```bash
# Development
pip install -r requirements.txt
streamlit run app.py
```

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/AreteDriver/Concept-Production/issues)
- **Roadmap**: [docs/roadmap.md](docs/roadmap.md)
- **UI/UX Docs**: [docs/ui-ux/](docs/ui-ux/)
