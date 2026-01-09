import streamlit as st
import time

st.set_page_config(page_title="Brick Breaker", layout="centered")

WIDTH = 30
HEIGHT = 15

# Initialize session state
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.paddle = WIDTH // 2
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT - 3
    st.session_state.dx = 1
    st.session_state.dy = -1
    st.session_state.bricks = []
    st.session_state.game_over = False

# Setup bricks per level
def setup_level(level):
    rows = level + 1
    bricks = []
    for r in range(rows):
        for c in range(5 + level):
            bricks.append((c * 2 + 2, r + 1))
    return bricks

if not st.session_state.bricks:
    st.session_state.bricks = setup_level(st.session_state.level)

st.title("🧱 Brick Breaker Game")
st.write(f"### Level {st.session_state.level}")

# Controls
col1, col2, col3 = st.columns(3)
if col1.button("⬅ Left"):
    st.session_state.paddle = max(1, st.session_state.paddle - 1)

if col3.button("Right ➡"):
    st.session_state.paddle = min(WIDTH - 2, st.session_state.paddle + 1)

# Move ball
if not st.session_state.game_over:
    st.session_state.ball_x += st.session_state.dx
    st.session_state.ball_y += st.session_state.dy

# Wall collision
if st.session_state.ball_x <= 0 or st.session_state.ball_x >= WIDTH:
    st.session_state.dx *= -1

if st.session_state.ball_y <= 0:
    st.session_state.dy *= -1

# Paddle collision
if (
    st.session_state.ball_y == HEIGHT - 2
    and abs(st.session_state.ball_x - st.session_state.paddle) <= 1
):
    st.session_state.dy *= -1

# Brick collision
for brick in st.session_state.bricks[:]:
    bx, by = brick
    if st.session_state.ball_x == bx and st.session_state.ball_y == by:
        st.session_state.bricks.remove(brick)
        st.session_state.dy *= -1
        break

# Level complete
if not st.session_state.bricks:
    if st.session_state.level < 5:
        st.session_state.level += 1
        st.session_state.bricks = setup_level(st.session_state.level)
        st.session_state.ball_x = WIDTH // 2
        st.session_state.ball_y = HEIGHT - 3
        st.session_state.dy = -1
        st.success("🎉 Level Up!")
        time.sleep(1)
    else:
        st.balloons()
        st.success("🏆 You completed all 5 levels!")
        st.session_state.game_over = True

# Game over
if st.session_state.ball_y > HEIGHT:
    st.error("❌ Game Over")
    st.session_state.game_over = True

# Draw game board
board = []
for y in range(HEIGHT):
    row = ""
    for x in range(WIDTH):
        if (x, y) in st.session_state.bricks:
            row += "■"
        elif x == st.session_state.ball_x and y == st.session_state.ball_y:
            row += "●"
        elif y == HEIGHT - 1 and abs(x - st.session_state.paddle) <= 1:
            row += "━"
        else:
            row += " "
    board.append(row)

st.text("\n".join(board))

# Refresh
if not st.session_state.game_over:
    time.sleep(0.15)
    st.rerun()
