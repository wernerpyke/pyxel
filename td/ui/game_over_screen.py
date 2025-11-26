from pyke_pyxel import Coord
from pyke_pyxel.drawable import Image
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

image = Image(Coord(1, 15), Coord(11, 12), col_tile_count=20, row_tile_count=4, resource_image_index=1)

def display(game: Game):
    game.hud.add_image(image)
    # print(f"GAME OVER AT {image.position.x}")

def hide(game: Game):
    game.hud.remove_image(image)

def mouse_down(x: int, y: int):
    pass

def mouse_up():
    Signals.send("ui_game_over_restart_selected", None)

def mouse_move(x: int, y: int):
    pass