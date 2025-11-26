
from dataclasses import dataclass
from pyke_pyxel import Coord
from pyke_pyxel.drawable import Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

@dataclass
class buttons:
    star = Button("star", 
                up_frame=Coord(25,13), 
                down_frame=Coord(29,13),
                col_tile_count=4, 
                row_tile_count=4)
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

def display(game: Game):  
    BUTTONS.star.set_position(Coord(12, 36))
    BUTTONS.bolt.set_position(Coord(17, 36))
    BUTTONS.fungus.set_position(Coord(22, 36))
    BUTTONS.meteor.set_position(Coord(27, 36))

    game.hud.add_button(BUTTONS.star)
    game.hud.add_button(BUTTONS.bolt)
    game.hud.add_button(BUTTONS.fungus)
    game.hud.add_button(BUTTONS.meteor)

def hide(game: Game):
    game.hud.remove_button(BUTTONS.star)
    game.hud.remove_button(BUTTONS.bolt)
    game.hud.remove_button(BUTTONS.fungus)
    game.hud.remove_button(BUTTONS.meteor)

def mouse_down(x: int, y: int) -> bool:
    if BUTTONS.star.contains(x, y):
        BUTTONS.star.push_down()
        return True
    elif BUTTONS.bolt.contains(x, y):
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
    if BUTTONS.star.is_down and not BUTTONS.star.contains(x, y):
        BUTTONS.star.pop_up()
    elif BUTTONS.bolt.is_down and not BUTTONS.bolt.contains(x, y):
        BUTTONS.bolt.pop_up()
    elif BUTTONS.fungus.is_down and not BUTTONS.fungus.contains(x, y):
        BUTTONS.fungus.pop_up()
    elif BUTTONS.meteor.is_down and not BUTTONS.meteor.contains(x, y):
        BUTTONS.meteor.pop_up()

def mouse_up():
    if BUTTONS.star.is_down:
        BUTTONS.star.pop_up()
        Signals.send("ui_weapon_selected", "star")
    elif BUTTONS.bolt.is_down:
        BUTTONS.bolt.pop_up()
        Signals.send("ui_weapon_selected", "bolt")
    elif BUTTONS.fungus.is_down:
        BUTTONS.fungus.pop_up()
        Signals.send("ui_weapon_selected", "fungus")
    elif BUTTONS.meteor.is_down:
        BUTTONS.meteor.pop_up()
        Signals.send("ui_weapon_selected", "meteor")