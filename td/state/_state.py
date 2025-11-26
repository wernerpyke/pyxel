import time

from pyke_pyxel.cell_auto.game import CellAutoGame

from .stats import STATS
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
        self.level = 0
        self.score_counter: float = 0
        self._max_health = STATS.PLAYER_HEALTH

    def start(self):
        self.level = 0
        self.score_counter = 0
        self._max_health = STATS.PLAYER_HEALTH

        self._timestamp = time.time()
        self._running_time = 0
        
        self.enemies.set_level(self.level)

        self.weapons.clear_all()
        self.enemies.clear_all()

    def pause(self):
        pass

    def unpause(self):
        self._timestamp = time.time()

    def update(self, game: CellAutoGame):
        now = time.time()
        self._running_time += now - self._timestamp
        self._timestamp = now

        # Progress level based on running time etc
        minutes = self.running_time_minutes
        if self.level < minutes:
            self.level = minutes
            print(f"STATE.update() PROGRESS level:{self.level}")
            self.enemies.set_level(self.level)

        self.enemies.update(game)
        self.weapons.update(game.matrix, self.enemies)

    def acquire_weapon(self, type: str) -> bool:
        cost = STATS.WEAPONS[type].cost
        # if cost > self.score_counter:
        #    return False
        self.score_counter -= cost
        print(f"STATE.acquire_weapon() cost:{cost} score:{self.score_counter}")
        return True

    @property
    def health_percentage(self) -> float:
        health = (self._max_health / 2) + self.score_counter # where self.score can be negative
        return health / self._max_health
    
    @property
    def running_time_minutes(self) -> int:
        seconds = round(self._running_time)
        return seconds // 60

    @property
    def running_time_text(self) -> str:
        seconds = round(self._running_time)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    # TODO the below causes a circular import in Enemy() and Weapon()
    # def enemy_stats(self, type: str) -> EnemyStats|None:
    #    return _STATS.ENEMIES.get(type)
    
    # def weapon_stats(self, type: str) -> WeaponStats|None:
    #    return _STATS.WEAPONS.get(type) # TODO apply POWER UP effects here