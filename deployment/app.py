import streamlit as st
from streamlit_autorefresh import st_autorefresh

from snake_game import SnakeGame
from renderer import render
from inference import SnakeAgent
from state_extractor import get_state

st.set_page_config(layout="wide")

@st.cache_resource
def load_agent():
    return SnakeAgent()

agent = load_agent()

# ---------- SESSION STATE ----------
if "game" not in st.session_state:
    st.session_state.game = SnakeGame()
    st.session_state.running = False
    st.session_state.score = 0

game = st.session_state.game

# ---------- LAYOUT ----------
col1, col2 = st.columns([3, 1], gap="small")

with col1:
    st.markdown("## Deep Q-Learning Snake Agent")
    game_slot = st.empty()

with col2:
    start = st.button("Start AI")
    reset = st.button("Reset")
    speed = st.slider("Speed", 1, 10, 3)

# ---------- CONTROLS ----------
if start:
    st.session_state.game = SnakeGame()
    st.session_state.running = True
    st.session_state.score = 0

if reset:
    st.session_state.game = SnakeGame()
    st.session_state.running = False
    st.session_state.score = 0

# ---------- AUTO REFRESH ----------
if st.session_state.running:
    st_autorefresh(interval=200, key="snake_refresh")  # ~5 FPS

# ---------- GAME STEP ----------
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

# ---------- RENDER ----------
frame = render(game)

game_slot.image(
    frame,
    width=640,
    caption=f"Score: {st.session_state.score}"
)
