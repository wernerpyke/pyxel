from typing import Optional

from pyke_pyxel import DIRECTION

from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

import random

from pyke_pyxel.sprite import Sprite

class Bolt:

    def __init__(self, position: Coord, direction_preference: str) -> None:
        self.colour: int = 7 # White
        self.position = position
        self.direction_preference = direction_preference

        self.ttl: int = random.randint(30, 200)
        self.cells: list[Cell] = []

    def launch(self, field: CellField):
        for i in range(5):
            cell = field.cell_at(self.position.x + (i*2), self.position.y)
            cell.type = "bolt"
            cell.colour = self.colour
            cell.can_propogate = True
            cell.ttl = self.ttl
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
                        if to and to.type == "bolt":
                            to = field.neighbour_N(to)
                    case DIRECTION.RIGHT:
                        to = field.neighbour_NE(cell)
                        if to and to.type == "bolt":
                            to = field.neighbour_NE(to)
                    case DIRECTION.LEFT:
                        to = field.neighbour_NW(cell)
                        if to and to.type == "bolt":
                            to = field.neighbour_NW(to)

                if to:
                    if to.type == "bolt":
                        print(f"Bolt collission at {to.x},{to.y} prop:{to.can_propogate} col:{to.colour} ttl:{to.ttl}")

                    to.type = "bolt"
                    to.colour = self.colour
                    to.can_propogate = True
                    to.ttl = self.ttl
                    new_cells.append(to)
            else:
                cell.ttl -= 1
                if cell.ttl <= 0:
                    cell.reset()
                else:
                    new_cells.append(cell)

        self.cells = new_cells

        return len(self.cells) > 0


position_left = Coord(16, 33)
position_center = Coord(19, 32)
position_right = Coord(23, 33)

bolts: list[Bolt] = []

def game_started(game: FieldGame):
    print("Game Started")

    base = Sprite("2", Coord(1, 1), col_tile_count=8, row_tile_count=8)
    base.set_position(Coord(16, 32))
    game.add_sprite(base)

    field = game.field

    bolt = Bolt(position_left, DIRECTION.LEFT)
    bolt.launch(field)
    bolts.append(bolt)

    bolt = Bolt(position_center, DIRECTION.UP)
    bolt.launch(field)
    bolts.append(bolt)

    bolt = Bolt(position_right, DIRECTION.RIGHT)
    bolt.launch(field)
    bolts.append(bolt)

def game_state_update(field: CellField):
    beams_to_remove: list[Bolt] = []
    for beam in bolts:
        if beam.update(field) == False:
            beams_to_remove.append(beam)
    
    for beam in beams_to_remove:
        bolts.remove(beam)

    # if len(beams) == 0:
    #    print("All beams finished")