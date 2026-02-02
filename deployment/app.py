import streamlit as st
import time

from snake_game import SnakeGame
from inference import SnakeAgent
from state_extractor import get_state
from renderer import render

st.set_page_config(layout="wide")

@st.cache_resource
def load_agent():
    return SnakeAgent()

agent = load_agent()

# -------- SESSION STATE --------
if "game" not in st.session_state:
    st.session_state.game = SnakeGame()
    st.session_state.running = False
    st.session_state.frame = None
    st.session_state.score = 0

game = st.session_state.game

# -------- LAYOUT --------
left, right = st.columns([3, 1], gap="small")

with left:
    st.markdown("## Deep Q-Learning Snake Agent")
    game_slot = st.empty()     # 🔒 ALWAYS EXISTS
    score_slot = st.empty()

with right:
    start = st.button("Start AI")
    reset = st.button("Reset")
    speed = st.slider("Speed", 1, 20, 10)

# -------- CONTROLS --------
if start:
    st.session_state.game = SnakeGame()
    st.session_state.running = True

if reset:
    st.session_state.game = SnakeGame()
    st.session_state.running = False
    st.session_state.frame = None
    st.session_state.score = 0

# -------- GAME STEP --------
if st.session_state.running:
    state = get_state(game)

    action = [0, 0, 0]
    action[agent.act(state)] = 1

    _, done, score = game.step(action)

    st.session_state.frame = render(game)
    st.session_state.score = score

    if done:
        st.session_state.running = False

    time.sleep(1 / speed)
    st.rerun()

# -------- RENDER (UNCONDITIONAL) --------
if st.session_state.frame is not None:
    game_slot.image(
        st.session_state.frame,
        width=640
    )
    score_slot.markdown(f"**Score:** {st.session_state.score}")
