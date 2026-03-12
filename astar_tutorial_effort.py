"""A* tutorial effort: grid pathfinding with a creative ASCII visualization.

This is a Codex-based implementation inspired by the Unity A* project.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import heapq
from typing import Iterable


GridPos = tuple[int, int]


@dataclass(order=True)
class PriorityNode:
    """Item stored in the priority queue for A*."""

    f_score: int
    h_score: int
    pos: GridPos = field(compare=False)


class GridAStar:
    """Simple 2D grid A* pathfinder with 4-directional movement."""

    def __init__(self, width: int, height: int, walls: set[GridPos]) -> None:
        self.width = width
        self.height = height
        self.walls = walls

    def in_bounds(self, pos: GridPos) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos: GridPos) -> bool:
        return pos not in self.walls

    def neighbors(self, pos: GridPos) -> Iterable[GridPos]:
        x, y = pos
        for nxt in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if self.in_bounds(nxt) and self.passable(nxt):
                yield nxt

    @staticmethod
    def heuristic(a: GridPos, b: GridPos) -> int:
        # Manhattan distance works for a 4-direction grid.
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start: GridPos, goal: GridPos) -> list[GridPos]:
        """Return shortest path from start to goal using A* (or empty list if none)."""

        open_heap: list[PriorityNode] = []
        heapq.heappush(open_heap, PriorityNode(self.heuristic(start, goal), 0, start))

        came_from: dict[GridPos, GridPos | None] = {start: None}
        g_score: dict[GridPos, int] = {start: 0}

        while open_heap:
            current = heapq.heappop(open_heap).pos
            if current == goal:
                return self._reconstruct_path(came_from, goal)

            for nxt in self.neighbors(current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(nxt, 10**9):
                    came_from[nxt] = current
                    g_score[nxt] = tentative_g
                    h = self.heuristic(nxt, goal)
                    heapq.heappush(open_heap, PriorityNode(tentative_g + h, h, nxt))

        return []

    @staticmethod
    def _reconstruct_path(came_from: dict[GridPos, GridPos | None], goal: GridPos) -> list[GridPos]:
        path: list[GridPos] = []
        cur: GridPos | None = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path


def render_grid(
    width: int,
    height: int,
    walls: set[GridPos],
    path: list[GridPos],
    start: GridPos,
    goal: GridPos,
) -> str:
    """Render an ASCII map for easy submission/upload."""

    path_set = set(path)
    rows: list[str] = []
    for y in range(height):
        row: list[str] = []
        for x in range(width):
            p = (x, y)
            if p == start:
                row.append("S")
            elif p == goal:
                row.append("G")
            elif p in walls:
                row.append("#")
            elif p in path_set:
                row.append("*")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)


def build_creative_level() -> tuple[int, int, set[GridPos], GridPos, GridPos]:
    """Create a small 'spiral gate' style map as a creative variation."""

    width, height = 14, 10
    walls: set[GridPos] = set()

    # Border walls with two gates.
    for x in range(width):
        walls.add((x, 0))
        walls.add((x, height - 1))
    for y in range(height):
        walls.add((0, y))
        walls.add((width - 1, y))

    gates = {(1, 0), (width - 2, height - 1)}
    walls -= gates

    # Interior maze-like stripes.
    for x in range(2, width - 2):
        if x % 2 == 0:
            for y in range(2, height - 2):
                walls.add((x, y))
            # Add alternating openings.
            opening = 2 if (x // 2) % 2 == 0 else height - 3
            walls.discard((x, opening))

    start = (1, 0)
    goal = (width - 2, height - 1)
    return width, height, walls, start, goal


def main() -> None:
    width, height, walls, start, goal = build_creative_level()
    astar = GridAStar(width, height, walls)
    path = astar.find_path(start, goal)

    print("=== A* Pathfinding Demo (Tutorial Effort) ===")
    if path:
        print(f"Path length: {len(path) - 1} steps")
    else:
        print("No path found.")
    print(render_grid(width, height, walls, path, start, goal))


if __name__ == "__main__":
    main()
