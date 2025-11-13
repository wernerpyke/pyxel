from pathlib import Path
from pyke_pyxel import COLOURS, GameSettings
from pyke_pyxel.signals import Signals
from pyke_pyxel.cell_auto.game import CellAutoGame

import game_loop
import ui

from td.profiler import ProfileGame

settings = GameSettings()

settings.size.window = 320
settings.size.tile = 8

settings.fps.game = 60

settings.colours.background = COLOURS.BLACK
settings.colours.sprite_transparency = COLOURS.BEIGE

settings.mouse_enabled = True
settings.display_smoothing_enabled = True

game = CellAutoGame(
        settings=settings,
        title="Pyke Tower", 
        resources=f"{Path(__file__).parent.resolve()}/assets/td_assets.pyxres"
        )

Signals.connect(Signals.GAME.WILL_START, game_loop.start)
Signals.connect(Signals.GAME.UPDATE, game_loop.update)
Signals.connect(Signals.MOUSE.MOVE, ui.mouse_move)
Signals.connect(Signals.MOUSE.DOWN, ui.mouse_down)
Signals.connect(Signals.MOUSE.UP, ui.mouse_up)

Signals.connect("enemy_dies", game_loop.enemy_killed)
Signals.connect("enemy_attacks", game_loop.enemy_attacks)
Signals.connect("enemy_spawns_enemy", game_loop.enemy_spawns_enemy)

Signals.connect("ui_title_screen_fade_out_complete", game_loop.ui_title_screen_fade_out_complete)
Signals.connect("ui_game_screen_fade_in_complete", game_loop.ui_game_screen_fade_in_complete)
Signals.connect("ui_game_start_selected", game_loop.ui_game_start_selected)
Signals.connect("ui_weapon_selected", game_loop.ui_weapon_selected)

game.start()