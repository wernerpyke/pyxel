from dataclasses import dataclass
import pyxel

import random

"""

    Note: another option for a matrix is
    
    import numpy as np
    rows, cols = 2, 3
    grid = np.empty((rows, cols), dtype=object)

"""

@dataclass
class Cell:
    x: int
    y: int
    colour: int = 0

class CellFied:
    def __init__(self, width: int = 0, height: int = 0):
        self._width = width
        self._height = height

        self._cells: list[ list[Cell] ] = []

        self.clear()

        # convenient flat list of all cells
        self._all_cells: list[Cell] = []
        for row in self._cells:
            for cell in row:
                self._all_cells.append(cell)

    def clear(self):
        self._cells = []
        for y in range(0, self._height):
            row: list[Cell] = []
            for x in range(0, self._width):
                row.append(Cell(x=x, y=y, colour=0))
            self._cells.append(row)

    def _update(self):
        for cell in self._all_cells:
            cell.colour = (cell.colour + 1) % 16 # random.randint(0, 15)

    def _draw(self):
        for cell in self._all_cells:
            pyxel.pset(cell.x, cell.y, cell.colour)

    def all_cells(self) -> list[Cell]:
        return self._all_cells

    def cell_at(self, x: int, y: int) -> Cell:
        return self._cells[y][x]
