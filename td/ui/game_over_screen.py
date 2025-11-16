from pyke_pyxel import Coord, Image
from pyke_pyxel.button import Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

image = Image(Coord(1, 15), Coord(12, 10), col_tile_count=20, row_tile_count=4, resource_image_index=1)

def display(game: Game):
    game.hud.add_image(image)

def hide(game: Game):
    game.hud.remove_image(image)

def mouse_down(x: int, y: int):
    pass

def mouse_up():
    Signals.send("ui_game_over_restart_selected", None)

def mouse_move(x: int, y: int):
    pass