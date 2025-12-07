from dataclasses import dataclass
from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite, OpenableSprite, MovableSprite, Animation

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
        return Sprite(OBJECTS.WALL, coord(2,14))
    
    @staticmethod
    def GREY():
        return Sprite(OBJECTS.WALL, coord(8,14))

    @staticmethod
    def LAVA():
        return Sprite(OBJECTS.LAVA_WALL, coord(6,14))
    
    @staticmethod
    def BOULDER():
        return Sprite(OBJECTS.WALL, coord(7,14))

class DOOR:
    
    @staticmethod
    def BROWN():
        sprite = OpenableSprite(OBJECTS.DOOR, coord(10, 15), coord(8,15), Animation(coord(8, 15), 3))
        return sprite
    
class PROJECTILE:

    @staticmethod
    def FIREBALL():
        sprite = Sprite(OBJECTS.FIREBALL, coord(6,5))
        sprite.add_animation("go", Animation(coord(6, 5), 2))
        sprite.activate_animation("go")
        return sprite

class PLAYER:
    @staticmethod
    def SPRITE():
        sprite = MovableSprite("player", coord(1, 1), 2)
        sprite.set_up_animation(coord(4, 1), 2)
        sprite.set_down_animation(coord(2, 1), 2)
        sprite.set_left_animation(coord(6, 1), 2, True)
        sprite.set_right_animation(coord(6, 1), 2, False)

        return sprite
    
class ENEMY:
    @staticmethod
    def DEMON():
        sprite = MovableSprite("demon", coord(1, 3), 1)
        sprite.set_up_animation(coord(3, 3), 2)
        sprite.set_down_animation(coord(1, 3), 2)
        sprite.set_left_animation(coord(5, 3), 2, True)
        sprite.set_right_animation(coord(5, 3), 2, False)

        return sprite