# Snake Game (贪吃蛇游戏)

A note about CI status (replace OWNER/REPO with your GitHub repo)

```
![Smoke Test](https://github.com/OWNER/REPO/actions/workflows/smoke.yml/badge.svg)
```

A classic arcade game built with Python and `pygame-zero` (`pgzrun`).

## Features
- **Manual Mode**: Control the snake using arrow keys (← → ↑ ↓).
- **Auto Mode**: Toggle auto-play with the `A` key, which uses BFS pathfinding to guide the snake to food.
- **Win/Lose Conditions**:
  - Win: Grow the snake to length 100.
  - Lose: Hit the wall or collide with yourself.

## Requirements
- Python 3.x
- `pygame-zero` (`pip install pgzero`)

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the game:
   ```bash
   python tanchishe.py
   ```

## Controls
- Arrow keys (← → ↑ ↓): Move the snake.
- `A` key: Toggle auto-play mode.

## Performance Optimizations
- Path caching for BFS.
- Snake body set caching to reduce CPU/memory usage.