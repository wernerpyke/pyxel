import time
import random

class GameEnemies:
    def __init__(self) -> None:
        
        self._max_count = 3 # count
        self._available_enemies = ["skeleton", "orb", "mage"]

        self._launch_frequency = 2 # seconds
        self._previous_launch_time = 0

    def launch_enemy_type(self, current_enemy_count: int) -> str|None:
        if current_enemy_count >= self._max_count:
            return None
        
        t = time.time()
        if (t - self._previous_launch_time) < self._launch_frequency:
            return None

        self._previous_launch_time = t
        return self._available_enemies[random.randint(0, len(self._available_enemies)-1)]

    def _set_level(self, level: int):
        match level:
            case 1:
                self._launch_frequency = 2
                self._max_count = 3
                self._available_enemies = ["skeleton"]
            case 2:
                self._launch_frequency = 2
                self._max_count = 3
                self._available_enemies = ["skeleton", "skeleton", "orb"]
            case 3:
                self._launch_frequency = 2
                self._max_count = 3
                self._available_enemies = ["skeleton", "skeleton", "orb", "mage"]