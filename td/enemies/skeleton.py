import random

from pyke_pyxel import GameSettings
from pyke_pyxel import Coord
from .enemy import Enemy

class Skeleton(Enemy):

    def __init__(self) -> None:
        super().__init__("skeleton", Coord(9,8), 
                         power=random.randint(500, 800), 
                         speed=2)

        self._move_from_y = random.randint(80, 180)

        self.max_x = self.max_y = GameSettings.get().size.window
        self.mid_x = self.max_x / 2

    def _move_towards_target(self) -> tuple[int, int]:
        position = self._sprite.position
        x_dist = self.mid_x - position.x
        y_dist = self.max_y - position.y

        if (x_dist == 0) or (y_dist > self._move_from_y):
            return (0, 1)
        
        factor = abs(y_dist / x_dist)
        if factor > 2.5:
            return (0, 1) # keep going down
        
        threshold = 0.8
        if factor < 1:
            threshold = 0.5
        elif factor < 2:
            threshold = 0.2

        if random.random() > threshold:
            if self._sprite.position.x < self.mid_x:
                return (1, 1)
            else:
                return (-1, 1)
        else:
            return (0, 1)