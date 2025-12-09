import pyxel
from pyke_pyxel import DIRECTION, COLOURS
from pyke_pyxel.rpg import RPGGame, Player
from pyke_pyxel.sprite import Sprite

from games.jet.player import PLAYER

def game_started(game: RPGGame):
    PLAYER.start(game)

def game_update(game: RPGGame):
    PLAYER.check_input(pyxel.KEY_UP, DIRECTION.UP)
    PLAYER.check_input(pyxel.KEY_DOWN, DIRECTION.DOWN)
    PLAYER.check_input(pyxel.KEY_LEFT, DIRECTION.LEFT)
    PLAYER.check_input(pyxel.KEY_RIGHT, DIRECTION.RIGHT)
    # STATE.check_input_none(pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_LEFT, pyxel.KEY_RIGHT)

    PLAYER.update_movement()

def player_blocked(player: Player, value: Sprite|None):
    print(f"BLOCKED {value}")
    PLAYER.stop_movement()
    








