from typing import Optional

from pyke_pyxel import COLOURS, DIRECTION, log_error
from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord

from .weapon import Weapon

import random

class Bolt(Weapon):

    def __init__(self, position: Coord, orientation: str, propagate: list[str]) -> None:
        super().__init__("bolt", position, power=random.randint(100, 200), speed=10)

        self.cell_count = 5

        self.colour: int = COLOURS.WHITE
        self.orientation = orientation
        self.propagate = propagate
        self.default_propogate = propagate[0]

    def launch(self, field: CellField):
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

    def update(self, field: CellField):
        if len(self.cells) == 0:
            return False
        
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
    
    def _select_next_cell(self, cell: Cell, field: CellField) -> Optional[Cell]:
        to: Optional[Cell] = None

        next_d = self.propagate[
            random.randint(0, len(self.propagate)-1)
            ]
        
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