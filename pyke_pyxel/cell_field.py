from typing import Any, Optional
import pyxel

from pyke_pyxel.base_types import Coord

from . import GLOBAL_SETTINGS
from pyke_pyxel.signals import Signals

"""
    Note: another option for a matrix is
    
    import numpy as np
    rows, cols = 2, 3
    grid = np.empty((rows, cols), dtype=object)
"""

class Cell:
    TYPE_EMPTY = "empty"

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self._neighbours: list[Cell] = []

        # state
        self.type: str = "empty"
        self.colour: int = 0
        self.can_propogate: bool = False
        self.power: int = 0
        self.tag: Any = None

        self.stored_type: str = "empty"
        self.stored_colour: int = 0
        self.stored_can_propogate: bool = False
        self.stored_power: int = 0
        self.stored_tag: Any = None

    def reset(self):
        self.type = "empty"
        self.colour = 0
        self.can_propogate = False
        self.power = 0
        self.tag = None

        self.store_state()

    def store_state(self):
        self.stored_type = self.type
        self.stored_colour = self.colour
        self.stored_can_propogate = self.can_propogate
        self.stored_power = self.power
        self.stored_tag = self.tag
    
    def recall_state(self):
        self.type = self.stored_type
        self.colour = self.stored_colour
        self.can_propogate = self.stored_can_propogate
        self.power = self.stored_power
        self.tag = self.stored_tag

        self.stored_type = "empty"
        self.stored_colour = 0
        self.stored_can_propogate = False
        self.stored_power = 0
        self.stored_tag = None
    
    @property
    def is_empty(self):
        return self.type == "empty"
    
    def __str__(self):
        return f"{self.x}/{self.y}"

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

    def neighbours(self, cell: Cell, filter_for_type: Optional[str] = None) -> list[Cell]:
        if len(cell._neighbours) == 0:
            x = cell.x
            y = cell.y

            max_x = self._width - 1
            max_y = self._height - 1

            neighbours = cell._neighbours

            if y > 0: # N
                n = self._cells[y - 1][x]
                neighbours.append(n)
                if x > 0: # NW
                    n = self._cells[y - 1][x-1]
                    neighbours.append(n)
                if x < max_x: # NE
                    n = self._cells[y - 1][x+1]
                    neighbours.append(n)
            
            if y < max_y: # S
                n = self._cells[y + 1][x]
                neighbours.append(n)
                if x > 0: # SW
                    n = self._cells[y + 1][x-1]
                    neighbours.append(n)
                if x < max_x: # SE
                    n = self._cells[y + 1][x+1]
                    neighbours.append(n)

            if x < max_x: # E
                n = self._cells[y][x+1]
                neighbours.append(n)
            
            if x > 0: # W
                n = self._cells[y][x-1]
                neighbours.append(n)
        
        if filter_for_type == None:
             return cell._neighbours.copy() # copy is to allow modification of the cached neighbours
        else:
            return [
                n for n in cell._neighbours if n.type == filter_for_type
            ]

            # neighbours: list[Cell] = []
            # for n in cell._neighbours:
            #    if n.type == filter_for_type:
            #        neighbours.append(n)
            # return neighbours    

    def all_cells(self) -> list[Cell]:
        return self._all_cells

    def cell_at(self, x: int, y: int) -> Cell:
        return self._cells[y][x]
    
    def cells_at(self, position: Coord, include_empty: bool = False) -> list[Cell]:
        cells: list[Cell] = []

        min_y = position.min_y if position.min_y > 0 else 0
        min_x = position.min_x if position.min_x > 0 else 0
        max_y = position.max_y if position.max_y < self._height else self._height
        max_x = position.max_x if position.max_x < self._width else self._width

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if y >= len(self._cells):
                    print("YUCK!")

                cells.append(self._cells[y][x])

        if not include_empty:
            cells = [
                c for c in cells if not c.is_empty
            ]
        return cells