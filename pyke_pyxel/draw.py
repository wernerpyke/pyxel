import pyxel

from pyke_pyxel.button import Button

from ._base_types import Coord, Image
from . import GameSettings
from .sprite import CompoundSprite, Sprite, TextSprite

class _TileMap:

    def __init__(self, resource_position: Coord, tiles_wide: int, tiles_high: int, resource_index: int, settings: GameSettings):
        screen_width = settings.size.window
        screen_height = settings.size.window
        
        # Cache the rendered map into an image once-off
        repeat_cols = (screen_width // (tiles_wide * settings.size.tile)) + 1
        repeat_rows = (screen_height // (tiles_high * settings.size.tile)) + 1

        tm = pyxel.tilemaps[resource_index]
        tm_x = resource_position.x
        tm_y = resource_position.y
        tm_w = tiles_wide * settings.size.tile
        tm_h = tiles_high * settings.size.tile

        self._img = pyxel.Image(screen_width, screen_height)
        for col in range(repeat_cols):
            for row in range(repeat_rows):
                x = col * tm_w
                y = row * tm_h

                self._img.bltm(x, y, tm, tm_x, tm_y, tm_w, tm_h, settings.colours.sprite_transparency)



def background(colour: int):
    pyxel.cls(colour)

def text(sprite: TextSprite):
    pyxel.text(sprite.position.x, sprite.position.y, sprite._text, sprite._colour, font=sprite._font)

def image(image: Image, settings: GameSettings):
    width = settings.size.tile * image.col_tile_count
    height = settings.size.tile * image.row_tile_count

    position = image.position

    pyxel.blt(x=position.x,
              y=position.y,
              img=image.resource_image_index,
              u=image.frame.x,
              v=image.frame.y,
              w=width,
              h=height,
              colkey=settings.colours.sprite_transparency)

def button(button: Button, settings: GameSettings):
    frame = button._up_frame
    if button.is_down:
        frame = button._down_frame
    position = button._position

    width = settings.size.tile * button._col_tile_count
    height = settings.size.tile * button._row_tile_count

    pyxel.blt(x=position.x,
              y=position.y,
              img=button._resource_image_index,
              u=frame.x,
              v=frame.y,
              w=width,
              h=height,
              colkey=settings.colours.sprite_transparency)

def sprite(sprite: Sprite|CompoundSprite, settings: GameSettings):
    if isinstance(sprite, CompoundSprite):
        sprite._draw(settings)
        return

    frame = sprite.active_frame
    position = sprite._position

    width = settings.size.tile * sprite.col_tile_count
    height = settings.size.tile * sprite.row_tile_count
    if sprite.is_flipped:
        width *= -1

    pyxel.blt(x=position.x,
              y=position.y,
              img=sprite._resource_image_index,
              u=frame.x,
              v=frame.y,
              w=width,
              h=height,
              colkey=settings.colours.sprite_transparency)
    
def tile_map(tile_map: _TileMap, settings: GameSettings):
    screen_width = settings.size.window
    screen_height = settings.size.window
    
    pyxel.blt(0, 0, tile_map._img, 0, 0, screen_width, screen_height, settings.colours.sprite_transparency)