from engine.sprite import Sprite, OpenableSprite
from engine.room import Room
from engine.player import Player
from config import WALLS, DOOR, PROTECTILE

def make_horizontal_wall(room: Room, wallType, fromColumn: int, toColumn: int, row: int):
    column = fromColumn
    while column <= toColumn:
        room.add_wall(wallType, column, row)
        column += 1

def build_room(room: Room):

        room.add_wall(WALLS.BROWN, 5, 10)
        room.add_wall(WALLS.LAVA, 5, 11)
        room.add_wall(WALLS.BOULDER, 6, 12)
        room.add_wall(WALLS.GREY, 6, 13)

        room.add_door(DOOR.BROWN, 6, 10, True)

        make_horizontal_wall(room, WALLS.BOULDER, 7, 10, 10)

def set_player(player: Player):
    player.set_position(1, 10)

def game_started(player: Player):
     print("GAME STARTED")

def player_blocked_by(sprite: Sprite):
    print(f"PLAYER BLOCKED BY {sprite.name} at {sprite.position}")

def player_interacts_with_openable(sprite: OpenableSprite):
    if sprite.is_open: 
        print(f"PLAYER CLOSES {sprite.name}")
        sprite.close()
    else:
        print(f"PLAYER OPENS {sprite.name}")
        sprite.open()

def player_attacks(player: Player):
     player.launch_projectile(PROTECTILE.FIREBALL(), 2, player.currentDirection)