from pyke_pyxel import COLOURS, log_error, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell, CellField

from td.weapons.weapon import Weapon

class Wave(Weapon):
    def __init__(self, position: Coord) -> None:
        super().__init__("wave", position)

        self.radius = 0

    def launch(self, field: CellField):
        pass

    def update(self, field: CellField) -> bool:
        if self.should_skip_update():
            return len(self.cells) > 0

        self.radius += 1

        new_cells = []
        for c in self.cells:
            if c.power > 0:
                c.power -= 1
                match c.power:
                    case 4:
                        c.colour = COLOURS.ORANGE
                    case 3:
                        c.colour = COLOURS.YELLOW
                    case 2:
                        c.colour = COLOURS.PINK
                    case 1:
                        c.colour = COLOURS.BEIGE
                new_cells.append(c)
            else:
                c.recall_state()

        TOLERANCE = 0.5 
        radius_outer_squared = (self.radius + TOLERANCE)**2
        radius_inner_squared = (self.radius - TOLERANCE)**2

        for y in range(field._height):
            for x in range(field._width):
                distance_squared = (x - self.position.x)**2 + (y - self.position.y)**2
                if (distance_squared > radius_inner_squared and 
                    distance_squared <= radius_outer_squared):
                    cell = field.cell_at(x, y)

                    if not cell.is_empty:
                        cell.store_state()

                    cell.type = self.type
                    cell.power = 5
                    cell.colour = COLOURS.RED
                    new_cells.append(cell)

        self.cells = new_cells

        return len(self.cells) > 0