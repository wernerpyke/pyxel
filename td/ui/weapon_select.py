
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
    fungus = Button("fungus", 
                up_frame=Coord(9,14), 
                down_frame=Coord(13,14),
                col_tile_count=4, 
                row_tile_count=4)

BUTTONS = buttons()

def display(game: FieldGame):  
    BUTTONS.bolt.set_position(Coord(12, 36))
    BUTTONS.fungus.set_position(Coord(17, 36))

    game.hud.add_button(BUTTONS.bolt)
    game.hud.add_button(BUTTONS.fungus)

def hide(game: FieldGame):
    game.hud.remove_button(BUTTONS.bolt)
    game.hud.remove_button(BUTTONS.fungus)

def mouse_down(x: int, y: int) -> bool:
    if BUTTONS.bolt.contains(x, y):
        BUTTONS.bolt.push_down()
        return True # TODO - should this rather be done through game_loop.update_queue?
    elif BUTTONS.fungus.contains(x, y):
        BUTTONS.fungus.push_down()
        return True
    else:
        return False
    
def mouse_up():
    if BUTTONS.bolt.is_down:
        BUTTONS.bolt.pop_up()
        Signals.send("ui_weapon_selected", "bolt")
    elif BUTTONS.fungus.is_down:
        BUTTONS.fungus.pop_up()
        Signals.send("ui_weapon_selected", "fungus")