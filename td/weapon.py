from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell, CellField


class Weapon:
    def __init__(self, type: str, position: Coord) -> None:
        self.position = position
        self.type = type

        self.cells: list[Cell] = []

    def launch(self, field: CellField):
        print("Weapon.launch() implement in your class")
        pass

    def update(self, field: CellField) -> bool:
        print("Weapon.update() implement in your class")
        return False