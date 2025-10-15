"""Streamlit app for a simple math practice game."""

import random
from dataclasses import dataclass

import streamlit as st


@dataclass
class MathProblem:
    """Container for a single math problem."""

    prompt: str
    answer: int


DIFFICULTIES = {
    "Easy": (0, 10),
    "Medium": (0, 20),
    "Hard": (0, 50),
}


OPERATIONS = {
    "Addition (+)": "+",
    "Subtraction (-)": "-",
    "Multiplication (×)": "*",
}


def generate_problem(difficulty: str, allowed_ops: list[str]) -> MathProblem:
    """Generate a random math problem given the difficulty and allowed operations."""

    if not allowed_ops:
        raise ValueError("At least one operation is required to generate a problem.")

    low, high = DIFFICULTIES[difficulty]
    a = random.randint(low, high)
    b = random.randint(low, high)
    symbol = OPERATIONS[random.choice(allowed_ops)]

    if symbol == "+":
        answer = a + b
    elif symbol == "-":
        answer = a - b
    else:  # symbol == "*"
        answer = a * b

    prompt = f"{a} {symbol} {b}"
    return MathProblem(prompt=prompt, answer=answer)


def init_state(difficulty: str, operations: list[str]) -> None:
    """Initialize session state for the game."""

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "problem" not in st.session_state:
        st.session_state.problem = generate_problem(difficulty, operations)
    if "feedback" not in st.session_state:
        st.session_state.feedback = ""


def new_problem(difficulty: str, operations: list[str]) -> None:
    """Reset the current problem and clear feedback."""

    st.session_state.problem = generate_problem(difficulty, operations)
    st.session_state.feedback = ""


def update_score(is_correct: bool) -> None:
    """Update score counters based on correctness."""

    st.session_state.attempts += 1
    if is_correct:
        st.session_state.score += 1
        st.session_state.streak += 1
    else:
        st.session_state.streak = 0


def main() -> None:
    st.set_page_config(page_title="Math Practice Game", layout="wide")
    st.title("🔢 Math Practice Game")
    st.write(
        "Sharpen your mental math skills with quick challenges. Choose the operations and "
        "difficulty that suit you, then enter the correct answer to boost your score!"
    )

    st.sidebar.header("Game Settings")
    difficulty = st.sidebar.selectbox("Difficulty", list(DIFFICULTIES.keys()))
    operation_choices = st.sidebar.multiselect(
        "Operations",
        list(OPERATIONS.keys()),
        default=list(OPERATIONS.keys()),
    )

    init_state(difficulty, operation_choices)

    if st.sidebar.button("New Challenge", use_container_width=True):
        new_problem(difficulty, operation_choices)

    if not operation_choices:
        st.warning("Select at least one operation to play the game.")
        return

    st.subheader("Current Challenge")
    st.markdown(
        f"<div style='font-size:2rem; font-weight:600;'>{st.session_state.problem.prompt}</div>",
        unsafe_allow_html=True,
    )

    with st.form("answer_form"):
        answer_input = st.text_input("Your answer", value="")
        submitted = st.form_submit_button("Check Answer", use_container_width=True)

    if submitted:
        try:
            guess = int(answer_input)
        except ValueError:
            st.session_state.feedback = "❗ Please enter a whole number."
        else:
            is_correct = guess == st.session_state.problem.answer
            update_score(is_correct)
            if is_correct:
                st.session_state.feedback = "✅ Correct! Nice work."
                new_problem(difficulty, operation_choices)
            else:
                st.session_state.feedback = (
                    f"❌ Not quite. The correct answer was {st.session_state.problem.answer}."
                )

    if st.session_state.feedback:
        st.info(st.session_state.feedback)

    st.subheader("Scoreboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", st.session_state.score)
    col2.metric("Attempts", st.session_state.attempts)
    col3.metric("Streak", st.session_state.streak)

    st.caption(
        "Tip: use the settings on the left to adjust the difficulty or operations at any time."
    )


if __name__ == "__main__":
    main()
