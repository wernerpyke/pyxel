import random
from pyke_pyxel import DIRECTION, log_debug

from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

from td.fungus import Fungus
from td.wave import Wave
from td.weapon import Weapon
from td.bolt import Bolt


position_left = Coord(16, 35)
position_center = Coord(19, 34)
position_right = Coord(23, 35)

weapons: list[Weapon] = []

def game_started(game: FieldGame):
    print("Game Started")

    field = game.field

    fungus = Fungus(position_center)
    fungus.launch(field)
    weapons.append(fungus)

    # wave = Wave(Coord(20, 20))
    # wave.launch(field)
    # weapons.append(wave)

def game_state_update(field: CellField):
    to_remove: list[Weapon] = []
    for w in weapons:
        if w.update(field) == False:
            to_remove.append(w)
    
    for w in to_remove:
        log_debug(f"GameLoop remove {w.type}")
        weapons.remove(w)

    if len(weapons) == 1:
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


        # print("NO MORE WEAPONS")
        # pyxel.quit()