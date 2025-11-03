from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from pyke_pyxel import DIRECTION, GLOBAL_SETTINGS
from pyke_pyxel.base_types import Coord
from pyke_pyxel.sprite import Sprite, TextSprite

@dataclass
class LaunchLocation:
    name: str
    from_x: int
    to_x: int
    from_y: int
    to_y: int
    marker_at: Coord
    launch_from: Coord
    propagate_direction: str

class GameMap:

    def __init__(self) -> None:
        self.launch_locations: list[LaunchLocation] = [
            LaunchLocation("left_top", 
                           120, 140, 
                           230, 250, 
                           marker_at=Coord(16, 30),
                           launch_from=Coord(16, 30),
                           propagate_direction=DIRECTION.LEFT),
            LaunchLocation("center", 
                           140, 160, 
                           220, 240, 
                           marker_at=Coord(19, 29),
                           launch_from=Coord(19, 30),
                           propagate_direction=DIRECTION.UP),
            LaunchLocation("right_top", 
                           170, 190, 
                           230, 250, 
                           marker_at=Coord(22, 30),
                           launch_from=Coord(23, 30),
                           propagate_direction=DIRECTION.RIGHT),
        ]
    
    def launch_location_at(self, x: int, y: int) -> Optional[LaunchLocation]:
        for l in self.launch_locations:
            if x >= l.from_x and x <= l.to_x and y >= l.from_y and y <= l.to_y:
                return l
        return None


@dataclass
class game_state:
    map = GameMap()
    score: int = 0
    score_text = TextSprite("*", 
                            GLOBAL_SETTINGS.colours.hud_text,
                            f"{Path(__file__).parent.resolve()}/assets/t0-14b-uni.bdf")
    
    # UI
    ui_state: str = "select_location"
    launch_location: Optional[LaunchLocation] = None
    ui_marker_sprite = Sprite("location_marker", Coord(5, 11), col_tile_count=2, row_tile_count=2)

STATE = game_state()