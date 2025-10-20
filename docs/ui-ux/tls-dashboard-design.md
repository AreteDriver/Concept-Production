# TLS Concept Dashboard – UI & UX Design Blueprint

## Purpose and guiding goals
- Provide production leaders with a single screen to understand flow health, waste hotspots, and improvement work-in-progress.
- Make data capture effortless during fast paced tiered meetings and gemba walks.
- Encourage daily habit building through persistent histories, clear trends, and actionable callouts.

## Target personas
| Persona | Needs | Design responses |
| --- | --- | --- |
| Area supervisor | Log observations while walking the floor and compare takt changes after shift adjustments. | Lightweight forms, autosaved histories, and CSV exports to share with wider teams. |
| Continuous improvement coach | Facilitate kaizen prioritisation workshops. | Impact/effort visuals, quick-win surfacing, and backlog progress indicators. |
| Site director | Monitor readiness for launches and improvement cadence. | Snapshot metrics, timeline charts, and downloadable evidence packs. |

## Information architecture
1. **Overview landing page** – Communicates guiding principles and explains how modules connect. Acts as onboarding for first-time users.
2. **Takt Time Planner** – Scenario modelling workspace with immediate feedback cards and historical comparison charts.
3. **Waste Observation Log** – Form-first logging experience with filters, KPIs, and bar charts to reveal patterns.
4. **Continuous Improvement Planner** – Backlog management table with progress meter, prioritisation sort options, and quick-win callouts.

Navigation is handled via a left-hand sidebar radio selector so modules remain a single click away during stand-up conversations.

## Layout system
- **Grid** – Streamlit wide layout with 12-column mental model. Cards and charts pair in 2-column arrangements for balanced density.
- **Hierarchy** – Each module uses a Header → Description → Form → Insights pattern to reduce cognitive load.
- **Feedback** – Success and warning states explain the next best action (e.g., log more data, balance cycle time, celebrate quick wins).

## Module-specific UX notes
### Takt Time Planner
- Tabs split configuration from insights to prevent forms and analytics from competing for attention.
- Metric cards display takt, capacity, and demand gap with consistent units to aid quick interpretation.
- Scenario history table uses column formatting and CSV export for offline analysis.

### Waste Observation Log
- Collapsible reference keeps the seven wastes available without consuming primary screen real estate.
- Dual multiselect filters mirror how teams slice data (by area and shift).
- KPI strip highlights observation volume, coverage, and freshness before diving into charts.
- Empty states gently coach users to capture new data rather than presenting blank visuals.

### Continuous Improvement Planner
- Intake form estimates impact vs. effort and captures owner plus due date for accountability.
- Progress bar summarises throughput of the improvement pipeline.
- Sort controls support different meeting cadences (status reviews, due-date scrubs, leverage planning).
- Download action lets teams archive or share the backlog snapshot after each meeting.

## Visual language
- **Tone** – Friendly and coaching-focused (info boxes, success prompts) to reinforce continuous improvement culture.
- **Colour accents** – Streamlit defaults with occasional success/warning states; can be themed later if brand palette is supplied.
- **Typography** – Rely on Streamlit system fonts for readability; headings in sentence case for clarity.

## Future enhancements
- Introduce authentication and persistence so histories survive across sessions.
- Add control charts or heat maps when more data is available.
- Allow exporting directly to presentation templates for leadership updates.
- Extend design blueprint into a Figma kit for cross-team collaboration once visual identity is finalised.
