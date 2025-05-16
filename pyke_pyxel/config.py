from dataclasses import dataclass
from engine.game import Game, Player
from engine.objects.map import Coord
from engine.objects.sprite import Sprite, Animation

class WALLS:
    @staticmethod
    def BROWN():
        return Sprite(Coord(2,14))
    
    @staticmethod
    def GREY():
        return Sprite(Coord(8,14))

    @staticmethod
    def LAVA():
        return Sprite(Coord(6,14))
    
    @staticmethod
    def BOULDER():
        return Sprite(Coord(7,14))
    
    

def add_player(game: Game) -> Player:
    return game.add_player(
            idleFrame=Coord(1, 1),
            downAnimation=Animation(Coord(2, 1), 2),
            upAnimation=Animation(Coord(4, 1), 2),
            leftAnimation=Animation(Coord(6, 1), 2, True),
            rightAnimation=Animation(Coord(6, 1), 2, False),
            movementSpeed=1)