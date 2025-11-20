import time
import random

from pyke_pyxel import Coord, log_error
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.signals import Signals
from td.enemies.enemy import Enemy
from td.enemies.bat import Bat
from td.enemies.mage import Mage
from td.enemies.orb import Orb
from td.enemies.skeleton import Skeleton

launch_locations = [
    Coord(2, 4), Coord(3, 2), Coord(4, 4), Coord(5, 6), Coord(7, 11), Coord(8, 8), Coord(9, 11), 
    Coord(10, 11), Coord(11, 11), Coord(12, 10), Coord(13, 10), Coord(14, 11), Coord(15, 11), Coord(16, 11), Coord(17, 10), Coord(18, 11), Coord(19, 12),
    Coord(20, 11), Coord(21, 11), Coord(22, 12), Coord(23, 13), Coord(24, 12), Coord(25, 9), Coord(26, 9),
    Coord(27, 10), Coord(28, 11), Coord(29, 11), Coord(30, 11), Coord(31, 11), Coord(32, 11),
    Coord(33, 7), Coord(34, 3), Coord(35, 6), Coord(36, 4), Coord(37, 2), Coord(38, 1)
]

class GameEnemies:
    def __init__(self) -> None:
        
        self._max_count = 3 # count
        self._available_enemies = ["skeleton", "orb", "mage"]

        self._launch_frequency = 2 # seconds
        self._previous_launch_time = 0

        self._enemies: list[Enemy] = []

    def launch_enemy_type(self, current_enemy_count: int) -> str|None:
        if current_enemy_count >= self._max_count:
            return None
        
        t = time.time()
        if (t - self._previous_launch_time) < self._launch_frequency:
            return None

        self._previous_launch_time = t
        return self._available_enemies[random.randint(0, len(self._available_enemies)-1)]

    def launch_bat(self, game: CellAutoGame, position: Coord):
        bat = Bat()
        bat.launch(game, position)
        self._enemies.append(bat)

    def update(self, game: CellAutoGame):
        def _remove_enemy_sprite(sprite_id: int):
            game.remove_sprite_by_id(sprite_id)
        
        field = game.matrix
        for e in self._enemies:
            cells = field.cells_at(e._sprite.position, include_empty=False)
            result = e.update(cells)
            match result:
                case 0: # continue
                    pass
                case -1: # killed
                    # log_debug(f"enemies.update() remove {e._sprite._id}")
                    self._enemies.remove(e)
                    e._sprite.activate_animation("die", loop=False, on_animation_end=_remove_enemy_sprite)
                    Signals.send("enemy_dies", game)
                case _: # win with potential multiplier
                    damage = e.damage * result
                    self._enemies.remove(e)
                    e._sprite.activate_animation("kill", loop=False, on_animation_end=_remove_enemy_sprite)
                    Signals.send_with("enemy_attacks", game, damage)

        type = self.launch_enemy_type(len(self._enemies))
        if type:
            match type:
                case "skeleton":
                    skeleton = Skeleton()
                    skeleton.launch(game, self._random_location())
                    self._enemies.append(skeleton)
                case "orb":
                    orb = Orb()
                    orb.launch(game, self._random_location())
                    self._enemies.append(orb)
                case "mage":
                    mage = Mage()
                    mage.launch(game, self._random_location())
                    self._enemies.append(mage)
                case _:
                    log_error(f"enemies.update invalid enemy type:{type}")

    def clear_all(self):
        self._enemies.clear()

    def _set_level(self, level: int):
        match level:
            case 0:
                self._launch_frequency = 2
                self._max_count = 2
                self._available_enemies = ["skeleton"]
            case 1:
                self._launch_frequency = 2
                self._max_count = 3
                self._available_enemies = ["skeleton", "skeleton", "orb"]
            case 2:
                self._launch_frequency = 1.8
                self._max_count = 4
                self._available_enemies = ["skeleton", "skeleton", "orb", "mage"]
            case 3:
                self._launch_frequency = 1.5
                self._max_count = 6
                self._available_enemies = ["skeleton", "skeleton", "skeleton", "orb", "orb", "mage", "mage"]
            case 4:
                self._launch_frequency = 1.2
                self._max_count = 8
                self._available_enemies = ["skeleton", "skeleton", "skeleton", "orb", "orb", "mage", "mage"]
            case _:
                self._launch_frequency = 1.2
                self._max_count = 10
                self._available_enemies = ["skeleton", "orb", "mage"]

    def _random_location(self) -> Coord:
        pos = launch_locations[random.randint(0, (len(launch_locations)-1))]
        return pos.clone()