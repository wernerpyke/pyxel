import pyxel

from pyke_pyxel.button import Button

from .base_types import Image, TileMap
from .settings import GameSettings
from .sprite import CompoundSprite, Sprite, TextSprite

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

def sprite(sprite: Sprite, settings: GameSettings):
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
    
def compound_sprite(sprite: CompoundSprite, settings: GameSettings):
    for c in range(0, len(sprite.cols)):
        row = sprite.cols[c]
        for r in range(0, len(row)):
            tile = row[r]
            if tile:

                width = settings.size.tile
                height = settings.size.tile
                # if tile.is_flipped: TODO sprite.is_flipped
                #    width *= -1

                pyxel.blt(x=sprite.position.x + (c * settings.size.tile),
                          y=sprite.position.y + (r * settings.size.tile),
                          img=sprite._resource_image_index,
                          u=tile.x,
                          v=tile.y,
                          w=width,
                          h=height,
                          colkey=settings.colours.sprite_transparency)
    
def tile_map(tile_map: TileMap, settings: GameSettings):
    screen_width = settings.size.window
    screen_height = settings.size.window

    repeat_cols = (screen_width // (tile_map.tiles_wide * 8)) + 1
    repeat_rows = (screen_height // (tile_map.tiles_high * 8)) + 1

    tm = pyxel.tilemaps[tile_map.resource_index]
    tm_x = tile_map.resource_position.x
    tm_y = tile_map.resource_position.y
    tm_w = tile_map.tiles_wide * settings.size.tile
    tm_h = tile_map.tiles_high * settings.size.tile

    for col in range(repeat_cols):
        for row in range(repeat_rows):
            x = col * tm_w
            y = row * tm_h

            pyxel.bltm(
                x, y,
                tm,
                tm_x, tm_y,
                tm_w, tm_h,
                colkey=settings.colours.sprite_transparency)