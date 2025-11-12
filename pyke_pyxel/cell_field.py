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

    def __init__(self, x: int, y: int, img: pyxel.Image) -> None:
        self.x: int = x
        self.y: int = y
        self._neighbours: list[Cell] = []

        self._img = img

        # state
        self.type: str = "empty"
        self._colour: int = 0
        self.can_propogate: bool = False
        self.power: float = 0
        self.tag: Any = None

        self.stored_type: str = "empty"
        self.stored_colour: int = 0
        self.stored_can_propogate: bool = False
        self.stored_power: float = 0
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
        self.stored_colour = self._colour
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
    def colour(self) -> int:
        return self._colour
    
    @colour.setter
    def colour(self, value: int):
        self._colour = value
        self._img.pset(self.x, self.y, value)
    
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

        self._img: pyxel.Image = pyxel.Image(width, height) # Use a pyxel.Image to optimise _draw()
        self.clear()

    def clear(self):
        self._cells = []
        for y in range(0, self._height):
            row: list[Cell] = []
            for x in range(0, self._width):
                row.append(Cell(x, y, self._img))
            self._cells.append(row)

    # Lifecycle methods

    def _draw(self):
        pyxel.blt(0, 0, self._img, 0, 0, self._width, self._height, colkey=0)

        """
        Unoptimised: it consumes 19% of game.draw()
        transparent = GLOBAL_SETTINGS.colours.sprite_transparency
        for cell in self._all_cells:
            if cell.colour != transparent:
                pyxel.pset(cell.x, cell.y, cell.colour)
        """

    # Convenience accessors

    def neighbour_N(self, cell: Cell) -> Cell|None:
        if cell.y > 0:
            return self._cells[cell.y - 1][cell.x]
        return None
    
    def neighbour_S(self, cell: Cell) -> Cell|None:
        if cell.y < self._height - 1:
            return self._cells[cell.y + 1][cell.x]
        return None
    
    def neighbour_E(self, cell: Cell) -> Cell|None:
        if cell.x < self._width - 1:
            return self._cells[cell.y][cell.x + 1]
        return None
    
    def neighbour_W(self, cell: Cell) -> Cell|None:
        if cell.x > 0:
            return self._cells[cell.y][cell.x - 1]
        return None
    
    def neighbour_NE(self, cell: Cell) -> Cell|None:
        if cell.x < self._width - 1 and cell.y > 0:
            return self._cells[cell.y - 1][cell.x + 1]
        return None
    
    def neighbour_NW(self, cell: Cell) -> Cell|None:
        if cell.x > 0 and cell.y > 0:
            return self._cells[cell.y - 1][cell.x - 1]
        return None
    
    def neighbour_SE(self, cell: Cell) -> Cell|None:
        if cell.x < self._width - 1 and cell.y < self._height - 1:
            return self._cells[cell.y + 1][cell.x + 1]
        return None
    
    def neighbour_SW(self, cell: Cell) -> Cell|None:
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

    def cell_at(self, x: int, y: int) -> Cell|None:
        if y < 0 or y >= len(self._cells):
            return None
        if x < 0 or x >= len(self._cells[0]):
            return None
        return self._cells[y][x]
    
    def cells_at(self, position: Coord, include_empty: bool = False) -> list[Cell]:
        cells: list[Cell] = []

        min_y = position.min_y if position.min_y > 0 else 0
        min_x = position.min_x if position.min_x > 0 else 0
        max_y = position.max_y if position.max_y < self._height else self._height
        max_x = position.max_x if position.max_x < self._width else self._width

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                cells.append(self._cells[y][x])

        if not include_empty:
            cells = [
                c for c in cells if not c.is_empty
            ]
        return cells

    def cells_in_line(self, from_position: Coord, to_position: Coord) -> list[Cell]:
        cells: list[Cell] = []

        from_x = from_position.x
        from_y = from_position.y
        to_x = to_position.x
        to_y = to_position.y

        # Create a line on the grid between (from_x, from_y) and (to_x, to_y) using Bresenham's algorithm.
        # This implementation handles all octants.
        
        # Ensure coordinates are within bounds for the simple example
        # In a real application, you'd add robust clipping/boundary checks.
        distance_x = abs(to_x - from_x)
        distance_y = abs(to_y - from_y)
        
        # Determine direction of step
        step_x = 1 if from_x < to_x else -1
        step_y = 1 if from_y < to_y else -1

        # Initial decision parameter (simplified for this general case)
        err = distance_x - distance_y
        
        current_x, current_y = from_x, from_y

        # Main loop iterates until the end point is reached
        # The loop condition ensures the drawing stops at (x1, y1)
        while True:
            # Draw the pixel at the current coordinates (y is row, x is column)
            # Note: In a list-of-lists matrix, the first index is the row (y-coordinate)
            # and the second index is the column (x-coordinate).
            if 0 <= current_y < len(self._cells) and 0 <= current_x < len(self._cells[0]):
                # print(f"Draw x:{current_x} y:{current_y}")
                cells.append(self._cells[current_y][current_x])

            # Exit condition: if we've reached the end point
            if current_x == to_x and current_y == to_y:
                break

            # Calculate the next step
            e2 = 2 * err
            
            if e2 > -distance_y:  # Move in x-direction
                err -= distance_y
                current_x += step_x
            
            if e2 < distance_x:  # Move in y-direction
                err += distance_x
                current_y += step_y

        return cells