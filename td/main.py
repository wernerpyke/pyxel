from pathlib import Path
from pyke_pyxel.base_types import Coord
from pyke_pyxel.signals import Signals
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.game_settings import GameSettings, SizeSettings

import game_loop

settings = GameSettings()

settings.size.window = 320
settings.size.tile = 8

settings.fps.game = 30

game = FieldGame(
        settings=settings,
        title="Pyke Tower", 
        resources=f"{Path(__file__).parent.resolve()}/assets/td_assets.pyxres"
        )

game.add_tilemap(Coord(1, 1), 16, 16)

Signals.connect(Signals.GAME.STARTED, game_loop.game_started)
Signals.connect(Signals.CELL_FIELD.UPDATE, game_loop.game_state_update)

game.start()