import pyxel
from .game_settings import GameSettings
from .sprite import Sprite

def background(settings: GameSettings):
    pyxel.cls(settings.colours.black)

def sprite(sprite: Sprite, settings: GameSettings):
    frame = sprite.active_frame
    position = sprite._position

    # width = constants.SIZE.TILE
    # if (sprite.is_flipped):
    #     width *= -1
    
    # print(f"draw.sprite() x:{frame.x} y:{frame.y}")

    pyxel.blt(x=position.x,
              y=position.y,
              img=0,
              u=frame.x,
              v=frame.y,
              w=(settings.size.tile * -1) if sprite.is_flipped else settings.size.tile,
              h=settings.size.tile,
              colkey=settings.colours.sprite_transparency)