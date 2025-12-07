from ._state import GameState

# from .stats import STATS 
# Cannot import stats here as it causes a circular import in Weapon() and Enemy()

STATE = GameState()

__all__ = [
    "STATE"
]