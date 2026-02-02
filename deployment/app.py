import streamlit as st
import time

from snake_game import SnakeGame
from renderer import render
from inference import SnakeAgent
from state_extractor import get_state

st.set_page_config(layout="wide")

# Load model ONCE
@st.cache_resource
def load_agent():
    return SnakeAgent()

agent = load_agent()

# Session state
if "game" not in st.session_state:
    st.session_state.game = SnakeGame()
    st.session_state.running = False

game = st.session_state.game

st.title("Deep Q-Learning Snake Agent")

col1, col2 = st.columns([3, 1])

with col2:
    if st.button("Start AI"):
        st.session_state.game = SnakeGame()
        st.session_state.running = True

    if st.button("Reset"):
        st.session_state.game = SnakeGame()
        st.session_state.running = False

    speed = st.slider("Speed", 1, 20, 20)

with col1:
    if st.session_state.running:
        state = get_state(game)

        action = [0, 0, 0]
        action[agent.act(state)] = 1

        _, done, score = game.step(action)
        frame = render(game)

        st.image(frame, caption=f"Score: {score}")

        if done:
            st.session_state.running = False

        delay = 1 / speed
        time.sleep(delay)
        st.rerun()