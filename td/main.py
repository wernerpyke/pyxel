from pathlib import Path
from pyke_pyxel.signals import Signals
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.game_settings import GameSettings, SizeSettings

settings = GameSettings()

settings.size.window = 320
settings.size.tile = 8

game = FieldGame(
        settings=settings,
        title="Pyke Tower", 
        sprite_sheet=f"{Path(__file__).parent.resolve()}/assets/td_assets.pyxres"
        )

game.start()