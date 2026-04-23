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

---

# Python Assignment: Flocking Simulation with Boids

Below is a complete reference implementation you can copy into `boids_simulation.py` and run with `pygame`.

```python
import math
import random
import pygame

WIDTH, HEIGHT = 1000, 700
BACKGROUND = (18, 20, 28)
BOID_COLOR = (230, 235, 255)

NUM_BOIDS = 60
NEIGHBOR_RADIUS = 55
SEPARATION_RADIUS = 20

SEPARATION_WEIGHT = 1.7
ALIGNMENT_WEIGHT = 1.0
COHESION_WEIGHT = 0.95

MAX_SPEED = 4.0
MAX_FORCE = 0.11


def limit(vec: pygame.Vector2, max_mag: float) -> pygame.Vector2:
    if vec.length_squared() == 0:
        return vec
    if vec.length() > max_mag:
        vec.scale_to_length(max_mag)
    return vec


class Boid:
    def __init__(self) -> None:
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        if self.velocity.length_squared() == 0:
            self.velocity = pygame.Vector2(1, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = MAX_SPEED
        self.max_force = MAX_FORCE

    def apply_force(self, force: pygame.Vector2) -> None:
        self.acceleration += force

    def neighbors(self, boids: list["Boid"]) -> list["Boid"]:
        near: list[Boid] = []
        for other in boids:
            if other is self:
                continue
            if self.position.distance_to(other.position) < NEIGHBOR_RADIUS:
                near.append(other)
        return near

    def separation(self, near: list["Boid"]) -> pygame.Vector2:
        steer = pygame.Vector2(0, 0)
        count = 0
        for other in near:
            d = self.position.distance_to(other.position)
            if 0 < d < SEPARATION_RADIUS:
                diff = self.position - other.position
                diff /= d
                steer += diff
                count += 1
        if count:
            steer /= count
        if steer.length_squared() > 0:
            steer.scale_to_length(self.max_speed)
            steer -= self.velocity
            limit(steer, self.max_force)
        return steer

    def alignment(self, near: list["Boid"]) -> pygame.Vector2:
        if not near:
            return pygame.Vector2(0, 0)
        avg = pygame.Vector2(0, 0)
        for other in near:
            avg += other.velocity
        avg /= len(near)
        if avg.length_squared() > 0:
            avg.scale_to_length(self.max_speed)
        steer = avg - self.velocity
        return limit(steer, self.max_force)

    def cohesion(self, near: list["Boid"]) -> pygame.Vector2:
        if not near:
            return pygame.Vector2(0, 0)
        center = pygame.Vector2(0, 0)
        for other in near:
            center += other.position
        center /= len(near)
        return self.seek(center)

    def seek(self, target: pygame.Vector2) -> pygame.Vector2:
        desired = target - self.position
        if desired.length_squared() == 0:
            return pygame.Vector2(0, 0)
        desired.scale_to_length(self.max_speed)
        steer = desired - self.velocity
        return limit(steer, self.max_force)

    def flock(self, boids: list["Boid"]) -> None:
        near = self.neighbors(boids)
        sep = self.separation(near) * SEPARATION_WEIGHT
        ali = self.alignment(near) * ALIGNMENT_WEIGHT
        coh = self.cohesion(near) * COHESION_WEIGHT
        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def update(self) -> None:
        self.velocity += self.acceleration
        limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.acceleration.update(0, 0)

        # screen wrapping
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def draw(self, surface: pygame.Surface) -> None:
        heading = self.velocity.angle_to(pygame.Vector2(1, 0))
        size = 9
        points = [
            pygame.Vector2(size, 0),
            pygame.Vector2(-size * 0.8, size * 0.5),
            pygame.Vector2(-size * 0.8, -size * 0.5),
        ]
        rotated = [p.rotate(-heading) + self.position for p in points]
        pygame.draw.polygon(surface, BOID_COLOR, rotated)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Flocking Simulation")
    clock = pygame.time.Clock()

    boids = [Boid() for _ in range(NUM_BOIDS)]
    running = True
    while running:
        dt = clock.tick(60)
        _ = dt  # intentionally kept for students who want dt-based motion later

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)
        for boid in boids:
            boid.flock(boids)
        for boid in boids:
            boid.update()
            boid.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
```

## Reflection Answers (Short)

1. **Biggest effect**: separation usually has the strongest immediate visible effect, because it prevents overlap and creates the characteristic spacing.
2. **If separation is too strong**: the flock explodes into jittery motion and never forms cohesive groups.
3. **If cohesion is too strong**: boids clump too tightly and can collapse into unrealistic blobs.
4. **Why emergent**: no boid plans global flock shape; group behavior appears from local interactions only.
5. **Complexity**: naive neighbor checking is **O(n²)** per frame.
6. **Optimization**: spatial hashing / uniform grids / quadtrees reduce neighbor checks to near-local buckets.

## Bonus: Simple Street Fighter HTML Page

If you want a quick single-file website about **Street Fighter**, save this as `streetfighter.html` and open it in your browser:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Street Fighter Fan Page</title>
    <style>
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        background: linear-gradient(135deg, #111, #2b0f0f);
        color: #fff;
      }
      header {
        text-align: center;
        padding: 3rem 1rem;
        background: #c1121f;
      }
      h1 {
        margin: 0;
        font-size: 2.5rem;
      }
      main {
        max-width: 900px;
        margin: 2rem auto;
        padding: 0 1rem 2rem;
      }
      .card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
      }
      .fighters {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.75rem;
      }
      .fighter {
        background: #1f1f1f;
        border-radius: 8px;
        padding: 0.75rem;
      }
      footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.9rem;
        opacity: 0.9;
      }
      .btn {
        display: inline-block;
        background: #fca311;
        color: #000;
        text-decoration: none;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        font-weight: bold;
      }
    </style>
  </head>
  <body>
    <header>
      <h1>Street Fighter</h1>
      <p>Iconic 1v1 battles, legendary fighters, and classic special moves.</p>
    </header>

    <main>
      <section class="card">
        <h2>About the Series</h2>
        <p>
          Street Fighter is one of the most influential fighting game franchises,
          known for tight gameplay, unique character styles, and high-level competitive play.
        </p>
      </section>

      <section class="card">
        <h2>Popular Fighters</h2>
        <div class="fighters">
          <div class="fighter"><strong>Ryu</strong><br />Balanced shotokan master.</div>
          <div class="fighter"><strong>Chun-Li</strong><br />Fast kicks and pressure.</div>
          <div class="fighter"><strong>Ken</strong><br />Aggressive rushdown style.</div>
          <div class="fighter"><strong>Guile</strong><br />Zoning with Sonic Boom.</div>
        </div>
      </section>

      <section class="card">
        <h2>Famous Moves</h2>
        <ul>
          <li>Hadoken</li>
          <li>Shoryuken</li>
          <li>Spinning Bird Kick</li>
          <li>Sonic Boom</li>
        </ul>
        <a class="btn" href="#">Start Training</a>
      </section>
    </main>

    <footer>
      Fan-made practice page · Fight on!
    </footer>
  </body>
</html>
```
