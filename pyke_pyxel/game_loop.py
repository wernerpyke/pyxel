import random
from engine.sprite import Sprite, OpenableSprite
from engine.room import Room
from engine.player import Player
from engine.enemy import Enemy
from engine.signals import DIRECTION
from config import WALLS, DOOR, PROJECTILE, ENEMY


# -- ======  Helper Functions ======= --

def build_horizontal_wall(room: Room, wallType, fromColumn: int, toColumn: int, row: int):
    column = fromColumn
    while column <= toColumn:
        room.add_wall(wallType, column, row)
        column += 1

def choose_random_direction():
     return random.choice( [DIRECTION.UP, DIRECTION.DOWN, DIRECTION.LEFT, DIRECTION.RIGHT] )

# -- ======  Game Loop ======= --

def build_room(room: Room):

        room.add_wall(WALLS.BROWN, 5, 10)
        room.add_wall(WALLS.LAVA, 5, 11)
        room.add_wall(WALLS.BOULDER, 5, 12)
        room.add_wall(WALLS.GREY, 6, 13)
        room.add_wall(WALLS.GREY, 6, 14)

        room.add_door(DOOR.BROWN, 6, 10, True)

        build_horizontal_wall(room, WALLS.BROWN, 7, 15, 10)
        build_horizontal_wall(room, WALLS.BROWN, 6, 15, 15)

        room.add_wall(WALLS.GREY, 15, 11)
        room.add_wall(WALLS.GREY, 15, 12)
        room.add_wall(WALLS.GREY, 15, 13)
        room.add_wall(WALLS.GREY, 15, 14)

def set_player(player: Player):
    player.set_position(1, 10)

def game_started(room: Room, player: Player):
     print("GAME STARTED")

     enemy = room.add_enemy(ENEMY.DEMON, 10, 12)
     enemy.start_moving(choose_random_direction())

def player_blocked_by(sprite: Sprite):
    print(f"PLAYER BLOCKED BY {sprite.name} AT {sprite.position}")

def player_interacts_with_openable(sprite: OpenableSprite):
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