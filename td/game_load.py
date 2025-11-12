from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.sprite import Animation, Sprite, CompoundSprite, TextSprite

from td.state import STATE

def load_level(game: CellAutoGame):
    game.set_tilemap(Coord(1, 1), 8, 8)

    mountain = Sprite("mountain", Coord(1, 21), 32, 12)
    mountain.set_position(Coord(4, 1))
    game.add_sprite(mountain)

    _add_plants(game)

    _add_base(game)
    STATE.ui.score_text.set_position(Coord(2,2))
    game.hud.add_text(STATE.ui.score_text)

def _add_plants(game: CellAutoGame):
    s = CompoundSprite("plants", 40, 4)
    s.fill_row(1, 1, 40, tile_row=9, tile_cols=[1, 2, 3, 4])
    s.fill_row(2, 1, 40, tile_row=10, tile_cols=[1, 2, 3, 4])
    s.fill_row(3, 1, 40, tile_row=11, tile_cols=[1, 2, 3, 4])
    s.fill_row(4, 1, 40, tile_row=12, tile_cols=[1, 2, 3, 4])
    s.set_position(Coord(1, 37))
    game.add_sprite(s)

def _add_base(game):
    base = Sprite("base", Coord(1, 1), col_tile_count=8, row_tile_count=7)
    base.set_position(Coord(16, 30))
    base.add_animation("loop", Animation(Coord(1, 1), 4))
    base.activate_animation("loop")
    game.add_sprite(base)

def vertical_bar(game: CellAutoGame, position: Coord):
    bar = CompoundSprite("bar", 3, 20)
    bar.set_position(position)

    bar.fill_tiles(Coord(3, 11))
    # Top Cap
    bar.set_tile(1, 1, Coord(2, 10))
    bar.set_tile(2, 1, Coord(3, 10))
    bar.set_tile(3, 1, Coord(4, 10))
    bar.set_tile(1, 2, Coord(2, 11))
    bar.set_tile(3, 2, Coord(4, 11))

    # Middle Left
    bar.fill_col(col=1, from_row=3, to_row=18, tile_col=2, tile_rows=[12, 13, 14])

    # Middle Right
    bar.fill_col(col=3, from_row=3, to_row=18, tile_col=4, tile_rows=[12, 13, 14])
    
    # Bottom Cap
    bar.set_tile(1, 19, Coord(2, 15))
    bar.set_tile(3, 19, Coord(4, 15))
    bar.set_tile(1, 20, Coord(2, 16))
    bar.set_tile(2, 20, Coord(3, 16))
    bar.set_tile(3, 20, Coord(4, 16))

    game.add_sprite(bar)