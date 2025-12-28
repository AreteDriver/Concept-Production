# ADR 0001: Initial Architecture

**Status**: Accepted
**Date**: 2025-01-01
**Decision Makers**: James C. Young

## Context

Concept-Production needs to provide a dashboard for production teams to explore lean manufacturing concepts. The system must support:

- Takt time calculations with scenario comparison
- Waste observation logging with aggregation
- Kaizen improvement backlog management
- AR HUD concept exploration
- Quick iteration for prototype feedback

## Decision

We will implement a Streamlit-based prototype with:

1. **UI Framework**: Streamlit for rapid prototyping
2. **State Management**: Streamlit session state for in-session persistence
3. **Data Processing**: Pandas DataFrames for aggregation
4. **Visualization**: Altair/Plotly for charts

Initial version uses session state only; database persistence planned for production pilot.

## Alternatives Considered

### Alternative 1: Custom React/Vue web application
- **Pros**: More control over UX, better interactivity
- **Cons**: Significantly more development time, requires frontend expertise
- **Rejected**: Streamlit enables faster iteration for prototype phase

### Alternative 2: Excel/Google Sheets
- **Pros**: Familiar to operations teams, zero deployment
- **Cons**: No interactive visualizations, hard to version control, collaboration issues
- **Rejected**: Dashboard provides better UX for daily standup use

### Alternative 3: Power BI / Tableau
- **Pros**: Enterprise-grade analytics, familiar to business users
- **Cons**: Licensing costs, less customizable, separate from development workflow
- **Rejected**: Python-based solution integrates better with potential future ML features

## Consequences

### Positive
- Extremely fast iteration (hours vs. days)
- Python ecosystem enables future analytics/ML integration
- Easy to share via Streamlit Cloud
- Low barrier for operations teams to request changes

### Negative
- Session state lost on page refresh (until persistence added)
- Limited interactivity compared to custom frontend
- Streamlit Cloud has usage limits for free tier

### Risks
- Prototype may outgrow Streamlit's capabilities
- Users may expect features that are hard to implement in Streamlit

## Follow-up Actions

1. Add SQLite persistence via SQLAlchemy
2. Implement authentication for production data protection
3. Create export functionality for integration with existing spreadsheets
4. Evaluate WebXR libraries for AR HUD mockups
