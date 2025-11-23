from typing import Optional
import random

from pyke_pyxel import COLOURS, Coord, DIRECTION, log_error
from pyke_pyxel.cell_auto.matrix import Matrix, Cell

from .weapon import Weapon

class Star(Weapon):

    def __init__(self, location_id: str, position: Coord, to: Coord) -> None:
        super().__init__("star", location_id, position, power=10, speed=10, cooldown=0.5)

        self._from = position
        self._to = to

    def launch(self, field: Matrix):
        self.line = field.cells_in_line(self._from, self._to, extend_to_matrix_end=True)
        self.line_index = 0

    def update(self, field: Matrix):
        check_aliveness = len(self.cells) > 0 
        still_living = 0
        total_power = 0
        for c in self.cells:
            if not c.is_empty:
                still_living += 1
                total_power += c.power
            c.reset()

        if check_aliveness:
            if still_living < 4: # Half died, kill the star
                self.cells = []
                return
            else:
                self.power = total_power / 8 # Each star is made up of 8 cells

        if self.line_index < (len(self.line)-1):
            center = self.line[self.line_index]
            self._draw_star(center, field)
            self.line_index += 1
        else:
            self.cells = []
            # print(f"STAR REACHED END")

    def _draw_star(self, center: Cell, field: Matrix):
        self.cells = []

        x, y = center.x, center.y
        if center.x % 2 == 0:
            # N
            self._add_star_cell(field.cell_at(x, (y-1)))
            self._add_star_cell(field.cell_at(x, (y-2)))
            # S
            self._add_star_cell(field.cell_at(x, (y+1)))
            self._add_star_cell(field.cell_at(x, (y+2)))
            # E
            self._add_star_cell(field.cell_at((x+1), y))
            self._add_star_cell(field.cell_at((x+2), y))
            # W
            self._add_star_cell(field.cell_at((x-1), y))
            self._add_star_cell(field.cell_at((x-2), y))
        else:
            # NE
            self._add_star_cell(field.cell_at(x+1, (y-1)))
            self._add_star_cell(field.cell_at(x+2, (y-2)))
            # NW
            self._add_star_cell(field.cell_at(x-1, (y-1)))
            self._add_star_cell(field.cell_at(x-2, (y-2)))
            # SE
            self._add_star_cell(field.cell_at(x+1, (y+1)))
            self._add_star_cell(field.cell_at(x+2, (y+2)))
            # SW
            self._add_star_cell(field.cell_at(x-1, (y+1)))
            self._add_star_cell(field.cell_at(x-2, (y+2)))

    def _add_star_cell(self, c:  Cell|None):
        if c:
            c.type = self.type
            c.colour = COLOURS.YELLOW
            c.power = self.power
            self.cells.append(c)