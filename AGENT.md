# Agent Checklist — SnakeGame

Short checklist for hands-on edits and verification.

- Run the game locally
  - Install deps: `pip install -r requirements.txt`
  - Start: `python tanchishe.py`

- Quick debug workflow
  1. Reproduce the issue in-game (use `A` to toggle auto mode, arrow keys for manual).
 2. Add minimal `print()` statements in `auto_eat_food()` or `update()` to inspect `current_path`, `snake_set`, `direction`.
 3. Attach VS Code debugger to `tanchishe.py` and set breakpoints in `update()` / `auto_eat_food()`.

- Safe refactor pattern for AI/pathfinding
  1. Preserve `current_path` cache behaviour: only recompute when `food_pos` changes or path is empty.
 2. Keep `snake_set = set(snake[:-1])` when checking BFS collisions (tail exclusion).
 3. After changes, run the game and visually verify no new frame rate regressions.

- PR checklist for small changes
  - Change limited to `tanchishe.py` unless adding assets.
  - Run locally and confirm UI text renders (requires fonts in `fonts/`).
  - Keep edits minimal and preserve existing function signatures.

If you want, I can: expand tests, split `tanchishe.py` into modules, or add a small automated smoke test script.
