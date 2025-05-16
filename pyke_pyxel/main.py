import config
from engine.game import Game
from engine.objects.map import Coord
from engine.objects.sprite import Animation

class App:

    def create_room(self):
        game = self.game
        walls = config.WALLS

        game.add_wall(walls.BROWN(), 5, 10)
        game.add_wall(walls.LAVA(), 5, 11)
        game.add_wall(walls.BOULDER(), 6, 12)
        game.add_wall(walls.GREY(), 6, 13)

    def create_player(self):
        player = config.add_player(self.game)
        player.set_position(1, 10)

    # ==================================

    def __init__(self):
        self.game = Game("Go Pyke!", "assets/sample.pyxres")

        self.create_room()

        self.create_player()
        
        self.game.start()

App()