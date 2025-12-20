import pyxel
from pyke_pyxel import DIRECTION, coord
from pyke_pyxel.rpg import RPGGame, Player
from pyke_pyxel.rpg.enemy import Enemy
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite

import sprites
import map
from games.jet.player import PLAYER
from games.jet.enemies import launch_spinner

def game_started(game: RPGGame):
    map.add_house(game)
    map.add_trees(game)

    player = game.set_player(sprites.player(), speed_px_per_second=220)
    player.set_position(coord(18, 23))
    PLAYER.start(game)

    for i in range(8):
        launch_spinner(game)

def game_update(game: RPGGame):
    PLAYER.check_input(pyxel.KEY_UP, DIRECTION.UP)
    PLAYER.check_input(pyxel.KEY_DOWN, DIRECTION.DOWN)
    PLAYER.check_input(pyxel.KEY_LEFT, DIRECTION.LEFT)
    PLAYER.check_input(pyxel.KEY_RIGHT, DIRECTION.RIGHT)

    PLAYER.update_movement()

def player_moved(player: Player):
    PLAYER.check_enemies_to_attack()

def player_blocked(player: Player, value: Sprite|None):
    if sprite := value:
        match sprite.name:
            case "house":
                PLAYER.game.fx.scale_in_out(sprite, to_scale=1.2, duration=0.1)
    else:
        direction = player.active_dir if player.active_dir else player.facing_dir
        PLAYER.game.fx.camera_shake(0.1, direction)
    
    PLAYER.stop_movement()


def enemy_stopped(enemy: Enemy):
    # Hit the house
    enemy.move_to(coord(22,22))

def enemy_blocked(enemy: Enemy, value: Sprite|None):
    def _remove_enemy(sprite_id: int):
        print(f"REMOVE ENEMY {enemy.name}")
        enemy.remove()

    enemy.stop_moving()

    if sprite := value:
        if sprite.name == "house":
            print("ENEMY KILLS")
            enemy._sprite.activate_animation("kill", on_animation_end=_remove_enemy)
        else:
            print(f"ENEMY BLOCKED {enemy.name} by {sprite.name}")
    else:
        print(f"ENEMY BLOCKED {enemy.name}")









