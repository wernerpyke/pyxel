from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.sprite import Sprite, CompoundSprite

def vertical_bar(game: FieldGame, position: Coord):
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

def load_level(game: FieldGame):
    game.add_tilemap(Coord(1, 1), 8, 8)

    mountain = Sprite("mountain", Coord(1, 17), 32, 12)
    mountain.set_position(Coord(4, 1))
    game.add_sprite(mountain)

    # vertical_bar(game, Coord(10, 8))

    # vertical_bar(game, Coord(26, 8))

    base = Sprite("base", Coord(1, 1), col_tile_count=8, row_tile_count=8)
    base.set_position(Coord(16, 33))
    game.add_sprite(base)