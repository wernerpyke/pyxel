# 🕹️ A Simple Sprite & Map-based game engine on top of Pyxel

## 🎯 Documentation

- [API Documentation](../docs/pyke_pyxel_API.md)

## Overview — building a game with `pyke_pyxel`

`pyke_pyxel` provides a small, practical toolkit for building tile-and-sprite games
on top of the Pyxel runtime. The package is intentionally lightweight but focuses on
the pieces you need day-to-day: a `Game` runner that manages the loop and screens,
a simple column/row coordinate (`Coord`) and `Map` model,
`Sprite` classes and utilities for animated characters, `HUD` helpers for on-screen status, 
`FX` utilities for transient visual effects,
and a `Signals` mechanism for decoupled event handling.

1) ***Game: the application shell***
--------------------------------
Start with `Game` — it provides the application lifecycle (initialization,
update, draw) and a place to register screens or states. A typical pattern is to
create a subclass or instantiate `Game` and register a title screen, gameplay
screen and a pause/menu screen. The `Game` object owns the Pyxel window and
drives the tick/update loop; it will call your current screen's update and draw
methods each frame. Treat `Game` as the single source of truth for game-wide
resources (loaded assets, global settings and top-level managers such as the
`Signals` broker).

2) ***Coord and Map: grid math and spatial queries**
-----------------------------------------------
Each game represents its world using a square grid of columns and rows.
Each column/row is represented by a `Coord` which makes positioning and moving sprites simple. 
`Coord` also stores an internal `x`/`y` representation including useful properties `x`, `y`, `mid_x`, `mid_y`, `min_x`, `max_x`, 
and convenience methods like `contains`, `collides_with`, `clone`, and `move_by` for simple positional math.
Use factory helpers `Coord.with_center` or `Coord.with_xy` when you need to translate between 
pixel coordinates and the tile grid.
The `Map` class stores the status and sprite of each `Coord` in the form of a `MapLocation` with statuses such as `FREE`, `BLOCKED`, `OPEN` and `CLOSED`.
Convenience methods on `Map` make common spatial tasks easy and readable. These include `is_blocked`, `is_openable`, `location_at`, `location_left_of`, `location_right_of`, `location_above`, `location_below` and others.

3) ***Sprite: characters, objects and animations***
---------------------------------------------
`Sprite` is the primary building block for visible entities. Sprites hold a
current frame and a dictionary of named `Animation` objects. Use `add_animation`
to register walk, attack, or idle animations, and `activate_animation` to start
them (optionally looping or invoking a callback when complete). `MovableSprite`
provides helpers for directional animations and a movement speed; `OpenableSprite`
models objects with open/closed states (doors, chests).

Typical usage:
- create a `Sprite` with an idle frame (a `Coord` into a tilesheet),
- add animations (start frame and frame count),
- set the sprite's `position` to a `Coord` (grid-aware)

4) ***Signals: decoupled messaging***
--------------------------------
`Signals` implements a simple pub/sub mechanism so parts of your game can
communicate without direct references. For example, the player sprite can emit
an "item_collected" signal with a payload, any interested HUD or inventory
manager can subscribe and update state. Signals are great for wiring UI, audio
triggers and cross-cutting behaviours without coupling modules together.

5) ***HUD: present game state to the player***
----------------------------------------
The `HUD` utilities make it easy to display player health, inventory, scores and
other overlays. A HUD is typically updated from the same game state that drives
your logic and drawn last so it appears above world sprites. Keep HUD code
separate from game logic: write small presenter functions that turn internal
state into text/tiles and hand them to the HUD renderer each frame.

7) ***FX: short-lived visual effects***
---------------------------------
Use `FX` helpers for transient effects — flashes, particles, screen shakes,
and animated overlays. FX objects are lightweight and intended to be created
on-the-fly by gameplay events (an explosion spawns an FX instance which lives
for its duration and then self-destructs). Because FX are short-lived, keep
their update/draw code efficient and stateless where possible (the engine
already provides small helpers to simplify common tasks).