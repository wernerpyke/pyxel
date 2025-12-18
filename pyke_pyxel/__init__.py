# pyke_pyxel/__init__.py

__version__ = "0.0.1"

# Re-exports (Flattening the Namespace)
# Import key classes and functions from submodules

from ._types import GameSettings, coord, area, COLOURS, DIRECTION
from ._log import log_debug, log_info, log_error

# 3. Public API Definition (Optional but Recommended)
# Controls what is imported with 'from my_package import *'
__all__ = [
    "GameSettings", "coord", "area", "COLOURS", "DIRECTION",
    "log_debug", "log_info", "log_error"
]

# Optional: Lazy Initialization (If absolutely necessary)
# If your package requires global setup (like logging configuration) that 
# must run only once, place it here, but keep it minimal.
