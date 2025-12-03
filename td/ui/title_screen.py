from pyke_pyxel import coord
from pyke_pyxel.drawable import ImageFactory, Image, Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

image = Image(coord(1, 1), cols=24, rows=10, image_index=1)
image.set_position(coord(9, 10))

img = ImageFactory(cols=16, rows=4, image_index=1)

play_button = Button("play_button", img.at(coord(1, 11)), img.at(coord(17, 11)))
play_button.set_icon(img.at(coord(1, 22)), img.at(coord(17, 22)))
play_button.set_position(coord(12, 24))

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
        Signals.send("ui_game_start_selected")

def mouse_move(x: int, y: int):
    play_button.check_mouse_move(x, y)