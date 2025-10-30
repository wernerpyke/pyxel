import pyxel

from .base_types import TileMap
from .game_settings import GameSettings
from .sprite import CompoundSprite, Sprite

def background(colour: int):
    pyxel.cls(colour)

def sprite(sprite: Sprite, settings: GameSettings):
    frame = sprite.active_frame
    position = sprite._position

    width = settings.size.tile * sprite.col_tile_count
    height = settings.size.tile * sprite.row_tile_count
    if sprite.is_flipped:
        width *= -1

    pyxel.blt(x=position.x,
              y=position.y,
              img=0,
              u=frame.x,
              v=frame.y,
              w=width, # (settings.size.tile * -1) if sprite.is_flipped else settings.size.tile,
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
                          img=0,
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

    tm = pyxel.tilemap(0)
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