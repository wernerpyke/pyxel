from pathlib import Path
from pyke_pyxel.signals import Signals
from pyke_pyxel.character_game import CharacterGame
from pyke_pyxel.game_settings import GameSettings, SizeSettings

import game_load
import game_loop
import config

# ==================================

Signals.connect(Signals.PLAYER.BLOCKED, game_loop.player_blocked_by)
Signals.connect(Signals.PLAYER.INTERACT_OPENABLE, game_loop.player_interacts_with)
Signals.connect(Signals.PLAYER.ATTACK, game_loop.player_attacks)

Signals.connect(Signals.ENEMY.BLOCKED, game_loop.enemy_blocked_by)

settings = GameSettings(
    debug=True,
    size=SizeSettings(window=160))

game = CharacterGame(
        settings=settings,
        title="Pyke Dungeon RPG", 
        sprite_sheet=f"{Path(__file__).parent.resolve()}/assets/sample.pyxres"
        )

game_load.build_room(game.room)

player = game.add_player(config.PLAYER.SPRITE)
game_load.set_player_position(player)

game_loop.game_started(game.room, player)

game.start()

