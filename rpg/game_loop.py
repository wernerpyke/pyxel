import random
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

def game_started(room: Room, player: Player):
     print("GAME STARTED")

     enemy = room.add_enemy(ENEMY.DEMON, 10, 12)
     enemy.start_moving(choose_random_direction())

def player_blocked_by(sprite: Sprite):
    print(f"PLAYER BLOCKED BY {sprite.name} AT {sprite.position}")

def player_interacts_with(sprite: OpenableSprite):
    if sprite.is_open: 
        print(f"PLAYER CLOSES {sprite.name}")
        sprite.close()
    else:
        print(f"PLAYER OPENS {sprite.name}")
        sprite.open()

def player_attacks(player: Player):
     player.launch_projectile(PROJECTILE.FIREBALL, 2, player.currentDirection)

def enemy_blocked_by(enemy: Enemy, other: Sprite):
     print(f"ENEMY {enemy.name} BLOCKED BY {other.name} AT {other.position}")
     enemy.start_moving(choose_random_direction())