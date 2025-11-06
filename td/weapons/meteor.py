import random

from pyke_pyxel import COLOURS, log_error, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell, CellField

from td.weapons.weapon import Weapon

class Meteor(Weapon):
    def __init__(self, position: Coord) -> None:
        to_x = 0
        if position.x >= 160: # right
            to_x = position.x + random.randint(10, 80)
        else:
            to_x = position.x - random.randint(10, 80)

        to_y = position.y - random.randint(80, 120)
        to = Coord.with_xy(to_x, to_y)

        super().__init__("wave", to, power=20, speed=10)

        self._from = position
        self._to = to
        self._has_landed = False

        self._radius = 0
        self._decay_rate = 1
        # TODO - calc max_radius as a way of determining decay rate

    @property
    def is_alive(self) -> bool:
        if self._radius == 0:
            return True
        else:
            return len(self.cells) > 0

    def launch(self, field: CellField):
        self.line = field.cells_in_line(self._from, self._to)
        self.line_index = 0

    def update(self, field: CellField):
        if not self._has_landed:
            for c in self.cells:
                c.reset()

            if self.line_index < (len(self.line)-1):
                center = self.line[self.line_index]
                self._draw_star(center, field)
                self.line_index += 1
            else:
                self._has_landed = True
            return True
        else:
            self._update_expand(field)
    
    def _draw_star(self, center: Cell, field: CellField):
        self.cells = []

        x, y = center.x, center.y
        if center.x % 2 == 0:
            # N
            self._add_star_cell(field.cell_at(x, (y-1)))
            self._add_star_cell(field.cell_at(x, (y-2)))
            # S
            self._add_star_cell(field.cell_at(x, (y+1)))
            self._add_star_cell(field.cell_at(x, (y+2)))
            # E
            self._add_star_cell(field.cell_at((x+1), y))
            self._add_star_cell(field.cell_at((x+2), y))
            # W
            self._add_star_cell(field.cell_at((x-1), y))
            self._add_star_cell(field.cell_at((x-2), y))
        else:
            # NE
            self._add_star_cell(field.cell_at(x+1, (y-1)))
            self._add_star_cell(field.cell_at(x+2, (y-2)))
            # NW
            self._add_star_cell(field.cell_at(x-1, (y-1)))
            self._add_star_cell(field.cell_at(x-2, (y-2)))
            # SE
            self._add_star_cell(field.cell_at(x+1, (y+1)))
            self._add_star_cell(field.cell_at(x+2, (y+2)))
            # SW
            self._add_star_cell(field.cell_at(x-1, (y+1)))
            self._add_star_cell(field.cell_at(x-2, (y+2)))

    def _add_star_cell(self, c:  Cell|None):
        if c:
            c.colour = COLOURS.RED
            c.power = self.power * 2
            self.cells.append(c)

    def _update_expand(self, field):
        self._radius += 1

        # POWER-UP: decay rate increases more slowly
        if self._radius > 40:
            self._decay_rate = 2
        if self._radius > 80:
            self._decay_rate = 3
        if self._radius > 120:
            self._decay_rate = 4
        if self._radius > 200:
            self._decay_rate = 5
        if self._radius > 220:
            self._decay_rate = 6

        new_cells = []
        for c in self.cells:
            if c.power > 0:
                c.power -= self._decay_rate
                self._update_cell_colour(c)
                new_cells.append(c)
            else:
                c.recall_state()

        TOLERANCE = 0.5 
        radius_outer_squared = (self._radius + TOLERANCE)**2
        radius_inner_squared = (self._radius - TOLERANCE)**2

        for y in range(field._height):
            for x in range(field._width):
                distance_squared = (x - self.position.x)**2 + (y - self.position.y)**2
                if (distance_squared > radius_inner_squared and 
                    distance_squared <= radius_outer_squared):
                    cell = field.cell_at(x, y)

                    if not cell.is_empty:
                        cell.store_state()

                    cell.type = self.type
                    cell.power = self.power
                    self._update_cell_colour(cell)
                    new_cells.append(cell)

        self.cells = new_cells

    def _update_cell_colour(self, c: Cell):
        ratio = c.power / self.power

        if ratio >= 0.9:
            c.colour = COLOURS.RED
        elif ratio >= 0.7:
            c.colour = COLOURS.ORANGE
        elif ratio >= 0.5:
            c.colour = COLOURS.YELLOW
        elif ratio >= 0.3:
            c.colour = COLOURS.PINK
        else:
            c.colour = COLOURS.BEIGE