import random

from pyke_pyxel import coord
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.sprite import Animation
from pyke_pyxel.math import RandomChoice
from .enemy import Enemy

class Tank(Enemy):

    def __init__(self) -> None:
        super().__init__("tank", coord(25,9), cols=2, rows=2)

        self.choice = RandomChoice()

        # TODO - move the below into a new base class: BigEnemy?
        self._sprite.add_animation("kill", Animation(coord(17,9), 2))
        self._sprite.add_animation("die", Animation(coord(21,9), 2))

        self._sprite.set_animation_fps(4)

    def launch(self, game: CellAutoGame, position: coord):
        super().launch(game, position)

        self._move_from_y = random.randint(60, 100)
        
        if game.map.x_is_left_of_center(self.position.x):
            self.choice.add((1,  0), 0.4)   # E
            self.choice.add((1,  1), 0.3)   # SE
            
            self.choice.add((-1, 0), 0.2)   # W
            self.choice.add((-1, 1), 0.1)   # SW
        else:
            self.choice.add((-1, 0), 0.4)   # W
            self.choice.add((-1, 1), 0.3)   # SW

            self.choice.add((1,  0), 0.2)   # E
            self.choice.add((1,  1), 0.1)   # SE

    def _move_towards_target(self) -> tuple[int, int]:
        if self.position.y < self._move_from_y:
            return (0, 1)

        return self.choice.select_one()