
from dataclasses import dataclass
from pyke_pyxel import coord
from pyke_pyxel.drawable import ImageFactory, Button, Image
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

img = ImageFactory(cols=4, rows=4)

up = img.at(coord(9, 9))
down = img.at(coord(13, 9))

@dataclass
class buttons:
    star = Button("star", up, down)
    bolt = Button("bolt", up, down)
    fungus = Button("fungus", up, down)
    meteor = Button("meteor", up, down)

BUTTONS = buttons()
BUTTONS.bolt.set_icon(img.at(coord(1, 13)), img.at(coord(5, 13)))
BUTTONS.fungus.set_icon(img.at(coord(9, 13)), img.at(coord(13, 13)))
BUTTONS.meteor.set_icon(img.at(coord(17, 13)), img.at(coord(21, 13)))
BUTTONS.star.set_icon(img.at(coord(25, 13)), img.at(coord(29, 13)))


def display(game: Game):  
    BUTTONS.star.set_position(coord(12, 36))
    BUTTONS.bolt.set_position(coord(17, 36))
    BUTTONS.fungus.set_position(coord(22, 36))
    BUTTONS.meteor.set_position(coord(27, 36))

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
    BUTTONS.bolt.check_mouse_move(x, y)
    BUTTONS.fungus.check_mouse_move(x, y)
    BUTTONS.meteor.check_mouse_move(x, y)
    BUTTONS.star.check_mouse_move(x, y)

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