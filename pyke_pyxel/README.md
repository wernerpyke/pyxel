# 🕹️ A Simple Sprite- & Map-based game engine on top of Pyxel

## 🎯 Documentation

- [Introduction](../docs/README.md) - an introduction to `pyke_pyxel`
- [API Documentation](../docs/pyke_pyxel_API.md)

## 🧩 TODO

- In `pyke_pyxel.fx`:
    - Move the circular wipe code out to either a class or functions
- In `pyke_pyxel.button`:
    - Fix `coord.contains()` dependency on tile width (currently calculated in Button). Consider allowing `coord()` to be created with col/row tile count.