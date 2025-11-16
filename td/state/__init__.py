import time

from pyke_pyxel.cell_auto.game import CellAutoGame

from .weapons import GameWeapons
from .enemies import GameEnemies

class GameState:
    def __init__(self) -> None:
        self.weapons = GameWeapons()
        self.enemies = GameEnemies()
        # Sound
        self.music_enabled = False

        # Timer
        self._start_time: float = 0
        self._running_time: float = 0
        
        # Progression
        self.score = 0
        self.level = 1

        self._max_health = 10

    def start(self):
        print("STATE.start()")
        self.score = 0
        self._max_health = 10

        self._start_time = time.time()
        self._running_time = 0
        
        self.level = 1
        self.enemies._set_level(self.level)

    def update(self, game: CellAutoGame):
        self._running_time = time.time() - self._start_time
        # TODO: progress level based on running time etc

        self.enemies.update(game)
        self.weapons.update(game.matrix)

    @property
    def health_percentage(self) -> float:
        health = (self._max_health / 2) + self.score # where score can be negative
        return health / self._max_health

STATE = GameState()