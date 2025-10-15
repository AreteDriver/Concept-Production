"""Streamlit app illustrating a TLS (Toyota Lean System) production concept."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List

import pandas as pd
import streamlit as st


@dataclass(frozen=True)
class WasteCategory:
    """Represents one of the classic Toyota Lean System wastes."""

    name: str
    description: str


WASTES: List[WasteCategory] = [
    WasteCategory("Transportation", "Unnecessary movement of materials or products."),
    WasteCategory("Inventory", "Excess stock that ties up cash and space."),
    WasteCategory("Motion", "Unnecessary employee movement."),
    WasteCategory("Waiting", "Idle time caused by imbalanced processes."),
    WasteCategory("Overproduction", "Making more than is needed or too early."),
    WasteCategory("Overprocessing", "Doing more work or using more components than required."),
    WasteCategory("Defects", "Rework or scrap due to quality issues."),
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
    st.subheader("Toyota Lean System roadmap for continuous improvement")
    st.write(
        "This dashboard captures core concepts from the Toyota Lean System (TLS) and "
        "helps teams quickly explore their production health. Use it to calculate takt "
        "time, visualise waste hotspots, and prioritise improvement experiments."
    )

    st.markdown(
        """
        ### Guiding principles
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


def render_takt_time_calculator() -> None:
    """Provide takt time and capacity planning guidance."""

    st.header("Takt Time Planner")
    st.write(
        "Capture different production scenarios to understand how demand, shift coverage, and cycle "
        "time impact flow. The tracker preserves each calculation for quick comparison during stand-up "
        "conversations."
    )

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
        right.info("Log a scenario to reveal the takt analytics workspace.")
        return

    latest = st.session_state["takt_history"][-1]
    total_available_time = latest["Available minutes"]
    takt_time = latest["Takt time"]
    cycle_time = latest["Cycle time"]
    capacity = latest["Daily capacity"]

    with right:
        st.subheader(f"{latest['Scenario']} snapshot")
        col1, col2, col3 = st.columns(3)
        col1.metric("Available time", f"{total_available_time:.0f} min/day")
        col2.metric("Takt time", f"{takt_time:.2f} min/unit")
        col3.metric("Daily capacity", f"{capacity:.1f} units")

        if cycle_time <= takt_time:
            st.success(
                "Cycle time is within takt — prioritise sustaining routines and error proofing."
            )
        else:
            st.warning(
                "Cycle time exceeds takt. Balance workloads, remove delays, or evaluate extra shifts."
            )

    history_df = pd.DataFrame(st.session_state["takt_history"])
    st.subheader("Scenario history")
    st.dataframe(history_df, use_container_width=True)

    chart_df = history_df.set_index("Scenario")["Takt time"]
    st.line_chart(chart_df)

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

    with st.expander("Quick reference: 7 wastes"):
        for waste in WASTES:
            st.markdown(f"**{waste.name}** — {waste.description}")

    with st.form("waste_form"):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Waste category", [w.name for w in WASTES])
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

    summary = (
        log_df.groupby("Waste", as_index=False)["Occurrences"].sum().sort_values(
            "Occurrences", ascending=False
        )
    )

    col_chart, col_table = st.columns((2, 1))
    with col_chart:
        st.subheader("Occurrences by waste")
        st.bar_chart(summary.set_index("Waste"))
    with col_table:
        st.subheader("Latest entries")
        st.dataframe(
            log_df.sort_values(["Recorded", "Occurrences"], ascending=[False, False]).head(8),
            use_container_width=True,
        )

    top_waste = summary.iloc[0]
    st.info(
        f"{top_waste['Waste']} is currently the largest source of waste with "
        f"{top_waste['Occurrences']} occurrences logged. Facilitate a root cause session and align "
        "kaizen ideas accordingly."
    )

    st.caption(
        "Export the table from the context menu to share with leadership or to support PDCA reviews."
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
    st.dataframe(
        ideas_df.sort_values(["Status", "Leverage score"], ascending=[True, False]),
        use_container_width=True,
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


PAGE_RENDERERS = {
    "Overview": render_overview,
    "Takt time": render_takt_time_calculator,
    "Waste tracker": render_waste_tracker,
    "Kaizen planner": render_kaizen_planner,
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
