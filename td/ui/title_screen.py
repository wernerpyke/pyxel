from pyke_pyxel.base_types import Coord, Image
from pyke_pyxel.button import Button
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.signals import Signals

image = Image(Coord(1, 1), Coord(8, 10), col_tile_count=24, row_tile_count=10, resource_image_index=1)
play_button = Button("play_button", Coord(1, 11), Coord(17, 11), col_tile_count=16, row_tile_count=4, resource_image_index=1)

def display(game: FieldGame):
    game.hud.add_image(image)
    play_button.set_position(Coord(12, 24))
    game.hud.add_button(play_button)

def hide(game: FieldGame):
    game.hud.remove_image(image)
    game.hud.remove_button(play_button)

def mouse_down(x: int, y: int):
    if play_button.contains(x, y):
        play_button.push_down()

def mouse_up():
    if play_button.is_down:
        play_button.pop_up()
        Signals.send("ui_game_start_selected", None)

def mouse_move(x: int, y: int):
    if not play_button.contains(x, y):
        play_button.pop_up()