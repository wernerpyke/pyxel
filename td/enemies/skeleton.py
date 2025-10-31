import random

from pyke_pyxel.base_types import Coord
from .enemy import Enemy


class Skeleton(Enemy):

    def __init__(self) -> None:
        super().__init__("skeleton", Coord(9,9), random.randint(200, 400))
