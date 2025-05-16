import pyxel
import constants
from .objects.sprite import Sprite

def background():
    pyxel.cls(constants.COLOURS.BLACK)

def sprite(sprite: Sprite):
    frame = sprite.active_frame
    position = sprite.position

    # width = constants.SIZE.TILE
    # if (sprite.is_flipped):
    #     width *= -1
    
    # print(f"draw.sprite() x:{frame.x} y:{frame.y}")

    pyxel.blt(x=position.x,
              y=position.y,
              img=0,
              u=frame.x,
              v=frame.y,
              w=(constants.SIZE.TILE * -1) if sprite.is_flipped else constants.SIZE.TILE,
              h=constants.SIZE.TILE,
              colkey=constants.COLOURS.SPRITE_TRANSPARENCY)