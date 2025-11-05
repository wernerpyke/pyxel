import random

from pyke_pyxel import DIRECTION, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import CellField
from td.game_state import STATE, LaunchLocation
from .fungus import Fungus
from .wave import Wave
from .weapon import Weapon
from .bolt import Bolt

weapons: list[Weapon] = []

def launch_fungus(location: Coord, field: CellField):
    # log_debug("GameLoop launch fungus")

    for c in field.cells_at(location): # Give fungus room to grow
        c.reset()

    fungus = Fungus(location)
    fungus.launch(field)
    weapons.append(fungus)

def launch_wave(field: CellField):
    wave = Wave(Coord(20, 20))
    wave.launch(field)
    weapons.append(wave)

def launch_bolt(location: LaunchLocation,
                field: CellField):
    bolt = Bolt(location.position, location.orientation, location.propagate)
    bolt.launch(field)
    weapons.append(bolt)

def has_active_weapon(type: str) -> bool:
    for w in weapons:
        if w.type == type:
            return True
    
    return False

def _should_skip_update(weapon: Weapon) -> bool:
    speed = weapon._speed
    if speed == 10:
        return False
    
    skip_frequency = (10 - speed) / 10

    skip = random.random() < skip_frequency
    # weapon._updates_attempted_count +=1
    #if skip:
    #    weapon._updates_skipped_count += 1
    #print(f"SKIP FREQ:{skip_frequency} vs {(weapon._updates_skipped_count / weapon._updates_attempted_count)}")
    return skip

def update(field: CellField):
    to_remove: list[Weapon] = []
    for w in weapons:
        if _should_skip_update(w):
            if not w.is_alive:
                to_remove.append(w)
        elif w.update(field) == False:
            to_remove.append(w)
    
    for w in to_remove:
        weapons.remove(w)

    # if len(weapons) == 0:
    #    launch_bolt(STATE.map.launch_locations[5], field)