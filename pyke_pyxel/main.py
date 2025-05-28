from engine.signals import Signals
from engine.game import Game

import game_loop
import config

# ==================================

game = Game("Go Pyke!", "assets/sample.pyxres") #, game_events.Handler)

game_loop.build_room(game.room)

player = game.add_player(config.PLAYER.SPRITE(), config.PLAYER.MOVEMENT_SPEED())
game_loop.set_player(player)

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)
Signals.connect(Signals.PLAYER.INTERACT_OPENABLE, game_loop.player_interacts_with_openable)

game.start()