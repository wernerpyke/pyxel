from dataclasses import dataclass, field

@dataclass
class FPS:
    game: int = 30
    animation: int = 8

@dataclass
class SIZE:
    window:int  = 160
    tile: int = 8

@dataclass
class COLOURS:
    sprite_transparency: int = 0
    black:int = 0

@dataclass
class GAME_SETTINGS:
    debug: bool = False

    fps: FPS = field(default_factory=FPS)

    size: SIZE = field(default_factory=SIZE)

    colours: COLOURS = field(default_factory=COLOURS)


