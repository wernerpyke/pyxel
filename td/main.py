from pathlib import Path
from pyke_pyxel import COLOURS
from pyke_pyxel.base_types import Coord
from pyke_pyxel.signals import Signals
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.game_settings import GameSettings, SizeSettings

import game_loop
from td.state import STATE
import ui

settings = GameSettings()

settings.size.window = 320
settings.size.tile = 8
# Override GameSettings.size.window
STATE.map.width = 320
STATE.map.height = 320

settings.fps.game = 60

settings.colours.background = COLOURS.BLACK
settings.colours.sprite_transparency = COLOURS.BEIGE

settings.mouse_enabled = True



game = FieldGame(
        settings=settings,
        title="Pyke Tower", 
        resources=f"{Path(__file__).parent.resolve()}/assets/td_assets.pyxres"
        )

Signals.connect(Signals.GAME.STARTED, game_loop.game_started)
Signals.connect(Signals.GAME.UPDATE, game_loop.game_update)
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