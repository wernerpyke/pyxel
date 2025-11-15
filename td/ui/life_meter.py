import math

from pyke_pyxel import Coord, COLOURS
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import CompoundSprite


class LifeMeter:

    def __init__(self) -> None:
        sprite = CompoundSprite("life_meter", 14, 2, resource_image_index=1)

        sprite.fill_row(row=1, from_col=1, to_col=12, tile_row=15,tile_cols=[3]) # middle
        sprite.fill_row(row=2, from_col=1, to_col=12, tile_row=16,tile_cols=[3])

        sprite.set_tile(1, 1, Coord(1,15)) # left cap
        sprite.set_tile(1, 2, Coord(1,16))
        sprite.set_tile(2, 1, Coord(2,15))
        sprite.set_tile(2, 2, Coord(2,16))

        sprite.set_tile(13, 1, Coord(4,15)) # right cap
        sprite.set_tile(13, 2, Coord(4,16))
        sprite.set_tile(14, 1, Coord(5,15)) 
        sprite.set_tile(14, 2, Coord(5,16))

        sprite.set_position(Coord(12, 1))

        self._sprite = sprite

        self._current_percentage: float = 0.5

    def show(self, game: Game):
        game.hud.add_sprite(self._sprite)

    def set_percentage(self, percentage: float):
        x, y = 16, 3
        center_width = (14 - 4) * 8
        height = 10

        self._sprite.clear_graphics()
        
        width = round(center_width * percentage)
        self._sprite.graph_rect(x, y, width, height, COLOURS.GREEN)
        
        x += width
        width = center_width - width
        self._sprite.graph_rect(x, y, width, height, COLOURS.RED)

        if not percentage == 0.5:
            if percentage >= self._current_percentage:
                self._sprite.graph_triangle(x, y, x, (y+height-1), (x+8), y, COLOURS.GREEN)
            else:
                self._sprite.graph_triangle(x, y, x, (y+height-1), (x-8), y, COLOURS.RED)
        self._current_percentage = percentage