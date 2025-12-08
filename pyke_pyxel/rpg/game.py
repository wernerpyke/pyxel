from typing import Callable

from pyke_pyxel.rpg.actor import Actor
from pyke_pyxel.rpg.enemy import Enemy

from pyke_pyxel import log_debug, GameSettings
from pyke_pyxel.game import Game
from .player import Player
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import MovableSprite
from .room import Room

class RPGGame(Game):

    def __init__(self, settings: GameSettings, title: str, resources: str):
        """
        Specialised sub-class of `pyke_pyxel.Game` which adds basic room- and actor-based RPG mechanics.
        
        Attributes:
            player (Player): The player character. Use set_player() to assign the player instance.
            room (Room): The current room/map the player is in. Automatically initialized with the game map.

        Args:
            settings (GameSettings): The game settings configuration.
            title (str): The title of the game window.
            resources (str): The path to the resources directory.
        """
        super().__init__(settings, title, resources)

        self._player: Player
        self._room = Room(self._map)

        self._actors: list[Actor] = []
        Signals.connect("enemy_added", self._enemy_added)
        Signals.connect("enemy_removed", self._enemy_removed)

    def set_player(self, sprite: Callable[[], MovableSprite]) -> Player:
        _sprite = sprite()

        self._player = Player(_sprite)

        self._sprites.append(_sprite)

        self._player._id = self._actors.__len__()
        self._actors.append(self._player)

        return self._player
    
    def _update(self):

        # Keyboard
        self._keyboard._update(self)

        if self._paused:
            return

        Signals.send(Signals.GAME.UPDATE, self)

        for actor in self._actors:
            actor._update(self._map)

        self._update_animations()

    def clear_all(self):
        super().clear_all()
        self._actors.clear()
        self.player = None # type: ignore

    def _enemy_added(self, enemy: Enemy):
        enemy._id = self._actors.__len__()
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