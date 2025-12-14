<!--
Purpose: concise guidance so AI coding agents are productive in this repo.
Keep this file short (20–50 lines). Update the 'Repo-specific details' section
after scanning the codebase so the instructions include concrete file and
command examples.
-->
# Copilot / AI Agent Instructions

Purpose: Help an AI coding agent quickly become productive in this repository.

## 1) Big picture
- **Project**: Snake Game (贪吃蛇游戏) - a classic arcade game with auto-play AI
- **Framework**: pygame-zero (`pgzrun`) - lightweight game development library
- **Core features**:
  - Manual mode: player controls snake with arrow keys (← → ↑ ↓)
  - Auto mode: BFS pathfinding algorithm automatically guides snake to food (press A to toggle)
  - Performance optimizations: path caching, snake body set caching to reduce CPU/memory
  - Win condition: grow snake to length 100; lose condition: hit wall or self
- **Primary entrypoint**: `tanchishe.py` (single-file game)

## 2) Key files & directories to read first
- [tanchishe.py](tanchishe.py) — single-file game; contains game state, AI pathfinding, rendering, input handling
  - `auto_eat_food()` — BFS algorithm to find shortest path to food
  - `move_snake()` — snake movement and collision detection logic
  - `update()` — main game loop; calls auto-eat or handles manual input
  - `draw()` — renders game board, snake, food, UI (scores, mode indicator)
  - `on_key_down()` — keyboard input dispatch (arrows, A=auto, R=restart, ESC=menu)

## 3) Important patterns and conventions
- **Global state**: game variables (`snake`, `food_pos`, `direction`, `score`) are module-level globals updated by `reset_game()`, `move_snake()`, `auto_eat_food()`
- **Game state machine**: `game_started` + `game_over` + `wingame` flags control flow (start screen → play → end screen → restart)
- **Performance optimizations** (documented in file header):
  - Path caching: `current_path` list reused across frames; only recalculated when empty or food moves
  - Body caching: `snake_set` avoids re-creating `snake[:-1]` slices on every pathfind check
  - Movement throttle: `MOVEMENT_INTERVAL = 2` limits movement to every Nth frame (not every update call)
- **Direction handling**: `direction` is current; `next_direction` buffers next move to prevent reverse-into-self
- **Color scheme** (BACKGROUND, SNAKE_HEAD, SNAKE_BODY, FOOD, GRID, TEXT defined at top)

## 4) Build / run / test commands
- **Install dependencies**: `pip install pygame-zero` (requires pygame-zero; standard pygame may not work)
- **Run game**: `python tanchishe.py` or `pgzrun tanchishe.py`
- **Controls**: Arrow keys to move (manual mode); A key to toggle auto mode; R to restart; SPACE to start; ESC to exit
- **Game parameters**: Grid 40×30 cells (800×600 px, 20px cell size), 10 FPS base, snake moves every 2 frames (5 effective FPS)

## 5) CI / checks (what the agent should run locally before PRs)
- No formal CI configured (single-file project)
- **Manual checks**: Run `python tanchishe.py`, verify both manual and auto modes work, check for frame rate and collisions

## 6) Commit / PR guidelines for the agent
- Branch naming: optional for single-file project; use `feat/<feature>`, `fix/<bug>` if branching
- Commit style: short title (≤50 chars) describing the change (e.g., "Add path visualization", "Optimize BFS heuristic")
- PR description: include **what changed** (e.g., new feature, performance fix), **testing steps** (manual play test in both modes), and **before/after behavior**

## 7) How to find repo-specific examples to update this file
- Game loop: see `update()` and `draw()` functions for frame-timing and rendering
- AI logic: `auto_eat_food()` uses BFS with deque; `move_snake()` handles collision and growth
- UI/rendering: `draw_snake()` places eyes based on `direction`; `draw_game_over_screen()` overlays results
- Input handling: `on_key_down()` dispatcher; note how A toggles `auto_mode` without blocking other keys
- Constants: grid size, colors, movement interval—all at module top for easy tweaking

## 8) When merging with an existing `.github/copilot-instructions.md`
- Preserve any project-specific command blocks and the "Key files" list.
- If this file already contains accurate commands, prefer those over generic ones.

---

**Next steps if improving this project**:
- Add difficulty levels (speed, grid size)
- Implement pathfinding heuristics (A*, avoiding dead ends)
- Add food spawning strategies (random vs. weighted)
- Performance profiling: measure BFS calls, cache hit ratio, frame time
- Unit tests: mock game state and verify pathfinding correctness
