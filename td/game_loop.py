from dataclasses import dataclass
from pyke_pyxel import COLOURS
from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

import weapons
import enemies

@dataclass
class game_state:
    score: int = 0

STATE = game_state()

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

def enemy_killed(game: FieldGame):
    STATE.score += 1
    text = game.hud.get_text()
    text.set_colour(COLOURS.GREEN_MINT)
    text.set_text(f"{STATE.score}")

def enemy_wins(game: FieldGame):
    STATE.score -= 1
    text = game.hud.get_text()
    text.set_colour(COLOURS.RED)
    text.set_text(f"{STATE.score}")