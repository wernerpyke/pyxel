import time
import random

from pyke_pyxel import coord, log_error
from pyke_pyxel._base_types import COLOURS
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.signals import Signals
from td.enemies.enemy import Enemy
from td.enemies.bat import Bat
from td.enemies.mage import Mage
from td.enemies.orb import Orb
from td.enemies.skeleton import Skeleton
from td.enemies.tank import Tank
from ._levels import EnemyLevel

launch_locations = [
    coord(2, 4), coord(3, 2), coord(4, 4), coord(5, 6), coord(7, 11), coord(8, 8), coord(9, 11), 
    coord(10, 11), coord(11, 11), coord(12, 10), coord(13, 10), coord(14, 11), coord(15, 11), coord(16, 11), coord(17, 10), coord(18, 11), coord(19, 12),
    coord(20, 11), coord(21, 11), coord(22, 12), coord(23, 13), coord(24, 12), coord(25, 9), coord(26, 9),
    coord(27, 10), coord(28, 11), coord(29, 11), coord(30, 11), coord(31, 11), coord(32, 11),
    coord(33, 7), coord(34, 3), coord(35, 6), coord(36, 4), coord(37, 2), coord(38, 1)
]

class GameEnemies:
    def __init__(self) -> None:
        self._enemies: list[Enemy] = []

        self._level = EnemyLevel()
        self._level.activate(0)
        self._previous_launch_time = 0

    def launch_enemy_type(self, current_enemy_count: int) -> str|None:
        level = self._level
        if current_enemy_count >= level.max_count:
            return None
        
        t = time.time()
        if (t - self._previous_launch_time) < level.frequency:
            return None

        self._previous_launch_time = t
        return level.random_type()

    def launch_bat(self, game: CellAutoGame, position: coord):
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
            outcome = result[0]
            was_hit = result[1]
            match outcome:
                case 0: # continue
                    pass
                case -1: # killed
                    # log_debug(f"enemies.update() remove {e._sprite._id}")
                    self._enemies.remove(e)
                    e._sprite.activate_animation("die", on_animation_end=_remove_enemy_sprite)
                    Signals.send_with("enemy_killed", game, e.bounty)
                case _: # win with potential multiplier
                    damage = e.damage * outcome
                    self._enemies.remove(e)
                    e._sprite.activate_animation("kill", on_animation_end=_remove_enemy_sprite)
                    Signals.send_with("enemy_attacks", game, damage)

            if was_hit:
                game.fx.splatter(COLOURS.RED, e._sprite.position)

        type = self.launch_enemy_type(len(self._enemies))
        if type:
            location = self._random_location()
            match type:
                case "skeleton":
                    enemy = Skeleton()
                    enemy.launch(game, location)
                    self._enemies.append(enemy)
                case "orb":
                    enemy = Orb()
                    enemy.launch(game, location)
                    self._enemies.append(enemy)
                case "mage":
                    enemy = Mage()
                    enemy.launch(game, location)
                    self._enemies.append(enemy)
                case "tank":
                    enemy = Tank()
                    enemy.launch(game, location)
                    self._enemies.append(enemy)
                case _:
                    log_error(f"enemies.update invalid enemy type:{type}")

    def closest_to(self, position: coord) -> Enemy|None:
        if len(self._enemies) == 0:
            return None

        closest = min(self._enemies, key=lambda enemy: enemy._sprite.position.distance_to(position))
        return closest

    def clear_all(self):
        self._enemies.clear()

    def set_level(self, id: int):
        self._level.activate(id)

    def _random_location(self) -> coord:
        pos = launch_locations[random.randint(0, (len(launch_locations)-1))]
        return pos.clone()