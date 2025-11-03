
from dataclasses import dataclass
from pyke_pyxel.base_types import Coord
from pyke_pyxel.button import Button
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.signals import Signals

@dataclass
class buttons:
    bolt = Button("bolt", 
                up_frame=Coord(1,14), 
                down_frame=Coord(5,14),
                col_tile_count=4, 
                row_tile_count=4)

BUTTONS = buttons()

def display(game: FieldGame):  
    BUTTONS.bolt.set_position(Coord(12, 22))
    game.hud.add_button(BUTTONS.bolt)

def hide(game: FieldGame):
    game.hud.remove_button(BUTTONS.bolt)

def mouse_down(x: int, y: int):
    if BUTTONS.bolt.contains(x, y):
        BUTTONS.bolt.push_down()

def mouse_up():
    if BUTTONS.bolt.is_down:
        BUTTONS.bolt.pop_up()
        Signals.send("ui_weapon_selected", "bolt")