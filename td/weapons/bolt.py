from typing import Optional

from pyke_pyxel import COLOURS, DIRECTION, log_error
from pyke_pyxel.cell_auto.matrix import Matrix, Cell
from pyke_pyxel.base_types import Coord

from .weapon import Weapon

import random

class Bolt(Weapon):

    def __init__(self, location_name: str, position: Coord, orientation: str) -> None:
        super().__init__("bolt", position, power=random.randint(100, 200), speed=10)

        self.cell_count = 5

        self.colour: int = COLOURS.WHITE
        self.orientation = orientation
        
        self.propagate = []
        match location_name:
            case "1":
                self.propagate = [ DIRECTION.LEFT, DIRECTION.LEFT, DIRECTION.LEFT, DIRECTION.UP, DIRECTION.DOWN]

            case "2":
                self.propagate = [ DIRECTION.LEFT, DIRECTION.LEFT, DIRECTION.LEFT, DIRECTION.UP, DIRECTION.RIGHT]
        
            case "3":
                self.propagate=[ DIRECTION.UP, DIRECTION.UP, DIRECTION.LEFT, DIRECTION.LEFT, DIRECTION.RIGHT]
        
            case "4":
                self.propagate=[ DIRECTION.UP, DIRECTION.UP, DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.RIGHT]
        
            case "5":
                self.propagate=[ DIRECTION.RIGHT, DIRECTION.RIGHT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.LEFT]
        
            case "6":
                self.propagate=[ DIRECTION.RIGHT, DIRECTION.RIGHT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.DOWN]

        self.default_propogate = self.propagate[0]

    def launch(self, field: Matrix):
        for i in range(self.cell_count):
            if self.orientation == "horizontal":
                cell = field.cell_at(self.position.x + (i*2), self.position.y)
            else:
                cell = field.cell_at(self.position.x, self.position.y + (i*2))
            
            if cell:
                cell.tag = self.default_propogate
                cell.type = self.type
                cell.colour = self.colour
                cell.can_propogate = True
                cell.power = self.power
                self.cells.append(cell)

    def update(self, field: Matrix):
        new_cells = []

        for cell in self.cells:
            if cell.can_propogate:
                cell.can_propogate = False
                new_cells.append(cell)

                to = self._select_next_cell(cell, field)
                if to:
                    # Note: Bolt does not care whether to is empty - it does not do to.store_state
                    to.type = self.type
                    to.colour = self.colour
                    to.can_propogate = True
                    to.power = self.power
                    new_cells.append(to)
            else:
                cell.power -= 1
                if cell.power <= 0:
                    cell.reset()
                else:
                    new_cells.append(cell)

        self.cells = new_cells
    
    def kill(self):
        pass # allow the existing instance to continue
    
    def _select_next_cell(self, cell: Cell, field: Matrix) -> Optional[Cell]:
        to: Optional[Cell] = None

        next_d = self.propagate[random.randint(0, len(self.propagate)-1)]
        
        d = f"{cell.tag}-{next_d}"

        match d:
            case "up-left":
                to = field.neighbour_W(cell)
                if to and to.type == self.type:
                    to = field.neighbour_NW(cell)
            case "up-right":
                to = field.neighbour_E(cell)
                if to and to.type == self.type:
                    to = field.neighbour_NE(cell)

            case "down-left":
                to = field.neighbour_W(cell)
                if to and to.type == self.type:
                    to = field.neighbour_SW(cell)
            case "down-right":
                to = field.neighbour_E(cell)
                if to and to.type == self.type:
                    to = field.neighbour_SE(cell)
            
            case "left-up":
                to = field.neighbour_N(cell)
                if to and to.type == self.type:
                    to = field.neighbour_NW(cell)
            case "left-down":
                to = field.neighbour_S(cell)
                if to and to.type == self.type:
                    to = field.neighbour_SW(cell)
            
            case "right-up":
                to = field.neighbour_N(cell)
                if to and to.type == self.type:
                    to = field.neighbour_NE(cell)
            case "right-down":
                to = field.neighbour_S(cell)
                if to and to.type == self.type:
                    to = field.neighbour_SE(cell)

            # Jump cases
            case "up-up":
                to = field.neighbour_N(cell)
                if to and to.type == self.type:
                    to = field.neighbour_N(to)
            case "down-down":
                to = field.neighbour_S(cell)
                if to and to.type == self.type:
                    to = field.neighbour_S(to)
            case "left-left":
                to = field.neighbour_W(cell)
                if to and to.type == self.type:
                    to = field.neighbour_W(to)
            case "right-right":
                to = field.neighbour_E(cell)
                if to and to.type == self.type:
                    to = field.neighbour_E(to)

            # Conflict cases
            case "up-down":
                cell.tag = self.default_propogate
                to = self._select_next_cell(cell, field)
                # to = field.neighbour_SW(cell)
                # if to and to.type == self.type:
                #     to = field.neighbour_SE(cell)
            case "down-up":
                cell.tag = self.default_propogate
                to = self._select_next_cell(cell, field)
            case "left-right":
                cell.tag = self.default_propogate
                to = self._select_next_cell(cell, field)
            case "right-left":
                cell.tag = self.default_propogate
                to = self._select_next_cell(cell, field)
            case _:
                log_error(f"Bolt._select_next_cell() unrecognised direction {d}")
        if to:
            to.tag = next_d
        
        return to