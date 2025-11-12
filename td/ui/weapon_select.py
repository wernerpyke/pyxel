
from dataclasses import dataclass
from pyke_pyxel.base_types import Coord
from pyke_pyxel.button import Button
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.signals import Signals

@dataclass
class buttons:
    bolt = Button("bolt", 
                up_frame=Coord(1,13), 
                down_frame=Coord(5,13),
                col_tile_count=4, 
                row_tile_count=4)
    fungus = Button("fungus", 
                up_frame=Coord(9,13), 
                down_frame=Coord(13,13),
                col_tile_count=4, 
                row_tile_count=4)
    meteor = Button("meteor", 
                up_frame=Coord(17,13), 
                down_frame=Coord(21,13),
                col_tile_count=4, 
                row_tile_count=4)

BUTTONS = buttons()

def display(game: CellAutoGame):  
    BUTTONS.bolt.set_position(Coord(12, 36))
    BUTTONS.fungus.set_position(Coord(17, 36))
    BUTTONS.meteor.set_position(Coord(22, 36))

    game.hud.add_button(BUTTONS.bolt)
    game.hud.add_button(BUTTONS.fungus)
    game.hud.add_button(BUTTONS.meteor)

def hide(game: CellAutoGame):
    game.hud.remove_button(BUTTONS.bolt)
    game.hud.remove_button(BUTTONS.fungus)
    game.hud.remove_button(BUTTONS.meteor)

def mouse_down(x: int, y: int) -> bool:
    if BUTTONS.bolt.contains(x, y):
        BUTTONS.bolt.push_down()
        return True # TODO - should this rather be done through game_loop.update_queue?
    elif BUTTONS.fungus.contains(x, y):
        BUTTONS.fungus.push_down()
        return True
    elif BUTTONS.meteor.contains(x, y):
        BUTTONS.meteor.push_down()
        return True
    else:
        return False
    
def mouse_move(x: int, y: int):
    if BUTTONS.bolt.is_down and not BUTTONS.bolt.contains(x, y):
        BUTTONS.bolt.pop_up()
    elif BUTTONS.fungus.is_down and not BUTTONS.fungus.contains(x, y):
        BUTTONS.fungus.pop_up()
    elif BUTTONS.meteor.is_down and not BUTTONS.meteor.contains(x, y):
        BUTTONS.meteor.pop_up()

def mouse_up():
    if BUTTONS.bolt.is_down:
        BUTTONS.bolt.pop_up()
        Signals.send("ui_weapon_selected", "bolt")
    elif BUTTONS.fungus.is_down:
        BUTTONS.fungus.pop_up()
        Signals.send("ui_weapon_selected", "fungus")
    elif BUTTONS.meteor.is_down:
        BUTTONS.meteor.pop_up()
        Signals.send("ui_weapon_selected", "meteor")