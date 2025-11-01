from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

import weapons
import enemies

def game_started(game: FieldGame):
    print("Game Started")

    field = game.field

    enemies.launch_skeleton(game)

    weapons.launch_fungus(field)

def game_update(game: FieldGame):
    enemies.update(game)

def game_field_update(field: CellField):
    weapons.update(field)

    if not weapons.has_active_weapon("fungus"):
        weapons.launch_fungus(field)

    if not weapons.has_active_weapon("bolt"):
        weapons.launch_bolt(field)
