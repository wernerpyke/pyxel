import time

from .ui import GameStateUI
from .map import GameMap
from .enemies import GameStateEnemies

class GameState:
    def __init__(self) -> None:
        self.map = GameMap()
        self.ui = GameStateUI()
        self.enemies = GameStateEnemies()
        # Sound
        self.music_enabled = False

        # Timer
        self._start_time: float = 0
        self._running_time: float = 0
        
        # Progression
        self.score = 0
        self.level = 1

    def start(self):
        self._start_time = time.time()
        self._running_time = 0
        
        self.level = 1
        self.enemies._set_level(self.level)

    def update(self):
        self._running_time = time.time() - self._start_time
        # Update enemy counts etc

STATE = GameState()