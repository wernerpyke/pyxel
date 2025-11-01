import random

from pyke_pyxel import log_error
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell, CellField


class Weapon:
    def __init__(self, type: str, position: Coord, power: int, speed: int) -> None:
        self.position = position
        self.type = type

        self.cells: list[Cell] = []

        self.power = power

        if speed > 10:
            log_error(f"Weapon({type}) speed > 10")
            speed = 10

        self.skip_frequency = (10 - speed) / 10

    def should_skip_update(self) -> bool:
        #
        # TODO: there may be something weird here
        # testing it with fungus @ speed=2, skip_frequency=0.8 yields a skip rate of 67%?
        #
        return random.random() < self.skip_frequency

    def launch(self, field: CellField):
        print("Weapon.launch() implement in your class")
        pass

    def update(self, field: CellField) -> bool:
        print("Weapon.update() implement in your class")
        return False