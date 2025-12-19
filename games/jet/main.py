from pathlib import Path
from pyke_pyxel import GameSettings, COLOURS
from pyke_pyxel.signals import Signals
from pyke_pyxel.rpg.game import RPGGame

import game_loop

settings = GameSettings()

settings.fps.game = 60
settings.fps.animation = 16

settings.size.window = 320

settings.colours.background = COLOURS.BLACK
settings.colours.sprite_transparency = COLOURS.BEIGE

settings.pathfinding.allow_diagonal = True
settings.pathfinding.reduce_hugging = True

settings.debug = False

game = RPGGame(
        settings=settings,
        title="Jet", 
        resources=f"{Path(__file__).parent.resolve()}/assets/assets.pyxres"
        )

Signals.connect(Signals.GAME.WILL_START, game_loop.game_started)
Signals.connect(Signals.GAME.UPDATE, game_loop.game_update)

Signals.connect(Signals.PLAYER.MOVED, game_loop.player_moved)
Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked)

Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked)
Signals.connect(Signals.ENEMY.STOPPED, game_loop.enemy_stopped)

game.start()