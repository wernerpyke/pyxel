from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell, CellField


class Weapon:
    def __init__(self, type: str, position: Coord) -> None:
        self.position = position
        self.type = type

        self.cells: list[Cell] = []

        self.skip_updates = 2 # this number reduces as speed increases
        self.skip_counter = self.skip_updates # to ensure that the first update draws

    def should_skip_update(self) -> bool:
        if self.skip_counter < self.skip_updates:
            self.skip_counter += 1
            return True
        else:
            self.skip_counter = 0
            return False

    def launch(self, field: CellField):
        print("Weapon.launch() implement in your class")
        pass

    def update(self, field: CellField) -> bool:
        print("Weapon.update() implement in your class")
        return False