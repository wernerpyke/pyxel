import random

from pyke_pyxel import DIRECTION, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import CellField
from .fungus import Fungus
from .wave import Wave
from .weapon import Weapon
from .bolt import Bolt

position_left = Coord(16, 31)
position_center = Coord(19, 30)
position_right = Coord(23, 31)

weapons: list[Weapon] = []

def launch_fungus(field: CellField):
    # log_debug("GameLoop launch fungus")

    for c in field.cells_at(position_center): # Give fungus room to grow
        c.reset()

    fungus = Fungus(position_center)
    fungus.launch(field)
    weapons.append(fungus)

def launch_wave(field: CellField):
    wave = Wave(Coord(20, 20))
    wave.launch(field)
    weapons.append(wave)

def launch_bolt(field: CellField):
    # log_debug("GameLoop launch bolt")
    bolt: Bolt
    i = random.randint(0,2)
    match i:
        case 0:
            bolt = Bolt(position_left, DIRECTION.LEFT)
        case 1:
            bolt = Bolt(position_center, DIRECTION.UP)
        case 2:
            bolt = Bolt(position_right, DIRECTION.RIGHT)
    bolt.launch(field)
    weapons.append(bolt)

def has_active_weapon(type: str) -> bool:
    for w in weapons:
        if w.type == type:
            return True
    
    return False

def update(field: CellField):
    to_remove: list[Weapon] = []
    for w in weapons:
        if w.update(field) == False:
            to_remove.append(w)
    
    for w in to_remove:
        # log_debug(f"GameLoop remove {w.type}")
        weapons.remove(w)