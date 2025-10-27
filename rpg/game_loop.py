import random
from pyke_pyxel import log_info
from pyke_pyxel.character_game import CharacterGame
from pyke_pyxel.sprite import Sprite, OpenableSprite
from pyke_pyxel.room import Room
from pyke_pyxel.player import Player
from pyke_pyxel.enemy import Enemy
from pyke_pyxel import DIRECTION
from config import PROJECTILE, ENEMY

# -- ======  Helper Functions ======= --

def choose_random_direction():
     return random.choice( [DIRECTION.UP, DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.RIGHT] )

# -- ======  Game Loop ======= --

def game_started(game: CharacterGame):
     log_info("GAME STARTED")

     enemy = game.room.add_enemy(ENEMY.DEMON, 10, 12)
     enemy.start_moving(choose_random_direction())

def player_blocked_by(sprite: Sprite):
    log_info(f"PLAYER BLOCKED BY {sprite.name} AT {sprite.position}")

def player_interacts_with(sprite: OpenableSprite):
    if sprite.is_open: 
        log_info(f"PLAYER CLOSES {sprite.name}")
        sprite.close()
    else:
        log_info(f"PLAYER OPENS {sprite.name}")
        sprite.open()

def player_attacks(player: Player):
     player.launch_projectile(PROJECTILE.FIREBALL, 2, player.currentDirection)

def enemy_blocked_by(enemy: Enemy, other: Sprite):
     log_info(f"ENEMY {enemy.name} BLOCKED BY {other.name} AT {other.position}")
     enemy.start_moving(choose_random_direction())