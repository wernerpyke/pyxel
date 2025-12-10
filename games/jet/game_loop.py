import pyxel
from pyke_pyxel import DIRECTION, coord
from pyke_pyxel.rpg import RPGGame, Player
from pyke_pyxel.sprite import Sprite

import sprites
import map
from games.jet.player import PLAYER
from games.jet.enemies.spinner import Spinner

def game_started(game: RPGGame):
    map.add_house(game)

    player = game.set_player(sprites.player(), speed_px_per_second=220)
    player.set_position(coord(10, 10))
    PLAYER.start(game)

    spinner = Spinner()
    spinner.set_position(coord(5, 5))
    game.room.add_enemy(spinner)
    spinner.move_to(coord(10, 10))

def game_update(game: RPGGame):
    PLAYER.check_input(pyxel.KEY_UP, DIRECTION.UP)
    PLAYER.check_input(pyxel.KEY_DOWN, DIRECTION.DOWN)
    PLAYER.check_input(pyxel.KEY_LEFT, DIRECTION.LEFT)
    PLAYER.check_input(pyxel.KEY_RIGHT, DIRECTION.RIGHT)
    # STATE.check_input_none(pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_LEFT, pyxel.KEY_RIGHT)

    PLAYER.update_movement()

def player_moved(player: Player):
    # print(f"MOVED {player.position}")
    pass

def player_blocked(player: Player, value: Sprite|None):
    if sprite := value:
        print(f"BLOCKED {sprite.name}")
        match sprite.name:
            case "house":
                PLAYER.game.fx.scale_in_out(sprite, to_scale=1.2, duration=0.1)
    
    PLAYER.stop_movement()

    








