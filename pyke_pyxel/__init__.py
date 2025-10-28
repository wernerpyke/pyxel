from dataclasses import dataclass
from .game_settings import GameSettings

GLOBAL_SETTINGS: GameSettings = GameSettings()

@dataclass
class DIRECTION:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

def log_debug(message):
    print(f"\x1b[2m{message}\x1b[0m")

def log_info(message):
    print(message)

def log_error(message):
    print(f"\x1b[31m{message}\x1b[0m")