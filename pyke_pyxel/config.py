from dataclasses import dataclass
from engine.game import Game, Player
from engine.map import Coord
from engine.sprite import Sprite, Animation, OpenableSprite

@dataclass
class OBJECTS:
    ROOM = "room"
    WALL = "wall"
    DOOR = "door"
    LAVA_WALL = "lava wall"
    FIREBALL = "fireball"

class WALLS:
    @staticmethod
    def BROWN():
        return Sprite(OBJECTS.WALL, Coord(2,14))
    
    @staticmethod
    def GREY():
        return Sprite(OBJECTS.WALL, Coord(8,14))

    @staticmethod
    def LAVA():
        return Sprite(OBJECTS.LAVA_WALL, Coord(6,14))
    
    @staticmethod
    def BOULDER():
        return Sprite(OBJECTS.WALL, Coord(7,14))

class DOOR:
    
    @staticmethod
    def BROWN():
        sprite = OpenableSprite(OBJECTS.DOOR, Coord(10, 15), Coord(8,15), Animation(Coord(8, 15), 3))
        return sprite
    
class PROTECTILE:

    @staticmethod
    def FIREBALL():
        return Sprite(OBJECTS.FIREBALL, Coord(5,5))

class PLAYER:
    @staticmethod
    def SPRITE():
        sprite = Sprite("player", idleFrame=Coord(1, 1))
        sprite.add_animation("down", Animation(Coord(2, 1), 2))
        sprite.add_animation("up", Animation(Coord(4, 1), 2))
        sprite.add_animation("left", Animation(Coord(6, 1), 2, True))
        sprite.add_animation("right", Animation(Coord(6, 1), 2, False))

        return sprite
    
    @staticmethod
    def MOVEMENT_SPEED():
        return 1
    