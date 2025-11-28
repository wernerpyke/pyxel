
from pyke_pyxel import Coord
from pyke_pyxel import COLOURS
from pyke_pyxel.drawable import Image, Rect
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals

image = Image(Coord(1, 19), col_tile_count=20, row_tile_count=4, resource_image_index=1)
image.set_position(Coord(10, 7))

def _show_options(game: Game):
    bg = Rect(position=Coord(8, 6), col_count=24, row_count=30)
    bg.set_background(COLOURS.BLACK)
    bg.set_border(COLOURS.BLUE_DARK, 2)
    game.hud.add_bg(bg)
    game.hud.add_bg(image)

def display(game: Game):
    def intro_complete(sender):
        game.pause()
        Signals.disconnect("ui_power_up_intro_complete", intro_complete)
        _show_options(game)

    Signals.connect("ui_power_up_intro_complete", intro_complete)
    game.fx.scale_in(image, duration=0.3, completion_signal="ui_power_up_intro_complete")

def mouse_down(x: int, y: int):
    pass
    # if play_button.contains(x, y):
    #    play_button.push_down()

def mouse_up():
    pass
    #if play_button.is_down:
    #    play_button.pop_up()
    #    Signals.send("ui_game_start_selected", None)

def mouse_move(x: int, y: int):
    pass
    #if not play_button.contains(x, y):
    #    play_button.pop_up()