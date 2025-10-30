import random

from pyke_pyxel import COLOURS, log_error, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import CellField, Cell
from .weapon import Weapon

class Fungus(Weapon):

    def __init__(self, position: Coord) -> None:
        super().__init__("fungus", position)

        self.colour = COLOURS.GREEN_MINT
        
        # TODO we'll use TTL to track the 'strength' of a cell.
        # if an enemy interacts with a cell the cell does damage to the enemy and
        # reduces its own ttl
        self.power = 30

        self.regrow: list[Cell] = []

    def launch(self, field: CellField):
        for i in range(5):
            cell = field.cell_at(self.position.x + (i*2), self.position.y)
            self.cells.append(self._prop(cell))

    def update(self, field: CellField) -> bool:
        new_cells = []

        # log_debug(f"Fungus {len(self.cells)} active cells")
        if len(self.regrow) > 0:
            for c in self.regrow:
                log_debug(f"Fungus waiting to regrow {c.x}/{c.y} from {c.type}")

        for c in self.regrow:
            if (c.type == self.type) or c.is_empty:
                c.type = self.type
                c.can_propogate = True
                # TODO - should we reset c.power here?
                self.cells.append(c)
                self.regrow.remove(c)

        propagate_to = 1
        if len(self.cells) < 10:
            propagate_to = 2

        for c in self.cells:
            if (not c.is_empty) and (not c.type == self.type):
                log_debug(f"Fungus {c.x}/{c.y} got usurped by {c.type}")
                self.regrow.append(c)
                continue

            if not c.can_propogate:
                log_error(f"Fungus cells contains non-propagating cell at x:{c.x} y:{c.y}")
            
            neighbours = field.neighbours(c, filter_for_type=Cell.TYPE_EMPTY)
            random.shuffle(neighbours)

            for i in range(0, propagate_to):
                if len(neighbours) > 0:
                    n = neighbours[0]
                    new_cells.append(self._prop(n))
                    neighbours.remove(n)

        c.can_propogate = False
        self.cells = new_cells

        return len(self.cells) > 0
    
    def _prop(self, cell: Cell) -> Cell:
        cell.type = self.type
        cell.colour = self.colour
        cell.can_propogate = True
        cell.power = self.power
        # log_debug(f"Fungus propagates to x:{cell.x} y:{cell.y}")
        return cell