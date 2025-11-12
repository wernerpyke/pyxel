from pyke_pyxel.rpg.room import Room
from pyke_pyxel.rpg.player import Player
from config import WALLS, DOOR


# -- ======  Helper Functions ======= --

def build_horizontal_wall(room: Room, wallType, fromColumn: int, toColumn: int, row: int):
    column = fromColumn
    while column <= toColumn:
        room.add_wall(wallType, column, row)
        column = column + 1



# -- ======  Game Load ======= --

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

def set_player_position(player: Player):
    player.set_position(1, 10)