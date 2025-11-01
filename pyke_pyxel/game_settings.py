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
    sprite_transparency: int = 0 # COLOURS.BLACK
    background:int = 0 # COLOURS.BLACK
    hud_text: int = 7 # COLOURS.WHITE

@dataclass
class GameSettings:
    debug: bool = False

    fps: FpsSettings = field(default_factory=FpsSettings)

    size: SizeSettings = field(default_factory=SizeSettings)

    colours: ColourSettings = field(default_factory=ColourSettings)


