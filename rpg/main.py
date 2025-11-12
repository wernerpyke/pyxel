from pathlib import Path
from pyke_pyxel.signals import Signals
from pyke_pyxel.rpg.game import RPGGame
from pyke_pyxel.settings import GameSettings, SizeSettings

import game_load
import game_loop
import config

# ==================================

Signals.connect(Signals.GAME.STARTED, game_loop.game_started)

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)
Signals.connect(Signals.PLAYER.INTERACT_OPENABLE, game_loop.player_interacts_with)
Signals.connect(Signals.PLAYER.ATTACK, game_loop.player_attacks)

Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked_by)

settings = GameSettings(
    debug=True,
    size=SizeSettings(window=160))

game = RPGGame(
        settings=settings,
        title="Pyke Dungeon RPG", 
        resources=f"{Path(__file__).parent.resolve()}/assets/sample.pyxres"
        )

game_load.build_room(game.room)

player = game.add_player(config.PLAYER.SPRITE)
game_load.set_player_position(player)

game.start()

