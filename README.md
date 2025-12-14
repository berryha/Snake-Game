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

# PR Title
chore(ci): add AI agent guidance, smoke tests, and CI workflow

## Description
Adds developer and AI agent productivity tools for the SnakeGame project:

### Changes
- **`.github/copilot-instructions.md`** — Comprehensive guide for AI coding agents covering architecture, caching patterns, developer workflows, and debugging strategies.
- **`AGENT.md`** — Quick checklist for hands-on edits: run/debug workflow, safe refactoring patterns, and PR validation steps.
- **`smoke_test.py`** — Headless syntax and AST validation script (no pgzrun import, safe for CI).
- **`.github/workflows/smoke.yml`** — GitHub Actions workflow to run `smoke_test.py` on push and PRs.
- **`README.md`** — Added CI badge template for workflow status visibility.

### Why
- AI agents (Copilot, Claude, Cursor) can now quickly understand project structure and conventions without multiple file reads.
- Developers get fast pre-PR feedback via automated smoke tests.
- CI catches basic syntax/structure issues early without requiring pgzero or X11 display.

### Testing
- `smoke_test.py` passes locally (syntax, required functions, font references all validated).
- Workflow runs on Linux with Python 3.x; adjust if needed for other runtimes.

### Usage
After merge, replace `OWNER/REPO` in the README badge with your actual repository path. The workflow will run automatically on future pushes.

**Follow-up items** (optional):
- Add flake8/black linting to the workflow if desired.
- Expand `AGENT.md` with example refactoring steps for specific game features.