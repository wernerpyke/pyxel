from pathlib import Path
from pyke_pyxel import COLOURS
from pyke_pyxel.base_types import Coord
from pyke_pyxel.signals import Signals
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.game_settings import GameSettings, SizeSettings

from game_load import load_level
import game_loop
import ui

settings = GameSettings()

settings.size.window = 320
settings.size.tile = 8

settings.fps.game = 60

settings.colours.background = COLOURS.BLACK
settings.colours.sprite_transparency = COLOURS.BEIGE

settings.mouse_enabled = True

game = FieldGame(
        settings=settings,
        title="Pyke Tower", 
        resources=f"{Path(__file__).parent.resolve()}/assets/td_assets.pyxres"
        )

load_level(game)

Signals.connect(Signals.GAME.STARTED, game_loop.game_started)
Signals.connect(Signals.GAME.UPDATE, game_loop.game_update)
Signals.connect(Signals.MOUSE.MOVE, ui.mouse_move)
Signals.connect(Signals.MOUSE.DOWN, ui.mouse_down)
Signals.connect(Signals.MOUSE.UP, ui.mouse_up)

Signals.connect("enemy_dies", game_loop.enemy_killed)
Signals.connect("enemy_attacks", game_loop.enemy_wins)

Signals.connect("ui_weapon_selected", game_loop.ui_weapon_selected)

game.start()