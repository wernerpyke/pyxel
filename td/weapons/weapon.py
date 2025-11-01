from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell, CellField


class Weapon:
    def __init__(self, type: str, position: Coord, power: int, update_delay: int) -> None:
        self.position = position
        self.type = type

        self.cells: list[Cell] = []

        self.power = power

        self.should_skip_update_count = update_delay # this number reduces as speed increases
        self.skip_update_count = self.should_skip_update_count # to ensure that the first update draws

    def should_skip_update(self) -> bool:
        if self.skip_update_count < self.should_skip_update_count:
            self.skip_update_count += 1
            return True
        else:
            self.skip_update_count = 0
            return False

    def launch(self, field: CellField):
        print("Weapon.launch() implement in your class")
        pass

    def update(self, field: CellField) -> bool:
        print("Weapon.update() implement in your class")
        return False