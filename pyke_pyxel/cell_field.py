from typing import Optional
from dataclasses import dataclass
import pyxel

from . import GLOBAL_SETTINGS
from pyke_pyxel.signals import Signals

"""

    Note: another option for a matrix is
    
    import numpy as np
    rows, cols = 2, 3
    grid = np.empty((rows, cols), dtype=object)

"""

class Cell:

    def __init__(self, x: int, y: int) -> None:
        self.type: str = "empty"
        self.x: int = x
        self.y: int = y
        self.colour: int = 0
        self.can_propogate: bool = False
        self.ttl: int = 0 

    def reset(self):
        self.type = "empty"
        self.colour = 0
        self.can_propogate = False
        self.ttl = 0

class CellField:

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
                row.append(Cell(x, y))
            self._cells.append(row)

    # Lifecycle methods

    def _update(self):
        Signals.send(Signals.CELL_FIELD.UPDATE, self)

    def _draw(self):
        transparent = GLOBAL_SETTINGS.colours.sprite_transparency

        for cell in self._all_cells:
            if cell.colour != transparent:
                pyxel.pset(cell.x, cell.y, cell.colour)

    # Convenience accessors

    def neighbour_N(self, cell: Cell) -> Optional[Cell]:
        if cell.y > 0:
            return self._cells[cell.y - 1][cell.x]
        return None
    
    def neighbour_S(self, cell: Cell) -> Optional[Cell]:
        if cell.y < self._height - 1:
            return self._cells[cell.y + 1][cell.x]
        return None
    
    def neighbour_E(self, cell: Cell) -> Optional[Cell]:
        if cell.x < self._width - 1:
            return self._cells[cell.y][cell.x + 1]
        return None
    
    def neighbour_W(self, cell: Cell) -> Optional[Cell]:
        if cell.x > 0:
            return self._cells[cell.y][cell.x - 1]
        return None
    
    def neighbour_NE(self, cell: Cell) -> Optional[Cell]:
        if cell.x < self._width - 1 and cell.y > 0:
            return self._cells[cell.y - 1][cell.x + 1]
        return None
    
    def neighbour_NW(self, cell: Cell) -> Optional[Cell]:
        if cell.x > 0 and cell.y > 0:
            return self._cells[cell.y - 1][cell.x - 1]
        return None
    
    def neighbour_SE(self, cell: Cell) -> Optional[Cell]:
        if cell.x < self._width - 1 and cell.y < self._height - 1:
            return self._cells[cell.y + 1][cell.x + 1]
        return None
    
    def neighbour_SW(self, cell: Cell) -> Optional[Cell]:
        if cell.x > 0 and cell.y < self._height - 1:
            return self._cells[cell.y + 1][cell.x - 1]
        return None

    """
    def neighbours(self, cell: Cell) -> NeighbourCells:
      if cell._neighbours is None:
        TODO - load the neighbours
            
      return cell._neighbours

    
        neighbours: list[Cell] = []
        x = cell.x
        y = cell.y

        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if (nx == x and ny == y) or nx < 0 or ny < 0 or nx >= self._width or ny >= self._height:
                    continue
                neighbours.append(self._cells[ny][nx])

        return neighbours
    """

    def all_cells(self) -> list[Cell]:
        return self._all_cells

    def cell_at(self, x: int, y: int) -> Cell:
        return self._cells[y][x]
