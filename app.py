import streamlit as st
import numpy as np
import random
import time
from PIL import Image, ImageDraw

# Generate a simple maze
def generate_maze(size):
    maze = np.ones((size, size), dtype=int)
    for i in range(1, size-1, 2):
        for j in range(1, size-1, 2):
            maze[i, j] = 0
            if random.choice([True, False]):
                maze[i+1, j] = 0
            else:
                maze[i, j+1] = 0
    return maze

# Render the maze as an image
def render_maze(maze, player_pos):
    size = len(maze)
    cell_size = 30
    img = Image.new("RGB", (size * cell_size, size * cell_size), "#f4f4f4")
    draw = ImageDraw.Draw(img)
    
    for y in range(size):
        for x in range(size):
            if maze[y, x] == 1:
                draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill="#333333")
    
    draw.rectangle([player_pos[1] * cell_size, player_pos[0] * cell_size,
                    (player_pos[1] + 1) * cell_size, (player_pos[0] + 1) * cell_size], fill="#ff4d4d")
    return img

# Initialize session state
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.maze_size = 11
    st.session_state.maze = generate_maze(st.session_state.maze_size)
    st.session_state.player_pos = [1, 1]

# Game Controls
def move_player(direction):
    x, y = st.session_state.player_pos
    if direction == "up" and st.session_state.maze[x-1, y] == 0:
        st.session_state.player_pos[0] -= 1
    elif direction == "down" and st.session_state.maze[x+1, y] == 0:
        st.session_state.player_pos[0] += 1
    elif direction == "left" and st.session_state.maze[x, y-1] == 0:
        st.session_state.player_pos[1] -= 1
    elif direction == "right" and st.session_state.maze[x, y+1] == 0:
        st.session_state.player_pos[1] += 1
    
    # Check if reached the end
    if st.session_state.player_pos == [st.session_state.maze_size-2, st.session_state.maze_size-2]:
        st.success(f"Level {st.session_state.level} Complete!")
        time.sleep(1)
        st.session_state.level += 1
        st.session_state.maze_size = min(21, 11 + st.session_state.level // 5)
        st.session_state.maze = generate_maze(st.session_state.maze_size)
        st.session_state.player_pos = [1, 1]

# Streamlit UI
st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title(f"🎮 Maze Solver - Level {st.session_state.level}")

game_image = render_maze(st.session_state.maze, st.session_state.player_pos)
st.image(game_image, caption="Find your way to the exit!", use_column_width=True)

st.markdown('<div class="button-container">', unsafe_allow_html=True)
st.button("⬆️ Up", on_click=move_player, args=("up",))
st.button("⬅️ Left", on_click=move_player, args=("left",))
st.button("➡️ Right", on_click=move_player, args=("right",))
st.button("⬇️ Down", on_click=move_player, args=("down",))
st.markdown('</div>', unsafe_allow_html=True)
