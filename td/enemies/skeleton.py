import random

from pyke_pyxel import GameSettings
from pyke_pyxel import coord
from pyke_pyxel.cell_auto.game import CellAutoGame
from .enemy import Enemy

class Skeleton(Enemy):

    def __init__(self) -> None:
        super().__init__("skeleton", coord(9,8))

    def launch(self, game: CellAutoGame, position: coord):
        self._move_from_y = random.randint(80, 180)

        self.max_x = game.map.right_x
        self.max_y = game.map.bottom_y
        self.mid_x = game.map.center_x
        return super().launch(game, position)

    def _move_towards_target(self) -> tuple[int, int]:
        position = self.position
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
            if self.position.x < self.mid_x:
                return (1, 1)
            else:
                return (-1, 1)
        else:
            return (0, 1)