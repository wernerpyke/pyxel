# Gemini Code Assist Guide for the `pyxel` Project

This document provides guidelines for using Gemini Code Assist with the `pyxel` repository. Adhering to these conventions will help ensure that AI-generated code is consistent, correct, and follows the project's established patterns.

## About This Project

This project, `pyxel`, is a Python-based game development library and a collection of example games. It is a set of utilities, abstractions, and game examples built upon the Pyxel retro game engine. The primary language is Python 3, and it uses type hints for clarity and robustness.

## Domain Model Context

**CRITICAL INSTRUCTION:** For any requests related to `pyke-pyxel` feature implementation, you MUST first read the overview of how the game engine is structured. The overview is located at **`@docs/README.md`**.

## Codebase Structure

The repository is organized into a core library and several example applications.

-   `pyke_pyxel/`: The core library source code. This contains reusable components for game development like drawing primitives, game state management, sprites, and more.
-   `td/`: A "Tower Defense" game example that uses the `pyke-pyxel` library.
-   `rpg/`: An RPG game example.
-   `docs/`: Contains generated API documentation.
-   `scripts/`: Holds shell scripts for performing common development tasks like running games and updating documentation.
-   `assets/`: Contains game assets used by the examples, such as images (`.aseprite`, `.png`) and Pyxel resource files (`.pyxres`).

## Development Conventions

Maintaining a consistent style is crucial. Please follow these conventions strictly.

### 1. Code Style and Formatting

-   **PEP 8**: Follow the PEP 8 style guide for all Python code.
-   **Naming Conventions**:
    -   `PascalCase` for class names (e.g., `Player`, `SpriteManager`).
    -   `snake_case` for functions, methods, variables, and file names (e.g., `update_player`, `game_loop.py`).
-   **Typing**: Use Python type hints for all new function and method signatures. Analyze existing code for the proper types to use.
-   **Docstrings**: Add Google-style docstrings to all new public modules, classes, and functions to explain their purpose, arguments, and return values. This is critical as documentation is generated from them.

### 2. Imports

-   Organize imports in the standard order:
    1.  Standard library imports (e.g., `os`, `sys`).
    2.  Third-party library imports (e.g., `pyxel`).
    3.  Local application/library imports (e.g., `from pyke_pyxel import draw`).

## 3. Specific Instructions for AI

-   **Refactoring:** When asked to refactor code, prioritize **readability** over extreme micro-optimizations.

## Common Tasks

When asked to perform a task, use the following commands and workflows.

### Updating Documentation

The documentation in `docs/` is generated from source code docstrings using `pydoc-markdown`.

-   **To update the API documentation:**
    ```bash
    ./scripts/update-docs.sh
    ```
