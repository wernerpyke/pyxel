import random

from pyke_pyxel import DIRECTION, log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.sprite import Animation, Sprite


class Enemy:
    def __init__(self, name: str, from_frame: Coord, power: int) -> None:
        self._sprite = Sprite(name, from_frame, 1, 1)
        self._sprite.add_animation("loop", Animation(from_frame, 2))
        self._sprite.activate_animation("loop")

        self.power = power

        self.skip_move_updates = 4 # this number reduces as speed increases
        self.skip_counter = 0

    def launch(self, game: FieldGame, position: Coord):
        # log_debug(f"Enemy.launch() {self._sprite._id} {position.y}")
        
        self._sprite.set_position(position)
        game.add_sprite(self._sprite)

    def _move_towards_target(self) -> tuple[int, int]:
        return (0, 1) # straight down

    def update(self, field_cells: list[Cell]) -> bool:
        self.skip_counter += 1
        if self.skip_counter >= self.skip_move_updates:
            # log_debug(f"Enemy.update() move {self._sprite._id}")
            to = self._move_towards_target()
            self._sprite.position.move_by(to[0], to[1])
            self.skip_counter = 0
        
        if len(field_cells) > 0:
            for c in field_cells:
                if self.power > c.power:
                    #print(f"ENEMY {self._sprite.name} EATS {c.power} => {self.power}")
                    self.power -= c.power
                    # TODO - there's a messy thing here, we're resetting a cell which may be in a weapon's active cells
                    # See Fungus.update(). Another possibility is to check if not c.can_propogate:
                    c.reset()
                    # c.power = 0
                else:
                    # print(f"ENEMY {self._sprite.name} KILLED {c.power} => {self.power}")
                    c.power -= self.power
                    self.power = 0

        if self.power <= 0:
            return False
        elif self._sprite.position.max_y > 320:
            print("Enemy.update() REMOVE WINNING ENEMY")
            return False
        else:
            return True