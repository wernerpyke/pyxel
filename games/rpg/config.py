from dataclasses import dataclass
from pyke_pyxel import coord
from pyke_pyxel.sprite import Sprite, OpenableSprite, MovableSprite, Animation, AnimationFactory

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
        sprite = OpenableSprite(OBJECTS.DOOR, coord(10, 15), coord(8,15))
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
        sprite = MovableSprite("player", coord(1, 1), speed_px_per_second=30)

        anim = AnimationFactory(2)
        sprite.set_up_animation(anim.at(coord(4, 1)))
        sprite.set_down_animation(anim.at(coord(2, 1)))
        sprite.set_left_animation(anim.at(coord(6, 1), flip=True))
        sprite.set_right_animation(anim.at(coord(6, 1)))

        return sprite
    
class ENEMY:
    @staticmethod
    def DEMON():
        sprite = MovableSprite("demon", coord(1, 3), speed_px_per_second=20)

        anim = AnimationFactory(2)
        sprite.set_up_animation(anim.at(coord(3, 3)))
        sprite.set_down_animation(anim.at(coord(1, 3)))
        sprite.set_left_animation(anim.at(coord(5, 3), flip=True))
        sprite.set_right_animation(anim.at(coord(5, 3)))

        return sprite