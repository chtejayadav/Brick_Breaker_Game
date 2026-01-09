import streamlit as st
import time

st.set_page_config(page_title="Brick Breaker", layout="centered")

WIDTH = 40
HEIGHT = 18

# ---------- RESET GAME ----------
def reset_game():
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT - 4
    st.session_state.dx = 1
    st.session_state.dy = -1
    st.session_state.paddle = WIDTH // 2
    st.session_state.bricks = [(x, y) for y in range(2, 6) for x in range(5, WIDTH - 5)]
    st.session_state.game_over = False

# ---------- INIT ----------
if "ball_x" not in st.session_state:
    reset_game()

# ---------- UI ----------
st.title("🧱 Brick Breaker Game")

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    if st.button("⬅ LEFT"):
        st.session_state.paddle = max(2, st.session_state.paddle - 2)

with col2:
    if st.button("🔄 RESTART"):
        reset_game()

with col3:
    if st.button("RIGHT ➡"):
        st.session_state.paddle = min(WIDTH - 3, st.session_state.paddle + 2)

# ---------- GAME LOGIC ----------
if not st.session_state.game_over:
    st.session_state.ball_x += st.session_state.dx
    st.session_state.ball_y += st.session_state.dy

# Wall collision
if st.session_state.ball_x <= 1 or st.session_state.ball_x >= WIDTH - 2:
    st.session_state.dx *= -1

if st.session_state.ball_y <= 1:
    st.session_state.dy *= -1

# Paddle collision
if (
    st.session_state.ball_y == HEIGHT - 3
    and abs(st.session_state.ball_x - st.session_state.paddle) <= 2
):
    st.session_state.dy *= -1

# Brick collision
for brick in st.session_state.bricks[:]:
    if (st.session_state.ball_x, st.session_state.ball_y) == brick:
        st.session_state.bricks.remove(brick)
        st.session_state.dy *= -1
        break

# Game over
if st.session_state.ball_y >= HEIGHT:
    st.session_state.game_over = True

# ---------- DRAW BOARD ----------
board = []
for y in range(HEIGHT):
    row = ""
    for x in range(WIDTH):
        if (x, y) in st.session_state.bricks:
            row += "█"
        elif x == st.session_state.ball_x and y == st.session_state.ball_y:
            row += "●"
        elif y == HEIGHT - 2 and
