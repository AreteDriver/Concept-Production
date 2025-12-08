"""Streamlit app illustrating the TLS facility production concept."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List

import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class TLSWasteCategory:
    """Represents a TLS waste focus area used across the facility."""

    name: str
    description: str


TLS_WASTES: List[TLSWasteCategory] = [
    TLSWasteCategory("Transportation", "Unnecessary movement of materials or products."),
    TLSWasteCategory("Inventory", "Excess stock that ties up cash and space."),
    TLSWasteCategory("Motion", "Unnecessary associate movement."),
    TLSWasteCategory("Waiting", "Idle time caused by imbalanced processes."),
    TLSWasteCategory("Overproduction", "Making more than is needed or too early."),
    TLSWasteCategory(
        "Overprocessing",
        "Doing more work or using more components than required for the TLS build list.",
    ),
    TLSWasteCategory("Defects", "Rework or scrap due to quality issues."),
]


def init_session_state() -> None:
    """Ensure session state keys are present."""

    defaults = {
        "improvement_ideas": [],
        "takt_history": [],
        "waste_log": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_overview() -> None:
    """Display background information about the TLS concept."""

    st.title("TLS Concept Production 2.0")
    st.subheader("TLS facility roadmap for continuous improvement")
    st.write(
        "This dashboard captures core concepts from the TLS facility playbook and helps "
        "teams quickly explore their production health. Use it to calculate takt time, "
        "visualise waste hotspots, and prioritise improvement experiments."
    )

    st.markdown(
        """
        ### TLS guiding principles
        * **Customer first** – Align production cadence with real demand.
        * **Eliminate waste** – Continuously surface and remove activities that do not add value.
        * **Respect for people** – Empower frontline teams to expose problems and solve them.
        * **Continuous improvement (Kaizen)** – Experiment, learn, and standardise the best practices.
        """
    )

    st.info(
        "Switch between the calculators in the sidebar to explore how each TLS element "
        "supports flow, quality, and stability."
    )

    st.caption(
        "The modules below are structured to capture data over time. Each calculation or observation "
        "is stored so teams can revisit trends during tiered meetings or kata coaching sessions."
    )


def _format_minutes(value: float) -> str:
    """Return a readable minutes string."""

    return f"{value:.0f} min/day"


def _format_units(value: float) -> str:
    """Return a readable unit string."""

    return f"{value:.1f} units"


def render_takt_time_calculator() -> None:
    """Provide takt time and capacity planning guidance."""

    st.header("Takt Time Planner")
    st.write(
        "Capture different production scenarios to understand how demand, shift coverage, and cycle "
        "time impact flow. The tracker preserves each calculation for quick comparison during stand-up "
        "conversations."
    )

    config_tab, insights_tab = st.tabs(["Scenario setup", "History & insights"])

    with config_tab:
        left, right = st.columns((1, 1))
        with left:
            with st.form("takt_form"):
                scenario = st.text_input(
                    "Scenario name",
                    help="Label the calculation (e.g. 'Baseline', 'Peak season', 'Future state').",
                )
                available_minutes = st.number_input(
                    "Available production time per shift (minutes)",
                    min_value=60,
                    max_value=1_200,
                    value=420,
                    step=15,
                )
                shifts = st.number_input(
                    "Number of shifts per day", min_value=1, max_value=4, value=1
                )
                demand = st.number_input(
                    "Customer demand per day (units)", min_value=1, value=200
                )
                cycle_time = st.number_input(
                    "Current average cycle time (minutes per unit)",
                    min_value=0.1,
                    value=2.5,
                )
                submitted = st.form_submit_button("Record scenario")

        with right:
            st.markdown(
                """
                **How to use**

                1. Enter the current shift structure and demand forecast.
                2. Capture the average process cycle time.
                3. Compare the resulting takt time to current performance to determine the gap.
                4. Save multiple scenarios (current, short-term, future state) for benchmarking.
                """
            )

    if submitted:
        total_available_time = available_minutes * shifts
        takt_time = total_available_time / demand
        capacity = total_available_time / cycle_time
        st.session_state["takt_history"].append(
            {
                "Scenario": scenario.strip() or f"Scenario {len(st.session_state['takt_history']) + 1}",
                "Recorded": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Available minutes": total_available_time,
                "Shifts": shifts,
                "Demand": demand,
                "Cycle time": cycle_time,
                "Takt time": takt_time,
                "Daily capacity": capacity,
                "Capacity vs demand": capacity - demand,
            }
        )

    if not st.session_state["takt_history"]:
        insights_tab.info("Log a scenario to reveal the takt analytics workspace.")
        return

    history_df = pd.DataFrame(st.session_state["takt_history"])
    history_df["Recorded"] = pd.to_datetime(history_df["Recorded"])
    history_df = history_df.sort_values("Recorded", ascending=False)

    latest = history_df.iloc[0]
    total_available_time = latest["Available minutes"]
    takt_time = latest["Takt time"]
    cycle_time = latest["Cycle time"]
    capacity = latest["Daily capacity"]

    with insights_tab:
        st.subheader(f"{latest['Scenario']} snapshot")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Available time", _format_minutes(total_available_time))
        col2.metric("Takt time", f"{takt_time:.2f} min/unit")
        col3.metric("Daily capacity", _format_units(capacity))
        col4.metric(
            "Capacity vs demand",
            f"{latest['Capacity vs demand']:.1f} units",
            help="Positive values indicate a capacity buffer.",
        )

        if cycle_time <= takt_time:
            st.success(
                "Cycle time is within takt — prioritise sustaining routines and error proofing."
            )
        else:
            st.warning(
                "Cycle time exceeds takt. Balance workloads, remove delays, or evaluate extra shifts."
            )

        chart_df = history_df.set_index("Recorded")["Takt time"].sort_index()
        st.markdown("### Scenario trends")
        st.line_chart(chart_df)

        st.dataframe(
            history_df,
            use_container_width=True,
            column_config={
                "Available minutes": st.column_config.NumberColumn(format="%d"),
                "Daily capacity": st.column_config.NumberColumn(format="%.1f"),
                "Capacity vs demand": st.column_config.NumberColumn(format="%.1f"),
                "Takt time": st.column_config.NumberColumn(format="%.2f"),
                "Cycle time": st.column_config.NumberColumn(format="%.2f"),
            },
        )

        st.download_button(
            "Download history (CSV)",
            history_df.to_csv(index=False).encode("utf-8"),
            file_name="takt_scenarios.csv",
            mime="text/csv",
        )

        st.caption(
            "Tip: Share the scenario history during tiered meetings so each team understands how changes "
            "in demand or shift coverage ripple through capacity."
        )


def render_waste_tracker() -> None:
    """Collect a snapshot of the seven wastes and highlight priorities."""

    st.header("Waste Observation Log")
    st.write(
        "Capture individual observations to build a time-based view of waste patterns. Filter the log "
        "to uncover hotspots by area, team, or shift."
    )

    with st.expander("Quick reference: TLS waste focus areas"):
        for waste in TLS_WASTES:
            st.markdown(f"**{waste.name}** — {waste.description}")

    with st.form("waste_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Waste category", [w.name for w in TLS_WASTES])
            count = st.number_input("Occurrences", min_value=1, value=1)
            observed_on = st.date_input(
                "Observation date",
                value=date.today(),
                max_value=date.today(),
            )
        with col2:
            area = st.text_input(
                "Process / area", help="e.g. Paint line, Shipping, Assembly cell 3"
            )
            shift = st.selectbox("Shift", ["Day", "Swing", "Night", "Mixed"])
            note = st.text_area(
                "Notes", help="Add context such as suspected root cause or defect count."
            )

        submitted = st.form_submit_button("Add observation")

    if submitted:
        st.session_state["waste_log"].append(
            {
                "Recorded": observed_on.strftime("%Y-%m-%d"),
                "Waste": category,
                "Occurrences": count,
                "Area": area.strip() or "Unspecified",
                "Shift": shift,
                "Notes": note.strip(),
            }
        )
        st.success(
            "Observation captured. Continue logging during gemba walks to build trends."
        )

    if not st.session_state["waste_log"]:
        st.caption("Log your first observation to unlock dashboards and analytics.")
        return

    log_df = pd.DataFrame(st.session_state["waste_log"])

    available_areas = sorted({entry["Area"] for entry in st.session_state["waste_log"]})
    area_filter = st.multiselect("Filter by area", available_areas)
    shift_filter = st.multiselect(
        "Filter by shift", ["Day", "Swing", "Night", "Mixed"],
    )

    filtered = log_df.copy()
    if area_filter:
        filtered = filtered[filtered["Area"].isin(area_filter)]
    if shift_filter:
        filtered = filtered[filtered["Shift"].isin(shift_filter)]

    if filtered.empty:
        st.warning("No observations available. Clear filters or log new data to continue.")
        return

    summary = (
        filtered.groupby("Waste", as_index=False)["Occurrences"].sum().sort_values(
            "Occurrences", ascending=False
        )
    )

    total_observations = int(filtered["Occurrences"].sum())
    unique_areas = filtered["Area"].nunique()
    last_observation = filtered.sort_values("Recorded", ascending=False).iloc[0]

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    kpi_col1.metric("Occurrences logged", f"{total_observations}")
    kpi_col2.metric("Areas represented", f"{unique_areas}")
    kpi_col3.metric(
        "Most recent entry", last_observation["Recorded"], help=last_observation["Area"]
    )

    col_chart, col_table = st.columns((2, 1))
    with col_chart:
        st.subheader("Occurrences by waste")
        if not summary.empty:
            st.bar_chart(summary.set_index("Waste"))
        else:
            st.info("No observations match the current filters.")
    with col_table:
        st.subheader("Latest entries")
        st.dataframe(
            filtered.sort_values(["Recorded", "Occurrences"], ascending=[False, False]).head(8),
            use_container_width=True,
        )

    if not summary.empty:
        top_waste = summary.iloc[0]
        st.info(
            f"{top_waste['Waste']} is currently the largest source of waste with "
            f"{top_waste['Occurrences']} occurrences logged. Facilitate a root cause session and align "
            "kaizen ideas accordingly."
        )

    st.download_button(
        "Download filtered log (CSV)",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="waste_observations.csv",
        mime="text/csv",
    )

    st.caption(
        "Export the filtered table to share with leadership or to support PDCA reviews."
    )


def render_kaizen_planner() -> None:
    """Simple impact vs. effort planner for kaizen experiments."""

    st.header("Continuous Improvement Planner")
    st.write(
        "Capture kaizen ideas, estimate impact and effort, and organise the backlog. Use the "
        "prioritisation cues to select quick wins versus larger strategic bets."
    )

    with st.form("kaizen_form"):
        title = st.text_input("Idea title")
        goal = st.text_area("Problem / goal statement")
        effort = st.slider("Effort", min_value=1, max_value=5, value=3)
        impact = st.slider("Impact", min_value=1, max_value=5, value=3)
        owner = st.text_input(
            "Owner", help="Person accountable for shepherding the experiment."
        )
        due = st.date_input("Target completion", value=date.today())
        status = st.selectbox("Status", ["To review", "In progress", "Complete"])
        submitted = st.form_submit_button("Add idea")

    if submitted and title.strip():
        st.session_state["improvement_ideas"].append(
            {
                "Idea": title.strip(),
                "Owner": owner.strip() or "Unassigned",
                "Impact": impact,
                "Effort": effort,
                "Leverage score": impact - effort,
                "Due": due.strftime("%Y-%m-%d"),
                "Status": status,
                "Statement": goal.strip() or "",
            }
        )
        st.success("Idea added to the backlog. Continue capturing insights!")

    if not st.session_state["improvement_ideas"]:
        st.caption("Add your first idea to see the prioritisation table.")
        return

    ideas_df = pd.DataFrame(st.session_state["improvement_ideas"])
    st.subheader("Kaizen backlog")

    status_counts = ideas_df["Status"].value_counts().reindex(
        ["To review", "In progress", "Complete"], fill_value=0
    )
    progress = 0
    if status_counts.sum():
        progress = status_counts["Complete"] / status_counts.sum()

    progress_col, legend_col = st.columns([2, 1])
    with progress_col:
        st.progress(progress, text=f"{int(progress * 100)}% complete")
    with legend_col:
        st.metric("Ideas logged", f"{len(ideas_df)}")

    sort_option = st.selectbox(
        "Sort backlog by",
        ["Status", "Due date", "Leverage"],
        help="Adjust to review near-term deadlines, leverage scores, or workflow status.",
    )

    if sort_option == "Due date":
        ideas_df = ideas_df.sort_values("Due")
    elif sort_option == "Leverage":
        ideas_df = ideas_df.sort_values("Leverage score", ascending=False)
    else:
        ideas_df = ideas_df.sort_values(["Status", "Leverage score"], ascending=[True, False])

    st.dataframe(
        ideas_df,
        use_container_width=True,
        column_config={
            "Impact": st.column_config.NumberColumn(min_value=1, max_value=5),
            "Effort": st.column_config.NumberColumn(min_value=1, max_value=5),
            "Leverage score": st.column_config.NumberColumn(format="%.0f"),
        },
    )

    quick_wins = ideas_df[(ideas_df["Impact"] >= 4) & (ideas_df["Effort"] <= 2)]
    if not quick_wins.empty:
        st.success(
            "Quick wins detected! Focus on these ideas first to build momentum: "
            + ", ".join(quick_wins["Idea"].tolist())
        )

    stretch = ideas_df[(ideas_df["Impact"] >= 4) & (ideas_df["Effort"] >= 4)]
    if not stretch.empty:
        st.warning(
            "High-impact but heavy lifts spotted. Plan cross-functional support for: "
            + ", ".join(stretch["Idea"].tolist())
        )

    st.download_button(
        "Download kaizen backlog (CSV)",
        ideas_df.to_csv(index=False).encode("utf-8"),
        file_name="kaizen_backlog.csv",
        mime="text/csv",
    )


def render_ar_hud_concepts() -> None:
    """Outline augmented reality HUD concepts for each facility role."""

    st.header("AR HUD Concepts")
    st.write(
        "Blueprint overlays for the TLS augmented reality programme. Each HUD is tuned to the "
        "workflow, safety posture, and quality checks required in specific areas across the "
        "facility. Use these references when briefing artists or prototyping heads-up displays."
    )

    st.info(
        "The concepts below assume lightweight wearable displays (Microsoft HoloLens 2) that can "
        "anchor callouts directly on vehicles, tools, and staging zones. They emphasise glanceable "
        "guidance, checklists, and quick access to escalation workflows, enhanced with real-time AI "
        "feedback for installation validation and quality assurance."
    )

    st.markdown(
        """
        ### AI-Enhanced Features
        - **Real-time guidance**: AI models provide step-by-step installation sequences optimized 
          for each vehicle configuration
        - **Visual quality checks**: Computer vision detects misaligned parts, missing components, 
          and assembly errors automatically
        - **Predictive alerts**: System warns of common installation pitfalls before they occur
        - **Performance tracking**: Telemetry captures cycle times and quality metrics for 
          continuous improvement
        
        📖 See [AI-Assisted Workflows documentation](../docs/ai-assisted-workflows.md) for complete 
        details on AI integration strategy.
        """
    )

    flow_tab, ppo_tab, fqa_tab, tech_tab = st.tabs([
        "Flow Driver shuttle",
        "PPO install shop",
        "FQA final assurance",
        "Technical implementation",
    ])

    with flow_tab:
        st.subheader("Flow Driver shuttle operations")
        st.write(
            "Supports associates moving vehicles between dry dock, production, and the last point "
            "of rest before outbound logistics."
        )

        flow_layers = pd.DataFrame(
            [
                {
                    "Install focus": "Dry dock pick-up",
                    "HUD layers": "Vehicle identifier, readiness status, battery/fuel check, route to production entry gate.",
                    "Operator cues": "Confirm staging order, acknowledge vehicle match, and review any hold tags before moving.",
                },
                {
                    "Install focus": "Production delivery",
                    "HUD layers": "Lane guidance overlay, takt alignment timer, drop-zone alignment grid.",
                    "Operator cues": "Highlight assigned bay, signal congestion alerts, and prompt for hand-off confirmation.",
                },
                {
                    "Install focus": "Last point of rest staging",
                    "HUD layers": "Logistics destination marker, outbound schedule countdown, safety sweep checklist.",
                    "Operator cues": "Display truck/train assignment, verify wheel chocks, and capture final walk-around photo.",
                },
            ]
        )
        st.dataframe(flow_layers, use_container_width=True)

        st.caption(
            "Consider pairing the HUD with voice capture for hands-free confirmations when drivers "
            "are in motion."
        )

    with ppo_tab:
        st.subheader("PPO install shop overlays")
        st.write(
            "Guides accessory installation sequences such as wheels, TRD upgrades, and cosmetic "
            "packages inside the production personalization operations (PPO) area."
        )

        ppo_layers = pd.DataFrame(
            [
                {
                    "Install focus": "Wheel & tire fitment",
                    "HUD layers": "Torque spec indicators, lug pattern alignment, batch barcode verification.",
                    "Operator cues": "Prompt torque gun settings, display required torque pattern, and log completion timestamp.",
                },
                {
                    "Install focus": "TRD & performance upgrades",
                    "HUD layers": "Part inventory checklist, fastener map, calibration reminders.",
                    "Operator cues": "Highlight correct component variant, flag incompatible combinations, and link to tuning steps.",
                },
                {
                    "Install focus": "Protection & exterior accessories",
                    "HUD layers": "Mudflap positioning silhouette, skid plate bolt order, decal alignment grid, exhaust routing cues.",
                    "Operator cues": "Surface prep checklist, warn about curing times, and capture photo proof for quality.",
                },
                {
                    "Install focus": "Cosmetic detailing",
                    "HUD layers": "Paint-safe zone masks, badge placement guide, inspection lighting controls.",
                    "Operator cues": "Coach on cleaning agents, show customer-specific notes, and escalate paint damage findings.",
                },
            ]
        )
        st.dataframe(ppo_layers, use_container_width=True)

        st.caption(
            "Use colour-coded layers to distinguish required checks versus optional personalisation "
            "steps, reducing cognitive load on installers."
        )

    with fqa_tab:
        st.subheader("FQA final assurance overlays")
        st.write(
            "Ensures every vehicle leaving production meets readiness requirements at the final "
            "quality assurance (FQA) stage."
        )

        fqa_layers = pd.DataFrame(
            [
                {
                    "Install focus": "Cabin readiness",
                    "HUD layers": "Floor mat placement outline, cargo net install prompt, document packet checklist.",
                    "Operator cues": "Confirm interior cleanliness, record invoice barcode, and flag missing literature instantly.",
                },
                {
                    "Install focus": "Exterior finishing",
                    "HUD layers": "Tie-down pin removal reminder, plastic clip placement guide, damage sweep overlay.",
                    "Operator cues": "Provide before/after comparison reference and require visual confirmation before proceeding.",
                },
                {
                    "Install focus": "Final paperwork & release",
                    "HUD layers": "Shipping manifest verification, compliance signature prompts, outbound bay assignment.",
                    "Operator cues": "Highlight outstanding holds, capture photo proof, and push release update to logistics.",
                },
            ]
        )
        st.dataframe(fqa_layers, use_container_width=True)

        st.caption(
            "A short huddle view can summarise defects or missing items detected through the HUD to "
            "tighten the feedback loop with upstream teams."
        )

    with tech_tab:
        st.subheader("Technical implementation architecture")
        st.write(
            "This section outlines the technical approach for deploying AI-enhanced AR HUD systems "
            "in production environments, integrating HoloLens 2, FastAPI backend, and containerized "
            "deployment for scalability."
        )

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                ### Hardware Platform
                **Microsoft HoloLens 2**
                - 2K resolution per eye for clear overlay visibility
                - Built-in WiFi 6 for real-time data streaming
                - 4+ hour battery life for full shift coverage
                - Industry-grade durability for manufacturing environments
                - Hands-free operation via voice and gestures
                - Spatial anchoring for precise vehicle-relative overlays
                
                ### Software Stack
                **Frontend (AR Client)**
                - HoloLens 2 native application
                - Spatial mapping and object recognition
                - Voice command processing
                - Gesture controls for interaction
                
                **Backend (FastAPI/Python)**
                - REST API for AR client communication
                - Real-time AI guidance engine
                - Visual quality inspection models
                - Telemetry and analytics pipeline
                - Integration with vehicle build systems
                """
            )
        
        with col2:
            st.markdown(
                """
                ### AI Capabilities
                **Real-time Installation Guidance**
                - Step-by-step sequences optimized per vehicle variant
                - Dynamic torque specifications and tool settings
                - Predictive alerts for common installation errors
                
                **Visual Quality Inspection**
                - Automated part verification and alignment checks
                - Surface quality and defect detection
                - Completeness validation for installation steps
                - Real-time feedback to prevent rework
                
                **Performance Analytics**
                - Cycle time tracking and takt comparison
                - First-time-through rate monitoring
                - Skill development and coaching insights
                - Waste pattern identification
                
                ### Deployment Infrastructure
                **Docker Containerization**
                - Microservices architecture for scalability
                - Version control and rollback capabilities
                - Cloud or on-premises deployment options
                - Automated CI/CD pipeline integration
                """
            )

        st.markdown("---")
        
        st.subheader("System integration overview")
        st.code(
            """
Architecture:
┌─────────────────────┐
│  HoloLens 2 Client  │ ← AR overlays, voice, gestures, spatial anchoring
└──────────┬──────────┘
           │ REST API (HTTPS/WebSocket)
           ▼
┌─────────────────────┐
│  FastAPI Backend    │ ← AI models, business logic, real-time guidance
│  (Containerized)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Data Layer         │ ← Vehicle specs, quality metrics, telemetry
│  + TLS Dashboard    │   Integration with existing Streamlit dashboard
└─────────────────────┘

Data Flow:
1. AR client requests installation guidance for VIN
2. Backend retrieves vehicle configuration and generates AI-optimized sequence
3. Visual overlays and voice prompts guide associate through steps
4. Computer vision validates each step in real-time
5. Telemetry feeds back to TLS dashboard for takt/waste/kaizen tracking
            """,
            language="text"
        )

        st.subheader("Integration with TLS dashboard")
        integration_data = pd.DataFrame([
            {
                "TLS Module": "Takt Time Planner",
                "AR Data Integration": "Real-time cycle time updates from AR-tracked installations",
                "Benefit": "Accurate capacity planning with live production data"
            },
            {
                "TLS Module": "Waste Observation Log",
                "AR Data Integration": "Automated waste detection (motion, waiting, defects) from AR sensors",
                "Benefit": "Continuous gemba observations without manual logging"
            },
            {
                "TLS Module": "Kaizen Planner",
                "AR Data Integration": "AI-generated improvement suggestions from installation pattern analysis",
                "Benefit": "Data-driven kaizen ideas with quantified impact"
            },
            {
                "TLS Module": "AR HUD Concepts",
                "AR Data Integration": "Usage metrics, adoption rates, and effectiveness scores",
                "Benefit": "Evidence-based iteration on AR experience design"
            },
        ])
        st.dataframe(integration_data, use_container_width=True)

        st.info(
            "📖 For complete AI integration strategy, deployment roadmap, and success metrics, "
            "see [docs/ai-assisted-workflows.md](https://github.com/AreteDriver/TLS-Concept-production-2.0/blob/main/docs/ai-assisted-workflows.md) "
            "and [docs/ui-ux/ar-hud-concepts.md](https://github.com/AreteDriver/TLS-Concept-production-2.0/blob/main/docs/ui-ux/ar-hud-concepts.md)"
        )

        st.caption(
            "This technical implementation builds upon research from AI/AR installation optimization "
            "initiatives, combining HoloLens visualization, real-time AI feedback, and Lean "
            "manufacturing principles for streamlined automotive production."
        )


PAGE_RENDERERS = {
    "Overview": render_overview,
    "Takt time": render_takt_time_calculator,
    "Waste tracker": render_waste_tracker,
    "Kaizen planner": render_kaizen_planner,
    "AR HUD concepts": render_ar_hud_concepts,
}


def main() -> None:
    """Application entry point."""

    st.set_page_config(page_title="TLS Concept Production 2.0", layout="wide")
    init_session_state()

    st.sidebar.title("TLS navigation")
    selection = st.sidebar.radio("Select module", list(PAGE_RENDERERS.keys()))

    PAGE_RENDERERS[selection]()


if __name__ == "__main__":
    main()
