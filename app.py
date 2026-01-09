import streamlit as st
import time
from streamlit.components.v1 import html

st.set_page_config(page_title="Brick Breaker", layout="wide")

# Game size (bigger display)
WIDTH = 60
HEIGHT = 22

# ----------------- SESSION STATE INIT -----------------
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.level = 1
    st.session_state.paddle = WIDTH // 2
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT - 4
    st.session_state.dx = 1
    st.session_state.dy = -1
    st.session_state.bricks = []
    st.session_state.game_over = False
    st.session_state.key = None


# ----------------- LEVEL SETUP -----------------
def setup_level(level):
    bricks = []
    rows = level + 2
    cols = 12 + level * 2
    start_x = (WIDTH - cols) // 2

    for r in range(rows):
        for c in range(cols):
            bricks.append((start_x + c, r + 2))
    return bricks


if not st.session_state.bricks:
    st.session_state.bricks = setup_level(st.session_state.level)

# ----------------- KEYBOARD INPUT -----------------
html(
    """
    <script>
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            window.parent.postMessage('LEFT', '*');
        }
        if (e.key === 'ArrowRight') {
            window.parent.postMessage('RIGHT', '*');
        }
    });
    </script>
    """,
    height=0,
)

# Receive key input
key = st.experimental_get_query_params().get("key", [None])[0]
if key:
    st.session_state.key = key

# JS → Streamlit bridge
html(
    """
    <script>
    window.addEventListener("message", (event) => {
        const key = event.data;
        const url = new URL(window.location);
        url.searchParams.set("key", key);
        window.location.href = url.toString();
    });
    </script>
    """,
    height=0,
)

# ----------------- MOVE PADDLE -----------------
if st.session_state.key == "LEFT":
    st.session_state.paddle = max(2, st.session_state.paddle - 2)

if st.session_state.key == "RIGHT":
    st.session_state.paddle = min(WIDTH - 3, st.session_state.paddle + 2)

st.session_state.key = None

# ----------------- BALL MOVEMENT -----------------
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
    bx, by = brick
    if st.session_state.ball_x == bx and st.session_state.ball_y == by:
        st.session_state.bricks.remove(brick)
        st.session_state.dy *= -1
        break

# ----------------- LEVEL COMPLETE -----------------
if not st.session_state.bricks:
    if st.session_state.level < 5:
        st.session_state.level += 1
        st.session_state.bricks = setup_level(st.session_state.level)
        st.session_state.ball_x = WIDTH // 2
        st.session_state.ball_y = HEIGHT - 4
        st.session_state.dy = -1
        st.success(f"🎉 Level {st.session_state.level - 1} Complete!")
        time.sleep(1)
    else:
        st.balloons()
        st.success("🏆 All 5 Levels Completed!")
        st.session_state.game_over = True

# Game over
if st.session_state.ball_y >= HEIGHT:
    st.error("❌ Game Over")
    st.session_state.game_over = True

# ----------------- DRAW GAME -----------------
board = []
for y in range(HEIGHT):
    row = ""
    for x in range(WIDTH):
        if (x, y) in st.session_state.bricks:
            row += "█"
        elif x == st.session_state.ball_x and y == st.session_state.ball_y:
            row += "●"
        elif y == HEIGHT - 2 and abs(x - st.session_state.paddle) <= 2:
            row += "═"
        else:
            row += " "
    board.append(row)

st.markdown(
    f"""
    <div style="font-family: monospace; font-size:18px; background:#000; color:#0f0; padding:15px">
    {'<br>'.join(board)}
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"### 🎯 Level: {st.session_state.level}  |  ⬅️ ➡️ Use Arrow Keys")

# ----------------- REFRESH -----------------
if not st.session_state.game_over:
    time.sleep(0.08)
    st.rerun()
