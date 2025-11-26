from pyke_pyxel import Coord, log_error
from pyke_pyxel.cell_auto.matrix import Cell, Matrix
from td.state.stats import STATS


class Weapon:
    def __init__(self, type: str, location_id: str, position: Coord) -> None:
        self.type = type
        self._location_id = location_id
        self.position = position

        stats = STATS.WEAPONS.get(type)
        if not stats:
            log_error(f"Weapon() invalid type {type}")
            return

        self.power = stats.power
        self._speed = stats.speed
        self._cooldown = stats.cooldown

        self._deactivate_upon_death = False

        self.cells: list[Cell] = []

    def launch(self, field: Matrix):
        print("Weapon.launch() implement in your class")

    def update(self, field: Matrix):
        print("Weapon.update() implement in your class")

    def kill(self):
        print("Weapon.kill() implement in your class")

    @property
    def is_alive(self) -> bool:
        return len(self.cells) > 0
    
    def __str__(self) -> str:
        return f"Weapon({self.type}{self._location_id})"
