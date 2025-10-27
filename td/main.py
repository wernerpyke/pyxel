from pathlib import Path
from pyke_pyxel.signals import Signals
from pyke_pyxel.game import Game
from pyke_pyxel.game_settings import GAME_SETTINGS, SIZE

settings = GAME_SETTINGS()

settings.size.window = 320
settings.size.tile = 8

game = Game(
        settings=settings,
        title="Pyke Tower", 
        sprite_sheet=f"{Path(__file__).parent.resolve()}/assets/td_assets.pyxres"
        )

game.start()