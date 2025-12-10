from pathlib import Path
from pyke_pyxel import GameSettings
from pyke_pyxel.signals import Signals
from pyke_pyxel.rpg.game import RPGGame

import game_load
import game_loop
import config

# ==================================

Signals.connect(Signals.GAME.WILL_START, game_loop.game_started)
Signals.connect(Signals.GAME.UPDATE, game_loop.game_update)

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)

Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked_by)

settings = GameSettings()
settings.debug = True

settings.fps.game = 30
settings.fps.animation = 8

settings.size.window = 160

game = RPGGame(
        settings=settings,
        title="Pyke Dungeon RPG", 
        resources=f"{Path(__file__).parent.resolve()}/assets/sample.pyxres"
        )

game_load.build_room(game.room)

player = game.set_player(config.PLAYER.SPRITE, 30)
game_load.set_player_position(player)

game.start()

