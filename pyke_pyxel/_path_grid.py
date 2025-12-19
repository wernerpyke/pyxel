from dataclasses import dataclass

from ._types import coord, GameSettings
from ._log import log_debug

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

@dataclass
class PATH_STATUS:
    AVOID = 3
    AVAILABLE = 2
    PREFERRED = 1
    BLOCKED = 0

class _PathGrid:
    def __init__(self, cols: int, rows: int):
        self._grid: list[list[int]] = []

        settings = GameSettings.get()
        self._allow_diagonal = settings.pathfinding.allow_diagonal
        self._reduce_hugging = settings.pathfinding.reduce_hugging

        for _ in range(0, cols):
            path_row: list[int] = []
            for _ in range(0, rows):
                path_row.append(PATH_STATUS.AVAILABLE)
        
            self._grid.append(path_row)

    def block(self, position: coord):
        # import pathfinding is whack? x/y are switched around
        c_index = position._col - 1
        r_index = position._row - 1
        self._grid[r_index][c_index] = PATH_STATUS.BLOCKED

        if self._reduce_hugging:
            neighbours = self._neighbours(c_index, r_index)
            for n in neighbours:
                c_index = n[0]
                r_index = n[1]
                value = self._grid[r_index][c_index]
                if value == PATH_STATUS.AVAILABLE:
                    self._grid[r_index][c_index] = PATH_STATUS.AVOID

    def open(self, position: coord):
        # import pathfinding is whack? x/y are switched around
        c_index = position._col - 1
        r_index = position._row - 1
        was_blocked = self._grid[r_index][c_index] == PATH_STATUS.BLOCKED

        self._grid[r_index][c_index] = PATH_STATUS.AVAILABLE

        if self._reduce_hugging:
            if was_blocked:
                # If this location was previously blocked then it means
                # that its neighbours would have been AVOID
                # and therefore, we should set this location from BLOCKED -> AVOID
                self._grid[r_index][c_index] = PATH_STATUS.AVOID

            neighbours = self._neighbours(c_index, r_index)
            for n in neighbours:
                n_c = n[0]
                n_r = n[1]
                value = self._grid[n_r][n_r]
                if value == PATH_STATUS.AVOID:
                    self._grid[n_r][n_c] = PATH_STATUS.AVAILABLE


    def _neighbours(self, c_index: int, r_index: int) -> list[tuple[int, int]]:
        result = []

        if c_index > 0: # Left
            result.append((c_index - 1, r_index))
        if c_index < len(self._grid) - 1: # Right
            result.append((c_index + 1, r_index))

        if r_index > 0: # Up
            result.append((c_index, r_index - 1))
        if r_index < len(self._grid[0]) - 1: # Down
            result.append((c_index, r_index + 1))
        return result

    def find_path(self, frm: coord, to: coord, allow_diagonal: bool|None = None) -> list[coord]|None:
        if allow_diagonal is None:
            allow_diagonal = self._allow_diagonal
        
        grid = Grid(matrix=self._grid)
        
        start = grid.node(frm._col - 1, frm._row - 1)
        end = grid.node(to._col - 1, to._row - 1)

        diagonal = DiagonalMovement.always if allow_diagonal else DiagonalMovement.never

        finder = AStarFinder(diagonal_movement=diagonal)
        path, _ = finder.find_path(start, end, grid)

        if path and len(path) > 0:
            # log_debug(self._grid_str())
            # log_debug(grid.grid_str(path=path, start=start, end=end))
            return [coord(p.x + 1, p.y + 1) for p in path]
        else:
            log_debug(f"_PathGrid.find_path() cannot find path from {frm} to {to}")
            log_debug(grid.grid_str(path=path, start=start, end=end))
            return None
        
    def _grid_str(self) -> str:
        result = ""
        for col in self._grid:
            for row in col:
                result += str(row)
            result += "\n"
        return result



    
