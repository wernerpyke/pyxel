from dataclasses import dataclass

DEBUG = False

@dataclass
class FPS:
    GAME = 30
    ANIMATION = 8

@dataclass
class SIZE:
    WINDOW = 160
    TILE = 8

@dataclass
class COLOURS:
    SPRITE_TRANSPARENCY = 0
    BLACK = 0
