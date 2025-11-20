import math
import random

from pyke_pyxel import Coord
from pyke_pyxel.cell_auto.matrix import Cell
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.signals import Signals
from .enemy import Enemy

class Mage(Enemy):

    def __init__(self) -> None:
        super().__init__("mage", Coord(19,8), 
                         animation_frame_count=2,
                         power=1000, 
                         speed=3,\
                         damage=2)
        
        self._to_x = 0
        self._to_y = 0

        self._launch_projectile = False

    def launch(self, game: CellAutoGame, position: Coord):
        self._map = game.map
        self._to_x = position.x #Down
        self._to_y = position.y + self._map.random_distance_down(position.y, 20, 40)
        # print(f"Mage DOWN to x:{self._to_x} y:{self._to_y}")
        return super().launch(game, position)
    
    def update(self, field_cells: list[Cell]) -> int:
        result = super().update(field_cells)
        if self._launch_projectile:
            launch_at = self._sprite.position.clone()
            launch_at.move_by(0, 8)
            Signals.send_with("enemy_spawns_enemy", "bat", (launch_at.x, launch_at.y))

            self._launch_projectile = False
        return result

    def _move_towards_target(self) -> tuple[int, int]:
        at_x = self._sprite.position.x
        at_y = self._sprite.position.y

        by_x = 0
        by_y = 0

        if at_x == self._to_x and at_y == self._to_y: # Arrived
            # Select new random location
            move_right = True
            distance = random.randint(30, 50)
            if self._map.x_is_left_of_center(at_x):
                move_right = random.random() > 0.3
            else:
                move_right = random.random() <= 0.3


            if move_right:
                self._sprite.is_flipped = False
                angle = random.randint(0, 90)
            else:
                self._sprite.is_flipped = True
                angle = random.randint(90, 180)

            self._to_x += round(distance * math.cos(math.radians(angle)))
            self._to_y += round(distance * math.sin(math.radians(angle)))
            self._to_x = self._map.bound_to_width(self._to_x)
            self._to_y = self._map.bound_to_height(self._to_y)

            # print(f"Mage {"RIGHT" if move_right else "LEFT"} {distance} @ {angle} from x{at_x} y:{at_y} to x:{self._to_x} y:{self._to_y}")

            self._launch_projectile = True # launch projectile
            
        
        if at_x < self._to_x:
            by_x = 1
        elif at_x > self._to_x:
            by_x = -1
        # else by_x = 0
        
        if at_y < self._to_y:
            by_y = 1
        elif at_y > self._to_y:
            by_y = -1
        # else by_y = 0

        return (by_x, by_y)