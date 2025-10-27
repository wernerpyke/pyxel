from dataclasses import dataclass, field

@dataclass
class FpsSettings:
    game: int = 30
    animation: int = 8

@dataclass
class SizeSettings:
    window:int  = 160
    tile: int = 8

@dataclass
class ColourSettings:
    sprite_transparency: int = 0
    black:int = 0

@dataclass
class GameSettings:
    debug: bool = False

    fps: FpsSettings = field(default_factory=FpsSettings)

    size: SizeSettings = field(default_factory=SizeSettings)

    colours: ColourSettings = field(default_factory=ColourSettings)


