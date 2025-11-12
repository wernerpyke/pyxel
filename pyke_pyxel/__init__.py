from dataclasses import dataclass
from .settings import GameSettings

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

@dataclass
class colours:
    BLACK = 0
    BLUE_DARK = 1
    PURPLE = 2
    GREEN = 3
    BROWN = 4
    BLUE = 5
    BLUE_SKY = 6
    WHITE = 7
    RED = 8
    ORANGE = 9
    YELLOW = 10
    GREEN_MINT = 11
    BLUE_LIGHT = 12    
    GREY = 13
    PINK = 14
    BEIGE = 15

COLOURS: colours = colours()