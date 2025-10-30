import random

from pyke_pyxel import COLOURS, log_error, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import CellField, Cell
from .weapon import Weapon

class Fungus(Weapon):

    def __init__(self, position: Coord) -> None:
        super().__init__("fungus", position)

        self.colour = COLOURS.GREEN
        
        # We'll use TTL to track the 'strength' of a cell.
        # if an enemy interacts with a cell the cell does damage to the enemy and
        # reduces its own ttl
        self.ttl = 30 

    def launch(self, field: CellField):
        for i in range(5):
            cell = field.cell_at(self.position.x + (i*2), self.position.y)
            self.cells.append(self._prop(cell))

    def update(self, field: CellField) -> bool:
        new_cells = []

        # log_debug(f"Fungus {len(self.cells)} active cells")

        propagate_to = 1
        if len(self.cells) < 10:
            propagate_to = 2

        for c in self.cells:
            if not c.can_propogate:
                log_error(f"Fungus cells contains non-propagating cell at x:{c.x} y:{c.y}")
            
            neighbours = field.neighbours(c, filter_for_type=Cell.TYPE_EMPTY)
            random.shuffle(neighbours)

            for i in range(0, propagate_to):
                if len(neighbours) > 0:
                    n = neighbours[0]
                    new_cells.append(self._prop(n))
                    neighbours.remove(n)

            # if did_propogate:
            #     c.can_propogate = False
            # else:
                # new_cells
        c.can_propogate = False
        self.cells = new_cells

        return len(self.cells) > 0
    
    def _prop(self, cell: Cell) -> Cell:
        cell.type = self.type
        cell.colour = self.colour
        cell.can_propogate = True
        cell.ttl = self.ttl
        # log_debug(f"Fungus propagates to x:{cell.x} y:{cell.y}")
        return cell