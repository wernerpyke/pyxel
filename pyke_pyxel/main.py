from engine.signals import Signals
from engine.game import Game

import game_events


# ==================================

game = Game("Go Pyke!", "assets/sample.pyxres") #, game_events.Handler)

game_events.create_room(game)
game_events.create_player(game)

Signals.register(Signals.PLAYER.BLOCKED, game_events.player_blocked)

game.start()