from pyke_pyxel import Coord, COLOURS
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import CompoundSprite


class LifeMeter:

    def __init__(self) -> None:
        sprite = CompoundSprite("life_meter", 14, 2, resource_image_index=1)

        sprite.fill_row(row=1, from_col=1, to_col=12, tile_row=1,tile_cols=[27]) # middle
        sprite.fill_row(row=2, from_col=1, to_col=12, tile_row=2,tile_cols=[27])

        sprite.set_tile(1, 1, Coord(25,1)) # left cap
        sprite.set_tile(1, 2, Coord(25,2))
        sprite.set_tile(2, 1, Coord(26,1))
        sprite.set_tile(2, 2, Coord(26,2))

        sprite.set_tile(13, 1, Coord(28,1)) # right cap
        sprite.set_tile(13, 2, Coord(28,2))
        sprite.set_tile(14, 1, Coord(29,1)) 
        sprite.set_tile(14, 2, Coord(29,2))

        self._sprite = sprite

        self._current_percentage: float = 0.5

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