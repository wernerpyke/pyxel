import random
import math

from pyke_pyxel import COLOURS, Coord, log_error, log_debug
from pyke_pyxel.cell_auto.matrix import Cell, Matrix

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

        super().__init__("meteor", to, power=20, speed=10)

        self._from = position
        self._to = to
        self._has_landed = False

        self._radius = 0
        self._decay_rate = 4 # POWER-UP reduce decay rate
        self._degrees_step = 4 # POWER-UP, reduce to 0.5. Generate one point for each step between 0 and 360
        # TODO - calc max_radius as a way of determining decay rate

    def launch(self, field: Matrix):
        self.line = field.cells_in_line(self._from, self._to)
        self.line_index = 0

    def update(self, field: Matrix):
        if not self._has_landed:
            for c in self.cells:
                c.reset()

            if self.line_index < (len(self.line)-1):
                center = self.line[self.line_index]
                self._draw_star(center, field)
                self.line_index += 1
            else:
                self._has_landed = True
        else:
            self._update_expand(field)
    
    def kill(self):
        pass # allow the existing instance to continue
    
    @property
    def is_alive(self) -> bool:
        if self._radius == 0:
            return True
        else:
            return len(self.cells) > 0

    def _draw_star(self, center: Cell, field: Matrix):
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

    def _update_expand(self, field: Matrix):
        self._radius += 1

        # POWER-UP: decay rate increases more slowly
        decay = self._decay_rate
        if self._radius > 40:
            decay = self._decay_rate * 1.2
        if self._radius > 80:
            decay = self._decay_rate * 1.5
        if self._radius > 120:
            decay = self._decay_rate * 2
        if self._radius > 160:
            decay = self._decay_rate * 2.2
        if self._radius > 200:
            decay = self._decay_rate * 2.5

        new_cells: list[Cell] = []
        for c in self.cells:
            if c.power > 0:
                c.power -= decay
                self._update_cell_colour(c)
                new_cells.append(c)
            else:
                c.recall_state()

        # print(f"DRAW NEW {len(new_cells)}")

        degrees = 0
        prev_x = prev_y = -1
        while degrees <= 360:
            
            # 1. Convert the angle to radians (required by math.cos/sin)
            radians = math.radians(degrees)
            degrees += self._degrees_step # make the loop safe
            
            # 2. Calculate the X and Y coordinates
            x = self._to.x + round(self._radius * math.cos(radians))
            y = self._to.y + round(self._radius * math.sin(radians))
            if x == prev_x and y == prev_y:
                continue # skip

            prev_x, prev_y = x, y

            cell = field.cell_at(x, y)
            if cell and not cell.type == self.type:

                if not cell.is_empty:
                    cell.store_state()

                cell.type = self.type
                cell.power = self.power
                self._update_cell_colour(cell)

                new_cells.append(cell)
                # print(f"cell: {x}/{y}")

        """
        MUCH SLOWER implementation - but draws a full (no gaps) circle
        TOLERANCE = 0.5 
        radius_outer_squared = (self._radius + TOLERANCE)**2
        radius_inner_squared = (self._radius - TOLERANCE)**2

        for y in range(field._height):
            for x in range(field._width):
                distance_squared = (x - self.position.x)**2 + (y - self.position.y)**2
                if (distance_squared > radius_inner_squared) and (distance_squared <= radius_outer_squared):
                    
                    cell = field.cell_at(x, y)

                    if not cell.is_empty:
                        cell.store_state()

                    cell.type = self.type
                    cell.power = self.power
                    self._update_cell_colour(cell)
                    new_cells.append(cell)
        """

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