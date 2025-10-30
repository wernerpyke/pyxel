import random
import pyxel
from pyke_pyxel import DIRECTION

from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

from td.fungus import Fungus
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

def game_state_update(field: CellField):
    to_remove: list[Weapon] = []
    for w in weapons:
        if w.update(field) == False:
            to_remove.append(w)
    
    for w in to_remove:
        weapons.remove(w)

    if len(weapons) == 1:
        i = random.randint(0,2)
        match i:
            case 0:
                bolt = Bolt(position_left, DIRECTION.LEFT)
                bolt.launch(field)
                weapons.append(bolt)
            case 1:
                bolt = Bolt(position_center, DIRECTION.UP)
                bolt.launch(field)
                weapons.append(bolt)
            case 2:
                bolt = Bolt(position_right, DIRECTION.RIGHT)
                bolt.launch(field)
                weapons.append(bolt)


        # print("NO MORE WEAPONS")
        # pyxel.quit()