"""Headless smoke-test for SnakeGame.

Performs static checks only (no imports of `tanchishe.py` to avoid launching `pgzrun.go()`).
Checks performed:
- Syntax check (compile)
- AST checks: presence of `update`, `draw`, `on_key_down` functions
- Presence of `pgzrun.go()` call (warns but does not execute)
- Fonts referenced exist in `fonts/` (if any literal strings found)

Exit codes: 0=pass, 1=fail
"""
import ast
import os
import sys
import re

ROOT = os.path.dirname(__file__)
GAME_FILE = os.path.join(ROOT, "tanchishe.py")
FONTS_DIR = os.path.join(ROOT, "fonts")


def read_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def syntax_check(source, filename):
    try:
        compile(source, filename, "exec")
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"


def ast_checks(source):
    tree = ast.parse(source)
    funcs = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}

    required = ["update", "draw", "on_key_down"]
    missing = [f for f in required if f not in funcs]

    # detect pgzrun.go() call
    found_pgzrun_go = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "go":
                if isinstance(func.value, ast.Name) and func.value.id == "pgzrun":
                    found_pgzrun_go = True
    return missing, found_pgzrun_go


def find_font_literals(source):
    # naive: find .ttf/.otf occurrences in source string literals
    literals = re.findall(r"\"([^\"]+\.(?:ttf|otf))\"|'([^']+\.(?:ttf|otf))'", source)
    fonts = set()
    for a, b in literals:
        fonts.add(a or b)
    return sorted(fonts)


def main():
    if not os.path.exists(GAME_FILE):
        print(f"ERROR: {GAME_FILE} not found.")
        sys.exit(1)

    src = read_source(GAME_FILE)

    ok, err = syntax_check(src, GAME_FILE)
    if not ok:
        print("[FAIL] Syntax check failed:", err)
        sys.exit(1)
    print("[OK] Syntax check passed.")

    missing, has_pgzrun = ast_checks(src)
    if missing:
        print("[FAIL] Missing required function(s):", ", ".join(missing))
        sys.exit(1)
    print("[OK] Required functions present: update, draw, on_key_down.")

    if has_pgzrun:
        print("[WARN] Detected call to pgzrun.go() in source. Tests avoid importing the module to prevent launching the game.")

    fonts = find_font_literals(src)
    if fonts:
        missing_fonts = [f for f in fonts if not os.path.exists(os.path.join(FONTS_DIR, f))]
        if missing_fonts:
            print("[WARN] Missing font files in fonts/:", ", ".join(missing_fonts))
        else:
            print("[OK] Referenced font files present in fonts/.")
    else:
        print("[INFO] No font file literals found in source.")

    print("Smoke test completed successfully.")
    sys.exit(0)


if __name__ == '__main__':
    main()
