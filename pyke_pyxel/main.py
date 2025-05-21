import config
from engine.game import Game
from engine.objects.map import Coord
from engine.objects.sprite import Animation

def create_horizontal_wall(game: Game, wallType, fromColumn: int, toColumn: int, row: int):
    column = fromColumn
    while column <= toColumn:
        game.add_wall_sprite(wallType, column, row)
        column += 1

def create_room(game: Game):
        game = game

        game.add_wall_sprite(config.WALLS.BROWN, 5, 10)
        game.add_wall_sprite(config.WALLS.LAVA, 5, 11)
        game.add_wall_sprite(config.WALLS.BOULDER, 6, 12)
        game.add_wall_sprite(config.WALLS.GREY, 6, 13)

        game.add_door_sprite(config.DOOR.BROWN, 6, 10, True)

        create_horizontal_wall(game, config.WALLS.BOULDER, 7, 10, 10)

def create_player(game):
    player = config.add_player(game)
    player.set_position(1, 10)

# ==================================

game = Game("Go Pyke!", "assets/sample.pyxres")

create_room(game)
create_player(game)

game.start()

# class App:

#    def __init__(self):
        
#App()