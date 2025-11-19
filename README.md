# 🕹️ Pixel-art Games with Pyxel (and pixel art)

A simple Sprite- and Map-based Python game engine on top of [Pyxel](https://github.com/kitao/pyxel) with two example games.

---

## 🎯 Project Structure
- [pyke_pyxel](pyke_pyxel/): a semi-reusable, Sprite- and Map-based game engine on top of Pyxel
    - with an [overview](../docs/README.md) and basic [API Documentation](../docs/pyke_pyxel_API.md)
- [td](td/): the beginnings of a type of tower defence game
- [rpg](rpg/): prototype for a room-based RPG

---

## 🧩 TODO

- In `Game.remove_sprite`:
    - Consider moving to an approach in which a Sprite is flagged for deletion and then deleted in `update()` rather than removed from the array immediately. The current approach might be a cause for weird callback-type bugs.
- In `pyke_pyxel.sprite.CompoundSprite`:
    - Support animations, would mean caching multiple images (one per frame)
- In `pyke_pyxel.draw.compound_sprite`:
    - Support horizontal flipping


---

## 🔧 Tools

- **Python 3.x** - not bad once you get used to it but singletons are messy
- **[Pyxel](https://github.com/kitao/pyxel)** — a retro game engine for Python
- **[Aseprite](https://www.aseprite.org/)** — a wonderful pixel art sprite editor
- **[Blinker](https://github.com/pallets-eco/blinker)** - a fast Python in-process signal/event dispatching system
- **[pydocs-markdown](https://niklasrosenstein.github.io/pydoc-markdown/)** - for docstrings documentation
- **ChatGPT Python by Nicholas Barker** - to teach me Python and it's tooling in VSCode
- VSCode for development
