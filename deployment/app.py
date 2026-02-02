import streamlit as st
import time

from snake_game import SnakeGame
from renderer import render
from inference import SnakeAgent
from state_extractor import get_state

st.set_page_config(layout="wide")

@st.cache_resource
def load_agent():
    return SnakeAgent()

agent = load_agent()

# ---------------- SESSION STATE ----------------
if "game" not in st.session_state:
    st.session_state.game = SnakeGame()
    st.session_state.running = False
    st.session_state.frame = None
    st.session_state.score = 0

game = st.session_state.game

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([3, 1], gap="small")

with col1:
    st.markdown("## Deep Q-Learning Snake Agent")
    game_slot = st.empty()
    score_slot = st.empty()

with col2:
    start = st.button("Start AI")
    reset = st.button("Reset")
    speed = st.slider("Game Speed (logic steps per frame)", 1, 10, 3)

# ---------------- CONTROLS ----------------
if start:
    st.session_state.game = SnakeGame()
    st.session_state.running = True

if reset:
    st.session_state.game = SnakeGame()
    st.session_state.running = False
    st.session_state.frame = None
    st.session_state.score = 0

# ---------------- GAME LOOP ----------------
MAX_FPS = 6  # hard Streamlit Cloud limit

if st.session_state.running:
    for _ in range(speed):  # logic speed
        state = get_state(game)

        action = [0, 0, 0]
        action[agent.act(state)] = 1

        _, done, score = game.step(action)
        st.session_state.score = score

        if done:
            st.session_state.running = False
            break

    st.session_state.frame = render(game)

    time.sleep(1 / MAX_FPS)
    st.rerun()

# ---------------- RENDER (ALWAYS) ----------------
if st.session_state.frame is None:
    st.session_state.frame = render(game)

game_slot.image(
    st.session_state.frame,
    width=640
)

score_slot.markdown(f"**Score:** {st.session_state.score}")
