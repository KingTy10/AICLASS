from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]


EXAMPLE_MAP_1 = """
##########
#S..#....#
#..##.##.#
#...#...G#
##########
""".strip("\n")

EXAMPLE_MAP_2 = """
############
#S.....#...#
###.##.#.#.#
#...#..#.#G#
#.###..#...#
#......###.#
############
""".strip("\n")

EXAMPLE_MAP_3 = """
###########
#S#.....#G#
#.#.###.#.#
#.#...#.#.#
#.#.#.#.#.#
#...#.....#
###########
""".strip("\n")

GAME_MAP = """
############
#P....#....#
#.##..#.#..#
#....##.#..#
#.##....#G.#
#..#..#....#
#....#...M.#
############
""".strip("\n")

MODE = "BFS"  # or "DFS"


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    rows = [list(line) for line in text.splitlines() if line.strip()]
    if not rows:
        raise ValueError("Grid text is empty")

    width = len(rows[0])
    if any(len(r) != width for r in rows):
        raise ValueError("All rows in the grid must have equal width")

    start: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            if cell == "S":
                if start is not None:
                    raise ValueError("Map must contain exactly one S")
                start = (r, c)
            elif cell == "G":
                if goal is not None:
                    raise ValueError("Map must contain exactly one G")
                goal = (r, c)
            elif cell not in {"#", "."}:
                raise ValueError(f"Invalid cell '{cell}' at {(r, c)}")

    if start is None or goal is None:
        raise ValueError("Map must contain exactly one S and one G")

    return rows, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    r, c = node
    out: List[Pos] = []
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
            out.append((nr, nc))
    return out


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if start == goal:
        return [start]
    if goal not in parent:
        return None

    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    q: deque[Pos] = deque([start])
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while q:
        node = q.popleft()
        if node == goal:
            return reconstruct_path(parent, start, goal), visited

        for nb in neighbors(grid, node):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                q.append(nb)

    return None, visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    stack: List[Pos] = [start]
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while stack:
        node = stack.pop()
        if node == goal:
            return reconstruct_path(parent, start, goal), visited

        # reversed order keeps traversal deterministic relative to neighbors()
        for nb in reversed(neighbors(grid, node)):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                stack.append(nb)

    return None, visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules (recommended):
    - path tiles shown as '*'
    - visited tiles shown as '·' (middle dot) or '+'
    - preserve 'S' and 'G'
    """
    canvas = [row[:] for row in grid]

    if visited:
        for r, c in visited:
            if canvas[r][c] == ".":
                canvas[r][c] = "·"

    if path:
        for r, c in path:
            if canvas[r][c] == "·" or canvas[r][c] == ".":
                canvas[r][c] = "*"

    return "\n".join("".join(row) for row in canvas)


def run_one(label: str, grid_text: str) -> None:
    grid, start, goal = parse_grid(grid_text)

    print("=" * 60)
    print(label)
    print("- Raw map")
    print(render(grid))

    path_bfs, visited_bfs = bfs_path(grid, start, goal)
    print("\n- BFS")
    print(
        f"found={path_bfs is not None} path_len={(len(path_bfs) if path_bfs else None)} visited={len(visited_bfs)}"
    )
    print(render(grid, path=path_bfs, visited=visited_bfs))

    path_dfs, visited_dfs = dfs_path(grid, start, goal)
    print("\n- DFS")
    print(
        f"found={path_dfs is not None} path_len={(len(path_dfs) if path_dfs else None)} visited={len(visited_dfs)}"
    )
    print(render(grid, path=path_dfs, visited=visited_dfs))


def parse_game_grid(text: str) -> Tuple[Grid, Pos, Pos, Pos]:
    rows = [list(line) for line in text.splitlines() if line.strip()]
    player: Optional[Pos] = None
    monster: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            if cell == "P":
                player = (r, c)
                rows[r][c] = "."
            elif cell == "M":
                monster = (r, c)
                rows[r][c] = "."
            elif cell == "G":
                goal = (r, c)

    if player is None or monster is None or goal is None:
        raise ValueError("Game map must contain P, M, and G")

    return rows, player, monster, goal


def game_loop(mode: str = MODE) -> None:
    grid, player, monster, goal = parse_game_grid(GAME_MAP)
    mode = mode.upper()
    if mode not in {"BFS", "DFS"}:
        raise ValueError("mode must be BFS or DFS")

    def with_entities() -> Grid:
        g = [row[:] for row in grid]
        pr, pc = player
        mr, mc = monster
        gr, gc = goal
        g[gr][gc] = "G"
        g[pr][pc] = "P"
        g[mr][mc] = "M"
        return g

    print("\n" + "=" * 60)
    print(f"Monster Chase (Turn-Based) mode={mode}")
    print("Use WASD to move, q to quit.")

    while True:
        print(render(with_entities()))
        if monster == player:
            print("Monster reached you. You lose!")
            return
        if player == goal:
            print("You reached the exit. You win!")
            return

        move = input("Move (w/a/s/d, q to quit): ").strip().lower()
        if move == "q":
            print("Game quit.")
            return

        deltas = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}
        if move in deltas:
            dr, dc = deltas[move]
            nr, nc = player[0] + dr, player[1] + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
                player = (nr, nc)

        if mode == "BFS":
            path, _ = bfs_path(grid, monster, player)
        else:
            path, _ = dfs_path(grid, monster, player)

        if path and len(path) >= 2:
            monster = path[1]


def main() -> None:
    run_one("Example Map 1", EXAMPLE_MAP_1)
    run_one("Example Map 2", EXAMPLE_MAP_2)
    run_one("Example Map 3 (DFS typically longer)", EXAMPLE_MAP_3)


if __name__ == "__main__":
    main()
