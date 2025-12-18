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
    map.add_trees(game)

    player = game.set_player(sprites.player(), speed_px_per_second=220)
    player.set_position(coord(18, 23))
    PLAYER.start(game)

    spinner = Spinner()
    spinner.set_position(coord(25, 1))
    game.room.add_enemy(spinner)

    spinner.move_to(coord(32, 30), game.map)

def game_update(game: RPGGame):
    PLAYER.check_input(pyxel.KEY_UP, DIRECTION.UP)
    PLAYER.check_input(pyxel.KEY_DOWN, DIRECTION.DOWN)
    PLAYER.check_input(pyxel.KEY_LEFT, DIRECTION.LEFT)
    PLAYER.check_input(pyxel.KEY_RIGHT, DIRECTION.RIGHT)

    PLAYER.update_movement()

def player_moved(player: Player):
    #print(f"MOVED {player.position}")
    PLAYER.check_enemies_to_attack()
    

def player_blocked(player: Player, value: Sprite|None):
    if sprite := value:
        print(f"BLOCKED {sprite.name}")
        match sprite.name:
            case "house":
                PLAYER.game.fx.scale_in_out(sprite, to_scale=1.2, duration=0.1)
    else:
        direction = player.active_dir if player.active_dir else player.facing_dir
        PLAYER.game.fx.camera_shake(0.1, direction)
    
    PLAYER.stop_movement()

    








