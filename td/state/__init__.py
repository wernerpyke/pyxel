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
        self._timestamp: float = 0
        self._running_time: float = 0
        
        # Progression
        self.score = 0
        self.level = 1

        self._max_health = 10

    def start(self):
        print("STATE.start()")
        self.score = 0
        self._max_health = 10

        self._timestamp = time.time()
        self._running_time = 0
        
        self.level = 1
        self.enemies._set_level(self.level)

    def pause(self):
        pass

    def unpause(self):
        self._timestamp = time.time()

    def update(self, game: CellAutoGame):
        now = time.time()
        self._running_time += now - self._timestamp
        self._timestamp = now
        # TODO: progress level based on running time etc

        self.enemies.update(game)
        self.weapons.update(game.matrix)

    @property
    def health_percentage(self) -> float:
        health = (self._max_health / 2) + self.score # where score can be negative
        return health / self._max_health
    
    @property
    def running_time_text(self) -> str:
        seconds = round(self._running_time)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

STATE = GameState()