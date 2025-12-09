import random
import pyxel

from pyke_pyxel import log_info, DIRECTION
from pyke_pyxel.map import Map
from pyke_pyxel.sprite import Sprite, OpenableSprite
from pyke_pyxel.rpg import RPGGame, Enemy, Player
from config import PROJECTILE, ENEMY

# -- ======  Helper Functions ======= --

def choose_random_direction():
     return random.choice( [DIRECTION.UP, DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.RIGHT] )

# -- ======  Game Loop ======= --

def game_started(game: RPGGame):
     log_info("GAME STARTED")

     enemy = game.room.add_enemy(ENEMY.DEMON, 10, 12)
     enemy.start_moving(choose_random_direction())

def game_update(game: RPGGame):
     keyboard = game.keyboard
     player = game.player

     if keyboard.was_pressed(pyxel.KEY_X):
           if openable := player.adjacent_openable(game.map):
               player_interacts_with(openable, game.map)
            
     elif keyboard.was_pressed(pyxel.KEY_Z):
          player.launch_projectile(PROJECTILE.FIREBALL, 60, player.facing_dir)

     # TODO - move the below to a default helper is pyke_pyxel.rpg
     if keyboard.was_pressed(pyxel.KEY_UP):
          player.start_moving(DIRECTION.UP)
     elif keyboard.was_released(pyxel.KEY_UP):
          player.stop_moving()
     elif keyboard.was_pressed(pyxel.KEY_DOWN):
          player.start_moving(DIRECTION.DOWN)
     elif keyboard.was_released(pyxel.KEY_DOWN):
          player.stop_moving()
     elif keyboard.was_pressed(pyxel.KEY_LEFT):
          player.start_moving(DIRECTION.LEFT)
     elif keyboard.was_released(pyxel.KEY_LEFT):
          player.stop_moving()
     elif keyboard.was_pressed(pyxel.KEY_RIGHT):
          player.start_moving(DIRECTION.RIGHT)
     elif keyboard.was_released(pyxel.KEY_RIGHT):
          player.stop_moving()

def player_blocked_by(player: Player, value):
     if value:
          log_info(f"PLAYER BLOCKED BY {value.name} AT {value.position}")
     else:
          log_info("PLAYER BLOCKED BY EDGE")

def player_interacts_with(sprite: OpenableSprite, map: Map):     
     if sprite.is_open: 
        log_info(f"PLAYER CLOSES {sprite.name}")
        sprite.close()
        map.mark_closed(sprite.position)
     else:
        log_info(f"PLAYER OPENS {sprite.name}")
        sprite.open()
        map.mark_open(sprite.position)

def enemy_blocked_by(enemy: Enemy, value: Sprite):
     log_info(f"ENEMY {enemy.name} BLOCKED BY {value.name} AT {value.position}")
     enemy.start_moving(choose_random_direction())