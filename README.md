# 🕹️ Top-Down Pixel Art Game

A very basic Python game engine on top of [Pyxel](https://github.com/kitao/pyxel) with two example games.

---

## 🎯 Project Structure
- `pyke_pyxel`: a semi-reusable, highly primitive game engine on top of Pyxel
- `td`: the beginnings of a type of tower defence game
- `rpg`: prototype for a room-based RPG

---

## 🧩 TODO

- In Game.remove_sprite:
 - Consider moving to an approach in which a Sprite is flagged for deletion and then deleted in update()
- In pyke_pyxel.draw.tile_map:
 - cache image to avoid nested looping
- In pyke_pyxel.draw.compound_sprite:
 - Support horizontal flipping
- In pyke_pyxel.sprite.CompoundSprite:
 - cache image to avoid nested looping
 - support animations

---

## 🔧 Technologies Used

- **ChatGPT Python by Nicholas Barker** - to teach me Python and it's tooling in VSCode
- **Python 3.x**
- **[Pyxel](https://github.com/kitao/pyxel)** — a retro game engine for Python
- **[Aseprite](https://www.aseprite.org/)** — a wonderful pixel art sprite editor
- **[Blinker](https://github.com/pallets-eco/blinker)** - a fast Python in-process signal/event dispatching system
- VSCode for development
