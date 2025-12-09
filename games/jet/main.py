from pathlib import Path
from pyke_pyxel import GameSettings, COLOURS
from pyke_pyxel.signals import Signals
from pyke_pyxel.rpg.game import RPGGame

import game_loop
import sprites

settings = GameSettings()

settings.fps.game = 60
settings.fps.animation = 16

settings.size.window = 160

settings.colours.background = COLOURS.BLACK
settings.colours.sprite_transparency = COLOURS.BEIGE

game = RPGGame(
        settings=settings,
        title="Jet", 
        resources=f"{Path(__file__).parent.resolve()}/assets/assets.pyxres"
        )

Signals.connect(Signals.GAME.WILL_START, game_loop.game_started)
Signals.connect(Signals.GAME.UPDATE, game_loop.game_update)

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked)

game.set_player(sprites.player())
game.start()