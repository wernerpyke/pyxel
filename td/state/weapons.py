import time
import random

from typing import Optional
from pyke_pyxel import Coord, log_debug, log_error
from pyke_pyxel.cell_auto.matrix import Matrix
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite
from td.weapons.bolt import Bolt
from td.weapons.fungus import Fungus
from td.weapons.meteor import Meteor
from td.weapons.weapon import Weapon

class WeaponLocation:
    def __init__(self, id: str, position: Coord, orientation: str) -> None:
        self.id = id
        self.position = position
        self.orientation = orientation    
    
        self._type: str|None = None
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

    def deactivate(self):
        if self._active:
            log_debug(f"WeaponLocation.deactivate() KILL {self._type}")
            self._active.kill()
            self._active = None
        
        self._type = None
        self._previous_launch_time = 0

    @property
    def cooldown(self) -> float:
        if self._active:
            return self._active._cooldown
        else:
            return 90

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

        self._locations: list[WeaponLocation] = [
            WeaponLocation("1", Coord.with_center(124, 268), "vertical"),
            WeaponLocation("2", Coord.with_center(130, 244), "horizontal"),
            WeaponLocation("3", Coord.with_center(140, 234), "horizontal"),
            WeaponLocation("4", Coord.with_center(164, 234), "horizontal"),
            WeaponLocation("5", Coord.with_center(174, 244), "horizontal"),
            WeaponLocation("6", Coord.with_center(180, 268), "vertical")
        ]

        self.active: list[Weapon] = []

    def cost_of(self, type: str) -> int:
        match type:
            case "bolt":
                return 1
            case "fungus":
                return 3
            case "meteor":
                return 2
            case _:
                log_error(f"weapons.cost_of() invalid type {type}")
                return 10

    def update(self, field: Matrix):
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
            if w._deactivate_upon_death:
                print(f"DEACTIVATE {w.type} from location {w._location_id}")
                Signals.send("weapon_deactivate_at_location", w._location_id)
            self.active.remove(w)

        now = time.time()
        
        for l in self._locations:
            if l._type and ((now - l._previous_launch_time) > l.cooldown):
                match l._type:
                    case "bolt":
                        self._launch_bolt(l, field)
                    case "fungus":
                        self._launch_fungus(l, field)
                    case "meteor":
                        self._launch_meteor(l, field)
    
    def clear_all(self):
        self.active.clear()
        for l in self._locations:
            l._active = None
            l._type = None

    def _launch_fungus(self, location: WeaponLocation, field: Matrix):
        active = location._active
        if active and active.type == "fungus" and active.is_alive:
            # log_debug(f"weapons.launch_fungus skipping launch - current fungus is still active")
            return active
        
        log_debug("weapons.launch_fungus")
        
        fungus = Fungus(location.id, location.position)
        fungus.launch(field)

        location._previous_launch_time = time.time()
        location._active = fungus
        self.active.append(fungus)

    def _launch_meteor(self, location: WeaponLocation, field: Matrix):
        log_debug("weapons._launch_meteor")

        meteor = Meteor(location.id, location.position)
        meteor.launch(field)
        
        location._previous_launch_time = time.time()
        location._active = meteor
        self.active.append(meteor)

    def _launch_bolt(self, location: WeaponLocation, field: Matrix):
        log_debug("weapons._launch_bolt")

        bolt = Bolt(location.id, location.position, location.orientation)
        bolt.launch(field)

        location._previous_launch_time = time.time()
        location._active = bolt
        self.active.append(bolt)

    def location_at(self, x: int, y: int) -> WeaponLocation|None:
        for l in self._locations:
            p = l.position
            if x >= p.min_x and x < p.max_x and y >= p.min_y and y < p.max_y:
                return l
        return None
    
    def location_by_id(self, id: str) -> WeaponLocation|None:
        for l in self._locations:
            if l.id == id:
                return l
        return None
