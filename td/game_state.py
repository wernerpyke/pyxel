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
    orientation: str
    propagate: list[str]

class GameMap:

    def __init__(self) -> None:
        self.launch_locations: list[LaunchLocation] = [
            # The order of propagate= is important
            # see Bolt.launch() - the first item in the list is used to tag the first set of cells
            LaunchLocation("1", 
                            position=Coord.with_center(124, 268),
                            orientation="vertical",
                            propagate=[ DIRECTION.LEFT, 
                                        DIRECTION.LEFT, 
                                        DIRECTION.LEFT,
                                        DIRECTION.UP,
                                        DIRECTION.DOWN]),
            
            LaunchLocation("2", 
                            position=Coord.with_center(130, 244),
                            orientation="horizontal",
                            propagate=[ DIRECTION.LEFT,
                                        DIRECTION.LEFT, 
                                        DIRECTION.LEFT,
                                        DIRECTION.UP,
                                        DIRECTION.RIGHT]),
            
            LaunchLocation("3", 
                            position=Coord.with_center(140, 234),
                            orientation="horizontal",
                            propagate=[ DIRECTION.UP,
                                        DIRECTION.UP, 
                                        DIRECTION.LEFT,
                                        DIRECTION.LEFT, 
                                        DIRECTION.RIGHT]),
            
            LaunchLocation("4", 
                            position=Coord.with_center(164, 234),
                            orientation="horizontal",
                            propagate=[ DIRECTION.UP,
                                        DIRECTION.UP,
                                        DIRECTION.LEFT, 
                                        DIRECTION.RIGHT, 
                                        DIRECTION.RIGHT]),
            
            LaunchLocation("5", 
                            position=Coord.with_center(174, 244),
                            orientation="horizontal",
                            propagate=[ DIRECTION.RIGHT, 
                                        DIRECTION.RIGHT, 
                                        DIRECTION.RIGHT,
                                        DIRECTION.UP, 
                                        DIRECTION.LEFT
                                        ]),
            
            LaunchLocation("6", 
                            position=Coord.with_center(180, 268),
                            orientation="vertical",
                            propagate=[ DIRECTION.RIGHT, 
                                        DIRECTION.RIGHT, 
                                        DIRECTION.RIGHT,
                                        DIRECTION.UP, 
                                        DIRECTION.DOWN
                                        ])
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
    
    launch_location: Optional[LaunchLocation] = None
    
    # UI
    ui_state: str = ""
    ui_marker_sprite = Sprite("location_marker", Coord(5, 10), col_tile_count=2, row_tile_count=2)

    # Sound
    music_enabled = False

STATE = game_state()