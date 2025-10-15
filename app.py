"""Streamlit app for calculating Stardew Valley skill experience."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import streamlit as st


@dataclass(frozen=True)
class SkillAction:
    """Representation of an activity that grants experience."""

    label: str
    xp: int
    description: str | None = None


# Cumulative XP required to reach each level (level 0 -> 10)
LEVEL_XP_REQUIREMENTS: List[int] = [
    0,
    100,
    380,
    770,
    1_300,
    2_150,
    3_300,
    4_800,
    6_900,
    10_000,
    15_000,
]


SKILL_ACTIONS: Dict[str, List[SkillAction]] = {
    "Farming": [
        SkillAction("Harvest regular crop", 8, "Parsnip, Potatoes, etc."),
        SkillAction("Harvest quality crop", 16, "Silver/Gold/Iridium crops"),
        SkillAction("Milking / Shearing", 5),
        SkillAction("Petting animals", 5),
    ],
    "Mining": [
        SkillAction("Break stone node", 1),
        SkillAction("Break ore node", 5),
        SkillAction("Break gem node", 12),
        SkillAction("Slay cave monster", 3, "Dust Sprites, Slimes, etc."),
    ],
    "Foraging": [
        SkillAction("Gather forage item", 7),
        SkillAction("Chop tree", 12, "Full tree (no seeds)"),
        SkillAction("Chop stump/log", 25),
        SkillAction("Tapper collection", 8, "Syrup, resin, etc."),
    ],
    "Fishing": [
        SkillAction("Catch fish", 3),
        SkillAction("Perfect catch bonus", 15, "In addition to catch XP"),
        SkillAction("Collect crab pot", 5),
        SkillAction("Fish treasure chest", 5),
    ],
    "Combat": [
        SkillAction("Slay monster", 4, "Typical overworld enemy"),
        SkillAction("Slay boss/strong monster", 15),
        SkillAction("Use explosive", 1, "Bomb damage"),
        SkillAction("Reach deeper floor", 25, "First-time floor completion"),
    ],
}


def determine_level(total_xp: int) -> int:
    """Return the current level (0-10) for the provided cumulative XP."""

    for level, requirement in reversed(list(enumerate(LEVEL_XP_REQUIREMENTS))):
        if total_xp >= requirement:
            return level
    return 0


def xp_to_next_level(total_xp: int) -> int | None:
    """Calculate XP needed to reach the next level, or None if at level cap."""

    current_level = determine_level(total_xp)
    if current_level >= 10:
        return None
    next_requirement = LEVEL_XP_REQUIREMENTS[current_level + 1]
    return max(0, next_requirement - total_xp)


def render_sidebar(skill: str) -> tuple[int, Dict[str, int]]:
    """Render sidebar inputs and return current XP plus action counts."""

    st.sidebar.header("Skill & Progress")
    st.sidebar.write(
        "Enter your current experience and how many actions you plan to take."
    )
    current_xp = st.sidebar.number_input(
        "Current XP", min_value=0, max_value=LEVEL_XP_REQUIREMENTS[-1], value=0
    )

    st.sidebar.header("Actions")
    counts: Dict[str, int] = {}
    for action in SKILL_ACTIONS[skill]:
        counts[action.label] = st.sidebar.number_input(
            action.label,
            min_value=0,
            step=1,
            value=0,
            key=f"{skill}-{action.label}",
        )
    return current_xp, counts


def render_skill_selector() -> str:
    """Display the skill selector and return the selected skill."""

    st.sidebar.title("Stardew XP Calculator")
    skill = st.sidebar.selectbox("Skill", list(SKILL_ACTIONS.keys()))
    return skill


def calculate_total_gain(skill: str, counts: Dict[str, int]) -> int:
    """Compute the total XP gained for the selected skill."""

    actions = {action.label: action for action in SKILL_ACTIONS[skill]}
    return sum(actions[label].xp * quantity for label, quantity in counts.items())


def render_results(skill: str, gained_xp: int, current_xp: int, counts: Dict[str, int]) -> None:
    """Render metrics summarizing the player's progress."""

    new_total = current_xp + gained_xp
    current_level = determine_level(current_xp)
    new_level = determine_level(new_total)
    to_next_now = xp_to_next_level(current_xp)
    to_next_after = xp_to_next_level(new_total)

    st.header(f"{skill} Progress Overview")
    st.write(
        "Use this calculator to estimate how your planned actions will move you toward "
        "the next skill level. XP values reflect standard Stardew Valley mechanics." 
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Level", current_level)
    col2.metric("XP Gained", gained_xp)
    col3.metric("New Level", new_level)

    st.progress(min(new_total / LEVEL_XP_REQUIREMENTS[-1], 1.0))

    if to_next_now is None:
        st.success("You've already reached level 10! 🎉")
    else:
        st.info(
            f"Current XP to next level: {to_next_now}"
            + (
                f" — after actions you'll need {to_next_after} more XP."
                if to_next_after is not None
                else " — these actions will cap the skill!"
            )
        )

    if gained_xp:
        st.subheader("XP Breakdown")
        for action in SKILL_ACTIONS[skill]:
            quantity = counts.get(action.label, 0)
            if quantity:
                total = quantity * action.xp
                description = f" ({action.description})" if action.description else ""
                st.write(f"• **{action.label}** × {quantity} → {total} XP{description}")
    else:
        st.caption("Select action counts in the sidebar to see projected gains.")

    st.subheader("Level Requirements")
    st.table(
        {
            "Level": list(range(1, 11)),
            "Total XP": LEVEL_XP_REQUIREMENTS[1:],
        }
    )


def main() -> None:
    st.set_page_config(page_title="Stardew Valley XP Calculator", layout="wide")
    skill = render_skill_selector()
    current_xp, counts = render_sidebar(skill)
    gained_xp = calculate_total_gain(skill, counts)
    render_results(skill, gained_xp, current_xp, counts)


if __name__ == "__main__":
    main()
