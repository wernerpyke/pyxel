from typing import Callable, Optional

import pyxel

from . import DIRECTION
from .game_settings import GameSettings
from .game import Game
from .player import Player
from .signals import Signals
from .sprite import Sprite, MovableSprite
from .room import Room

class CharacterGame(Game):

    def __init__(self, settings: GameSettings, title: str, sprite_sheet: str):
        super().__init__(settings, title, sprite_sheet)

        self._player: Player
        self._room = Room(self._map)

    def add_player(self, sprite: Callable[[], MovableSprite]) -> Player:
        _sprite = sprite()

        self._player = Player(_sprite)

        self._sprites.append(_sprite)

        self._player._id = self._actors.__len__()
        self._actors.append(self._player)

        return self._player
    
    def update(self):
        # Keyboard
        if pyxel.btnp(pyxel.KEY_X):
            self._player.interact(self._map)
        elif pyxel.btnp(pyxel.KEY_Z):
            Signals.send(Signals.PLAYER.ATTACK, self._player)
        
        if self.movement_tick:
            if pyxel.btn(pyxel.KEY_UP):
                self._player.move(DIRECTION.UP, self._map)
            elif pyxel.btn(pyxel.KEY_DOWN):
                self._player.move(DIRECTION.DOWN, self._map)
            elif pyxel.btn(pyxel.KEY_LEFT):
                self._player.move(DIRECTION.LEFT, self._map)
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self._player.move(DIRECTION.RIGHT, self._map)
            else:
                self._player.stop_moving()

        super().update()

    @property
    def room(self) -> Room:
        return self._room