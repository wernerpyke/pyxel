from pyke_pyxel import coord
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import Anim, Sprite, CompoundSprite

from ui import UI

def load_level(game: CellAutoGame):
    game.set_tilemap(coord(1, 1), 8, 8)

    mountain = Sprite("mountain", coord(1, 21), 32, 12)
    mountain.set_position(coord(4, 1))
    game.add_sprite(mountain)

    _add_plants(game)

    _add_base(game)

    UI.load_hud(game)

def _add_plants(game: Game):
    s = CompoundSprite("plants", 40, 4)
    s.fill_row(1, tile_row=9, tile_cols=[1, 2, 3, 4])
    s.fill_row(2, tile_row=10, tile_cols=[1, 2, 3, 4])
    s.fill_row(3, tile_row=11, tile_cols=[1, 2, 3, 4])
    s.fill_row(4, tile_row=12, tile_cols=[1, 2, 3, 4])
    s.set_position(coord(1, 37))
    game.add_sprite(s)

def _add_base(game):
    base = Sprite("base", coord(1, 1), cols=8, rows=7)
    base.set_position(coord(16, 30))
    base.add_animation("loop", Anim(coord(1, 1), 4))
    base.activate_animation("loop")
    game.add_sprite(base)