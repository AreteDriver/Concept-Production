# TLS Concept Roadmap

## Purpose
This roadmap outlines high-value improvements to pursue in upcoming iterations of the TLS concept dashboard so every commit builds toward a production-ready pilot.

## 1. Data and persistence
- Introduce a lightweight database (e.g., SQLite via SQLAlchemy) so takt, waste, and kaizen histories persist between sessions.
- Add authentication hooks to protect production data once pilots move beyond mock content.
- Design import/export templates to bootstrap the app with historical spreadsheets from the facility launch team.

## 2. Analytics depth
- Layer in takt versus cycle time variance charts with control limits to highlight instability.
- Provide Pareto breakdowns for the waste log and allow trend slicing by week or shift.
- Add prioritisation scoring visuals (impact vs. effort matrix) inside the kaizen planner to support workshop facilitation.

## 3. AR HUD prototyping and AI integration
### AR visualization
- Translate the concept brief into interactive Figma frames or lightweight WebXR mockups.
- Attach asset checklists to each HUD tab in the app so designers can download references directly.
- Integrate feedback capture (thumbs up/down, comments) for each HUD concept to guide iterative art reviews.

### Technical foundation
- Set up FastAPI backend with REST API endpoints for AR client communication.
- Establish development environment for HoloLens 2 prototyping and spatial anchoring.
- Create proof-of-concept AR overlay for one workflow (e.g., wheel installation in PPO).
- Implement basic telemetry capture pipeline for AR usage metrics.

### AI-assisted workflows
- Develop visual AI models for automated quality inspection (one installation type to start).
- Create real-time AI guidance engine for standardized installation sequences.
- Integrate AI-detected waste observations into existing Waste Observation Log.
- Build predictive analytics dashboard for bottleneck and quality forecasting.

### Deployment infrastructure
- Containerize application components with Docker for scalable deployment.
- Design cloud and on-premises hosting architecture for production environments.
- Establish version control and rollback procedures for AI models and AR experiences.
- Create monitoring and alerting for system health and performance metrics.

## 4. Operational readiness
- Document standard work for updating the dashboard before daily huddles, including data validation steps.
- Create a deployment playbook covering Streamlit Cloud and on-prem hosting expectations.
- Develop a change log template to track feature rollouts to pilot teams.

## 5. Research and validation
- Schedule usability walkthroughs with Flow Driver, PPO, and FQA associates; log insights in a research repository.
- Instrument the dashboard with usage analytics (mixpanel, PostHog, or open-source equivalent) to understand adoption.
- Establish success metrics (takt adherence, defect reduction, kaizen throughput) and define how the dashboard reports on them.

Keep this roadmap under version control—update sections as milestones are achieved or new priorities emerge.
