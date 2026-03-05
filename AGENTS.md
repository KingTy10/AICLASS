# AGENTS.md

## Project Goal
Teach grid pathfinding by implementing:
- BFS using a queue (`collections.deque`)
- DFS using a stack (Python `list`, iterative)
- Path reconstruction with a parent map
- A small turn-based "Monster Chase" demo

## Rules for Codex
- Modify only existing files (`pathfinding.py`, `README.md`, `AGENTS.md`) unless explicitly told otherwise.
- Do not change required function signatures in `pathfinding.py`.
- DFS must be iterative (no recursion).
- BFS must use `collections.deque`.
- Use a `visited` set and `parent` dict for reconstruction.
- Keep changes minimal and keep `main()` runnable.

## Output Contract
Running `python pathfinding.py` must:
- run BFS and DFS on at least 2 maps
- print found/path length/visited count
- print rendered maps with overlays

## If Codex Goes Off-Track
Paste failing output and say:
"Follow AGENTS.md, minimal diff, and fix only <target issue>."
