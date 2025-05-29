from dataclasses import dataclass
from engine.game import Game, Player
from engine.map import Coord
from engine.sprite import Sprite, Animation, OpenableSprite, MovableSprite

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
        sprite = Sprite(OBJECTS.FIREBALL, Coord(6,5))
        sprite.add_animation("go", Animation(Coord(6, 5), 2))
        sprite.activate_animation("go")
        return sprite

class PLAYER:
    @staticmethod
    def SPRITE():
        sprite = MovableSprite("player", Coord(1, 1), 2)
        sprite.set_up_animation(Coord(4, 1), 2)
        sprite.set_down_animation(Coord(2, 1), 2)
        sprite.set_left_animation(Coord(6, 1), 2, True)
        sprite.set_right_animation(Coord(6, 1), 2, False)

        return sprite
    
class ENEMY:
    @staticmethod
    def DEMON():
        sprite = MovableSprite("enemy", Coord(1, 3), 1)
        sprite.set_up_animation(Coord(3, 3), 2)
        sprite.set_down_animation(Coord(1, 3), 2)
        sprite.set_left_animation(Coord(5, 3), 2, True)
        sprite.set_right_animation(Coord(5, 3), 2, False)

        return sprite