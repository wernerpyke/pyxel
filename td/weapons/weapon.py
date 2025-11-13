from pyke_pyxel import Coord, log_error
from pyke_pyxel.cell_auto.matrix import Cell, Matrix


class Weapon:
    def __init__(self, type: str, position: Coord, power: float, speed: int) -> None:
        self.position = position
        self.type = type

        self.cells: list[Cell] = []

        self.power = power

        if speed > 10:
            log_error(f"Weapon({type}) speed > 10")
            speed = 10
        self._speed = speed

        #self._updates_attempted_count = 0
        #self._updates_skipped_count = 0

    def launch(self, field: Matrix):
        print("Weapon.launch() implement in your class")

    def update(self, field: Matrix):
        print("Weapon.update() implement in your class")

    def kill(self):
        print("Weapon.kill() implement in your class")
    
    # def _track_cell(self, cell: Cell):
    #    if not cell.is_border:
    #        self._cells.append(cell)

    @property
    def is_alive(self) -> bool:
        return len(self.cells) > 0