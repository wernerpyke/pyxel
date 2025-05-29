from engine.signals import Signals
from engine.game import Game

import game_loop
import config

# ==================================

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)
Signals.connect(Signals.PLAYER.INTERACT_OPENABLE, game_loop.player_interacts_with_openable)
Signals.connect(Signals.PLAYER.ATTACK, game_loop.player_attacks)

Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked_by)

game = Game("Go Pyke!", "assets/sample.pyxres")

game_loop.build_room(game.room)

player = game.add_player(config.PLAYER.SPRITE)
game_loop.set_player(player)

game_loop.game_started(game.room, player)

game.start()

