from typing import Callable, Optional

import pyxel

from pyke_pyxel.actor import Actor
from pyke_pyxel.enemy import Enemy

from . import DIRECTION, log_debug
from .game_settings import GameSettings
from .game import Game
from .player import Player
from .signals import Signals
from .sprite import Sprite, MovableSprite
from .room import Room

class RPGGame(Game):

    def __init__(self, settings: GameSettings, title: str, resources: str):
        super().__init__(settings, title, resources)

        self._player: Player
        self._room = Room(self._map)

        self.movement_tick: bool = False
        self._actors: list[Actor] = []
        Signals.connect("enemy_added", self._enemy_added)
        Signals.connect("enemy_removed", self._enemy_removed)

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
        
        # movement
        self.movement_tick = not self.movement_tick

        for actor in self._actors:
            actor._update(self._map, self.movement_tick)

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

    def _enemy_added(self, enemy: Enemy):
        self._actors.append(enemy)

    def _enemy_removed(self, enemy: Enemy):
        if enemy in self._actors:
            self._actors.remove(enemy)
            log_debug(f"GAME._enemy_removed() {enemy._id}")

    @property
    def player(self) -> Player:
        return self._player

    @property
    def room(self) -> Room:
        return self._room