from typing import Optional

from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.field_game import FieldGame

import random

class Beam:

    def __init__(self, x: int, y: int) -> None:
        self.colour: int = random.randint(1, 15)
        self.ttl: int = random.randint(80, 200)
        self.x: int = x
        self.y: int = y
        self.cells: list[Cell] = []

    def launch(self, field: CellField):
        for i in range(5):
            cell = field.cell_at(self.x + i, self.y)
            cell.colour = self.colour
            cell.can_propogate = True
            cell.ttl = 200
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
                match random.randint(0, 2):
                    case 0:
                        to = field.neighbour_N(cell)
                        if to and to.colour == self.colour:
                            to = field.neighbour_N(to)
                    case 1:
                        to = field.neighbour_NE(cell)
                        if to and to.colour == self.colour:
                            to = field.neighbour_NE(to)
                    case 2:
                        to = field.neighbour_NW(cell)
                        if to and to.colour == self.colour:
                            to = field.neighbour_NW(to)

                if to:
                    if to.colour == self.colour:
                        # already part of beam
                        print(f"Beam collission at {to.x},{to.y}=>{to.can_propogate}")

                    to.colour = self.colour
                    to.can_propogate = True
                    to.ttl = 200
                    new_cells.append(to)
            else:
                cell.ttl -= 1
                if cell.ttl <= 0:
                    cell.colour = 0  # Black
                else:
                    new_cells.append(cell)

        self.cells = new_cells

        return len(self.cells) > 0


beams: list[Beam] = []

def game_started(game: FieldGame):
    print("Game Started")

    field = game.field

    for i in range(3):
        x = random.randint(60 + (i * 10), field._width - 100)
        y = 300 # random.randint(200, 300)
        beam = Beam(x, y)
        beam.launch(field)
        beams.append(beam)

def game_state_update(field: CellField):
    beams_to_remove: list[Beam] = []
    for beam in beams:
        if beam.update(field) == False:
            beams_to_remove.append(beam)
    
    for beam in beams_to_remove:
        beams.remove(beam)

    if len(beams) == 0:
        print("All beams finished")