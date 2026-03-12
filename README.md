# A* Tutorial Effort (Codex Version)

I completed the assignment using Codex as an alternative to Unity and produced a creative A* pathfinding artifact.

## Files
- `astar_tutorial_effort.py` — A complete A* implementation on a 2D grid with:
  - Priority-queue open set (`heapq`)
  - Manhattan heuristic
  - Path reconstruction
  - A creative "spiral gate" level
  - ASCII visualization for easy upload/evidence
- `wordle_fsm.py` — existing FSM-based Wordle assignment file retained from previous work.

## Run
```bash
python3 astar_tutorial_effort.py
```

## What this demonstrates
- Core A* concepts from the tutorial flow:
  - Open list / frontier
  - `g` cost from start
  - `h` heuristic to goal
  - `f = g + h` prioritization
  - Parent tracking (`came_from`) and final path build
- A creative extension beyond a plain shortest-path test: a patterned maze map rendered as text output.

## Sample output shape
`S` = Start, `G` = Goal, `#` = Wall, `*` = Path, `.` = Empty.

(Your path should be visible as `*` characters from `S` to `G` when run.)
