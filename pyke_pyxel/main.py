from engine.signals import Signals
from engine.game import Game
from engine.game_settings import GAME_SETTINGS, SIZE

import game_load
import game_loop
import config

# ==================================

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)
Signals.connect(Signals.PLAYER.INTERACT_OPENABLE, game_loop.player_interacts_with)
Signals.connect(Signals.PLAYER.ATTACK, game_loop.player_attacks)

Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked_by)

settings = GAME_SETTINGS(
    debug=True,
    size=SIZE(window=160))

game = Game(
        settings=settings,
        title="Go Pyke!", 
        spriteSheet="assets/sample.pyxres"
        )

game_load.build_room(game.room)

player = game.add_player(config.PLAYER.SPRITE)
game_load.set_player_position(player)

game_loop.game_started(game.room, player)

game.start()

