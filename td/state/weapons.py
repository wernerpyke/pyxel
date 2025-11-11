import time
import random

from dataclasses import dataclass
from typing import Optional
from pyke_pyxel import GLOBAL_SETTINGS, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import CellField
from pyke_pyxel.sprite import Sprite
from td.weapons.bolt import Bolt
from td.weapons.fungus import Fungus
from td.weapons.meteor import Meteor
from td.weapons.weapon import Weapon

class WeaponLocation:
    def __init__(self, name: str, position: Coord, orientation: str) -> None:
        self.name = name
        self.position = position
        self.orientation = orientation    
    

        self._type: str|None = None
        self._cooldown: float = 8 # seconds
        self._previous_launch_time: float = 0
        self._active: Weapon|None = None

        self.marker: Sprite|None = None

    def activate(self, type: str):
        if self._active:
            log_debug(f"WeaponLocation.activate() KILL {self._type}")
            self._active.kill()
            self._active = None
        
        log_debug(f"WeaponLocation.activate() {type}")
        self._type = type
        self._previous_launch_time = 0
        

def _should_skip_update(weapon: Weapon) -> bool:
    speed = weapon._speed
    if speed == 10:
        return False
    
    skip_frequency = (10 - speed) / 10

    skip = random.random() < skip_frequency
    return skip

class GameWeapons:

    def __init__(self) -> None:
        self.selected_location: Optional[WeaponLocation] = None

        self._weapon_locations: list[WeaponLocation] = [
            WeaponLocation("1", Coord.with_center(124, 268), "vertical"),
            WeaponLocation("2", Coord.with_center(130, 244), "horizontal"),
            WeaponLocation("3", Coord.with_center(140, 234), "horizontal"),
            WeaponLocation("4", Coord.with_center(164, 234), "horizontal"),
            WeaponLocation("5", Coord.with_center(174, 244), "horizontal"),
            WeaponLocation("6", Coord.with_center(180, 268), "vertical")
        ]

        self.active: list[Weapon] = []

    def update(self, field: CellField):
        to_remove: list[Weapon] = []
        for w in self.active:
            if _should_skip_update(w):
                if not w.is_alive:
                    to_remove.append(w)
            else:
                w.update(field)
                if not w.is_alive:
                    to_remove.append(w)
        
        for w in to_remove:
            self.active.remove(w)

        now = time.time()
        
        for l in self._weapon_locations:
            if l._type and ((now - l._previous_launch_time) > l._cooldown):
                match l._type:
                    case "bolt":
                        self._launch_bolt(l, field)
                    case "fungus":
                        self._launch_fungus(l, field)
                    case "meteor":
                        self._launch_meteor(l, field)
    
    def _launch_fungus(self, location: WeaponLocation, field: CellField):
        active = location._active
        if active and active.type == "fungus" and active.is_alive:
            # log_debug(f"weapons.launch_fungus skipping launch - current fungus is still active")
            return active
        
        log_debug("weapons.launch_fungus")

        fungus = Fungus(location.position)
        fungus.launch(field)

        location._previous_launch_time = time.time()
        location._active = fungus
        self.active.append(fungus)

    def _launch_meteor(self, location: WeaponLocation, field: CellField):
        log_debug("weapons._launch_meteor")

        meteor = Meteor(location.position)
        meteor.launch(field)
        
        location._previous_launch_time = time.time()
        location._active = meteor
        self.active.append(meteor)

    def _launch_bolt(self, location: WeaponLocation, field: CellField):
        log_debug("weapons._launch_bolt")

        bolt = Bolt(location.name, location.position, location.orientation)
        bolt.launch(field)

        location._previous_launch_time = time.time()
        location._active = bolt
        self.active.append(bolt)

    def location_at(self, x: int, y: int) -> Optional[WeaponLocation]:
        for l in self._weapon_locations:
            p = l.position
            if x >= p.min_x and x < p.max_x and y >= p.min_y and y < p.max_y:
                return l
        return None