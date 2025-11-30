from pyke_pyxel import Coord
from pyke_pyxel.drawable import Image, Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

image = Image(Coord(1, 1), cols=24, rows=10, image_index=1)
image.set_position(Coord(9, 10))

up = Image(Coord(1, 11), cols=16, rows=4, image_index=1)
down = up.clone_to(Coord(17, 11))
play_button = Button("play_button", up, down)

up = up.clone_to(Coord(1, 22))
down = down.clone_to(Coord(17, 22))
play_button.set_icon(up, down)
play_button.set_position(Coord(12, 24))

def display(game: Game):
    game.hud.add_bg(image)
    game.hud.add_button(play_button)

def hide(game: Game):
    game.hud.remove_bg(image)
    game.hud.remove_button(play_button)

def mouse_down(x: int, y: int):
    if play_button.contains(x, y):
        play_button.push_down()

def mouse_up():
    if play_button.is_down:
        play_button.pop_up()
        Signals.send("ui_game_start_selected", None)

def mouse_move(x: int, y: int):
    play_button.check_mouse_move(x, y)