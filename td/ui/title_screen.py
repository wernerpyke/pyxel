from pyke_pyxel import Coord
from pyke_pyxel.drawable import Image, Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

image = Image(Coord(1, 1), col_tile_count=24, row_tile_count=10, resource_image_index=1)
image.set_position(Coord(9, 10))

play_button = Button("play_button", Coord(1, 11), Coord(17, 11), col_count=16, row_count=4, resource_image_index=1)
play_button.set_icon(Coord(1, 22), Coord(17, 22))
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