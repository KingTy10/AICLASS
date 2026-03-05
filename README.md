# BFS + DFS Grid Pathfinding (Python Console)

## Run
```bash
python pathfinding.py
```

## Files
- `pathfinding.py` — BFS/DFS implementation, rendering, examples, and optional game loop.
- `AGENTS.md` — repo rules to keep Codex constrained and predictable.
- `README.md` — run instructions and reflection.

## What the script prints
For each built-in map, it runs both BFS and DFS and prints:
- whether a path was found
- path length
- number of visited nodes
- rendered map with overlays (`*` for final path, `·` for visited floor tiles)

## Reflection

### 1) A map where DFS path is longer than BFS
`EXAMPLE_MAP_3` is intentionally maze-like with misleading branches. On that map, BFS typically returns a shorter route from `S` to `G`, while DFS can return a longer route because it follows one branch deeply before backtracking.

The exact DFS path can vary with neighbor order. In this project, neighbors are generated in the order up, right, down, left and DFS pushes reversed neighbors to keep runs deterministic. This still does **not** make DFS shortest-path; it only makes it reproducible.

### 2) Visited count comparison
BFS often visits many nodes in a wavefront before reaching the goal, especially when the goal is far away or behind bottlenecks. DFS can visit fewer nodes in some layouts if it gets "lucky" and dives toward the goal quickly, but it can also visit many dead-end nodes when it gets unlucky.

In short:
- BFS: more systematic exploration by depth layer
- DFS: branch-first exploration, sensitive to ordering

### 3) Why BFS guarantees shortest path here, and DFS does not
This grid is unweighted (every move has equal cost = 1). BFS explores nodes in increasing distance from `S`:
- distance 0, then distance 1, then distance 2, etc.

Therefore, the first time BFS reaches `G`, it has found a path with minimum number of steps.

DFS does not expand by distance layers. It follows one branch as deep as possible first. The first time DFS reaches `G` could be via a long detour, even if a much shorter path exists elsewhere.

### 4) Simple game idea: Monster Chase (Turn-Based)
Implemented in `pathfinding.py` as `game_loop(mode="BFS"|"DFS")`.

Rules:
- Map has `P` (player), `M` (monster), `#` (walls), `.` (floor), `G` (exit)
- Each turn:
  - player moves with WASD (cannot move through walls)
  - monster recomputes a path to player using selected mode (BFS or DFS)
  - monster moves one step along that path
- Outcomes:
  - monster reaches player -> lose
  - player reaches `G` -> win

Try from a Python REPL:
```python
import pathfinding
pathfinding.game_loop("BFS")
# or
pathfinding.game_loop("DFS")
```

BFS monster is usually more efficient/challenging; DFS monster can feel goofy due to detours.
