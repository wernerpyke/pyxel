from typing import Optional

from pyke_pyxel import COLOURS, DIRECTION
from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord

from .weapon import Weapon

import random

class Bolt(Weapon):

    def __init__(self, position: Coord, direction_preference: str) -> None:
        super().__init__("bolt", position)

        self.colour: int = COLOURS.WHITE
        self.direction_preference = direction_preference
        self.power: int = random.randint(30, 200)

    def launch(self, field: CellField):
        for i in range(5):
            cell = field.cell_at(self.position.x + (i*2), self.position.y)
            cell.type = self.type
            cell.colour = self.colour
            cell.can_propogate = True
            cell.power = self.power
            self.cells.append(cell)

    def update(self, field: CellField) -> bool:
        if len(self.cells) == 0:
            return False
        
        new_cells = []

        for cell in self.cells:
            if cell.can_propogate:
                cell.can_propogate = False
                new_cells.append(cell)

                to: Optional[Cell] = None
                directions = []
                match self.direction_preference:
                    case DIRECTION.UP:
                        directions = [DIRECTION.UP, DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.UP, DIRECTION.UP]
                    case DIRECTION.LEFT:
                        directions = [DIRECTION.UP, DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.LEFT, DIRECTION.LEFT]
                    case DIRECTION.RIGHT:
                        directions = [DIRECTION.UP, DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.RIGHT, DIRECTION.RIGHT]

                preferred_direction = random.randint(0, len(directions)-1)
                preferred_direction = directions[preferred_direction]

                match preferred_direction:
                    case DIRECTION.UP:
                        to = field.neighbour_N(cell)
                        if to and to.type == self.type:
                            to = field.neighbour_N(to)
                    case DIRECTION.RIGHT:
                        to = field.neighbour_NE(cell)
                        if to and to.type == self.type:
                            to = field.neighbour_NE(to)
                    case DIRECTION.LEFT:
                        to = field.neighbour_NW(cell)
                        if to and to.type == self.type:
                            to = field.neighbour_NW(to)

                if to:
                    # Note: Bolt does not care whether to is empty
                    # it does not do to.store_state

                    # if to.type == self.type:
                    #    print(f"Bolt collission at {to.x},{to.y} prop:{to.can_propogate} col:{to.colour} ttl:{to.power}")

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

        return len(self.cells) > 0