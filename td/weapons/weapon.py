from pyke_pyxel import coord, log_error, log_debug
from pyke_pyxel.cell_auto.matrix import Cell, Matrix
from td.state.stats import STATS


class Weapon:
    def __init__(self, type: str, location_id: str, position: coord) -> None:
        self.type = type
        self._location_id = location_id
        self.position = position

        stats = STATS.weapon_stats(type)
        if not stats:
            log_error(f"Weapon() invalid type {type}")
            return

        self.power = stats.power
        self._speed = stats.speed
        self._cooldown = stats.cooldown

        # log_debug(f"Weapon({self.type}) power:{self.power} speed:{self._speed} cooldown:{self._cooldown}")

        self._deactivate_upon_death = False

        self.cells: list[Cell] = []

    def launch(self, field: Matrix):
        raise NotImplementedError("Weapon.launch() implement in your class")

    def update(self, field: Matrix):
        raise NotImplementedError("Weapon.update() implement in your class")

    def kill(self):
        raise NotImplementedError("Weapon.kill() implement in your class")

    @property
    def is_alive(self) -> bool:
        return len(self.cells) > 0
    
    def __str__(self) -> str:
        return f"Weapon({self.type}{self._location_id})"
