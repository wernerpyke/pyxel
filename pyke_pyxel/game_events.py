from engine.game import Game
from engine.sprite import Sprite
import config

def make_horizontal_wall(game: Game, wallType, fromColumn: int, toColumn: int, row: int):
    column = fromColumn
    while column <= toColumn:
        game.add_wall(wallType, column, row)
        column += 1

def create_room(game: Game):

        game.add_wall(config.WALLS.BROWN, 5, 10)
        game.add_wall(config.WALLS.LAVA, 5, 11)
        game.add_wall(config.WALLS.BOULDER, 6, 12)
        game.add_wall(config.WALLS.GREY, 6, 13)

        game.add_door(config.DOOR.BROWN, 6, 10, True)

        make_horizontal_wall(game, config.WALLS.BOULDER, 7, 10, 10)

        game.add_wall(config.PROTECTILE.FIREBALL, 2, 12)

def create_player(game: Game):
    player = game.add_player(config.PLAYER.SPRITE(), config.PLAYER.MOVEMENT_SPEED())
    player.set_position(1, 10)


def player_blocked(blockedBy: Sprite):
    print(f"PLAYER BLOCKED BY {blockedBy.name} at {blockedBy.position}")