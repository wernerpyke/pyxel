from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from pyke_pyxel import DIRECTION, GLOBAL_SETTINGS
from pyke_pyxel.base_types import Coord
from pyke_pyxel.sprite import Sprite, TextSprite

@dataclass
class LaunchLocation:
    name: str
    position: Coord
    propagate_direction: str

class GameMap:

    def __init__(self) -> None:
        self.launch_locations: list[LaunchLocation] = [
            LaunchLocation("1", 
                            position=Coord.with_center(124, 268),
                            propagate_direction=DIRECTION.LEFT),
            LaunchLocation("2", 
                            position=Coord.with_center(130, 244),
                            propagate_direction=DIRECTION.LEFT),
            LaunchLocation("3", 
                            position=Coord.with_center(140, 234),
                            propagate_direction=DIRECTION.UP),
            LaunchLocation("4", 
                            position=Coord.with_center(164, 234),
                            propagate_direction=DIRECTION.RIGHT),
            LaunchLocation("5", 
                            position=Coord.with_center(174, 244),
                            propagate_direction=DIRECTION.RIGHT),
            LaunchLocation("6", 
                            position=Coord.with_center(180, 268),
                            propagate_direction=DIRECTION.RIGHT),
        ]
    
    def launch_location_at(self, x: int, y: int) -> Optional[LaunchLocation]:
        for l in self.launch_locations:
            p = l.position
            if x >= p.min_x and x < p.max_x and y >= p.min_y and y < p.max_y:
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

    # Sound
    music_enabled = False

STATE = game_state()