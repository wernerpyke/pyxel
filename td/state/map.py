from dataclasses import dataclass
from typing import Optional
from pyke_pyxel import DIRECTION, GLOBAL_SETTINGS
from pyke_pyxel.base_types import Coord

@dataclass
class WeaponLocation:
    name: str
    position: Coord
    orientation: str

class GameMap:

    def __init__(self) -> None:
        self.width = GLOBAL_SETTINGS.size.window
        self.height = GLOBAL_SETTINGS.size.window

        self.selected_location: Optional[WeaponLocation] = None

        self._weapon_locations: list[WeaponLocation] = [
            WeaponLocation("1", Coord.with_center(124, 268), "vertical"),
            WeaponLocation("2", Coord.with_center(130, 244), "horizontal"),
            WeaponLocation("3", Coord.with_center(140, 234), "horizontal"),
            WeaponLocation("4", Coord.with_center(164, 234), "horizontal"),
            WeaponLocation("5", Coord.with_center(174, 244), "horizontal"),
            WeaponLocation("6", Coord.with_center(180, 268), "vertical")
        ]
    
    def weapon_location_at(self, x: int, y: int) -> Optional[WeaponLocation]:
        for l in self._weapon_locations:
            p = l.position
            if x >= p.min_x and x < p.max_x and y >= p.min_y and y < p.max_y:
                return l
        return None