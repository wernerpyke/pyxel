from pyke_pyxel import Coord
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import CompoundSprite


class LifeMeter:

    def __init__(self) -> None:
        sprite = CompoundSprite("life_meter", 12, 2, resource_image_index=1)

        sprite.fill_row(row=1, from_col=1, to_col=12, tile_row=15,tile_cols=[2]) # middle
        sprite.fill_row(row=2, from_col=1, to_col=12, tile_row=16,tile_cols=[2])

        sprite.set_tile(1, 1, Coord(1,15)) # left cap
        sprite.set_tile(1, 2, Coord(1,16))

        sprite.set_tile(12, 1, Coord(7,15)) # right cap
        sprite.set_tile(12, 2, Coord(7,16))

        sprite.set_position(Coord(14, 1))

        self._sprite = sprite

    def show(self, game: Game):
        game.hud.add_sprite(self._sprite)