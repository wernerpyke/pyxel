from dataclasses import dataclass
from pathlib import Path
from pyke_pyxel import GameSettings, Coord
from pyke_pyxel.sprite import Sprite, TextSprite

@dataclass
class GameUI:
    state: str = ""
    score_text = TextSprite("*", 
                            GameSettings.get().colours.hud_text,
                            f"{Path(__file__).parent.resolve()}/../assets/t0-14b-uni.bdf")
    marker_sprite = Sprite("location_marker", Coord(5, 10), col_tile_count=2, row_tile_count=2)