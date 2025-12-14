# Guidance for AI coding agents — SnakeGame

Purpose
- Help an AI agent be productive quickly in this repository: a single-file Python/pgzero Snake game.

Big picture
- Main runtime: `tanchishe.py` — a pgzero app using `update()`, `draw()`, `on_key_down()` and `pgzrun.go()`.
- Assets: `fonts/` contains font files referenced by name (e.g. "simhei.ttf").
- Dependencies: lightweight; see `requirements.txt` (uses `pgzero`).

Key implementation notes and patterns
- Single-file architecture: most logic lives in `tanchishe.py` (game state, rendering, input, pathfinding).
- Auto-play uses BFS in `auto_eat_food()` with explicit caching: `current_path` (path reuse) and `snake_set` (body membership).
  - When editing pathfinding keep cache invalidation rules: clear `current_path` on food change and pop walked nodes as head advances.
- Movement is frame-throttled: constants at top (`CELL_SIZE`, `GRID_WIDTH`, `GRID_HEIGHT`, `MOVEMENT_INTERVAL`, `FPS`) control timing and grid.
- UI text uses explicit font names — keep fonts in `fonts/` and reference identical filenames.

Developer workflows (how to run/debug)
- Install deps: `pip install -r requirements.txt`.
- Run locally: `python tanchishe.py` (pgzero app; `pgzrun.go()` runs the loop).
- Debugging: use prints or VS Code debugger attached to `tanchishe.py`; breakpoints in `update()`/`auto_eat_food()` are effective.

Conventions to follow
- Keep game constants at file top; changes to grid size must update related derived constants (`GRID_WIDTH`, `GRID_HEIGHT`).
- Avoid heavy imports inside per-frame logic — the code already moved `deque` import to top for performance.
- Preserve the caching strategy when modifying auto mode — removing caches will cause major performance regressions.

Integration and touchpoints
- Changing visuals: edit draw_* functions in `tanchishe.py`.
- Changing AI/autoplay: edit `auto_eat_food()` and respect `current_path`/`snake_set` semantics.
- Assets: update `fonts/` for custom fonts; use the same filename strings used in the code.

What to look for when changing behavior
- If you change `MOVEMENT_INTERVAL` or `FPS`, verify snake speed remains playable and pathfinding cadence still valid.
- When modifying grid or cell size, visually test collisions and food placement (use `generate_food()` logic).

Examples & small rules
- Cache invalidation: `current_path` is intentionally cleared in `generate_food()` when `food_pos` changes — preserve that behavior when refactoring pathfinding.
- Path consumption: `auto_eat_food()` assumes `current_path.pop(0)` is called as the head moves; do not remove this step or the head-index checks that avoid stale steps.
- Snake set semantics: `snake_set = set(snake[:-1])` excludes the tail because it may move this frame; preserve this when checking BFS collisions.
- Quick local test: add temporary logs inside `auto_eat_food()` (for example `print('path', len(current_path), 'snake', len(snake_set))`) and run:

```bash
pip install -r requirements.txt
python tanchishe.py
```

If merging with an existing .github/copilot-instructions.md
- Preserve run commands and any project-specific patterns above. Merge any extra examples from that file into the relevant sections (Big picture, Key patterns, Workflows).

Files to inspect first
- `tanchishe.py` — main logic and most important file.
- `README.md` — run instructions and feature summary.
- `requirements.txt` — dependency list.

If anything in this guidance is unclear or you want more depth (testing, refactors, or split into modules), ask for specifics.

Annotated example: instrumenting `auto_eat_food()`
 - Goal: add temporary, low-overhead logging to inspect BFS behaviour and cache usage.
 - Safe edits: add `print()` calls only inside `auto_eat_food()`; avoid importing `tanchishe.py` elsewhere because `pgzrun.go()` runs on import.
 - Example (insert near top of `auto_eat_food()`):

```python
# inside auto_eat_food(), after computing head and before using current_path
print(f"AUTO DEBUG head={head} food={food_pos} path_len={len(current_path)} snake_len={len(snake)}")
```

 - What to watch for:
   - `path_len` should decrease as the snake advances (path nodes popped).
   - If `path_len` is repeatedly 0 while `food_pos` unchanged, BFS may be failing or being recomputed too often.
   - If `snake_set` size seems wrong, confirm `snake_set = set(snake[:-1])` is preserved (tail exclusion).

 - Quick test run:

```bash
pip install -r requirements.txt
python tanchishe.py
```

Remove the `print()` statements after diagnosing to avoid console spam.
