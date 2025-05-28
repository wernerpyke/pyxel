from engine.signals import Signals
from engine.game import Game

import game_loop
import config

# ==================================

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)
Signals.connect(Signals.PLAYER.INTERACT_OPENABLE, game_loop.player_interacts_with_openable)
Signals.connect(Signals.PLAYER.ATTACK, game_loop.player_attacks)

game = Game("Go Pyke!", "assets/sample.pyxres") #, game_events.Handler)

game_loop.build_room(game.room)

player = game.add_player(config.PLAYER.SPRITE(), config.PLAYER.MOVEMENT_SPEED())
game_loop.set_player(player)

game_loop.game_started(player)

game.start()

