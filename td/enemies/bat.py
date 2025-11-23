from pyke_pyxel import Coord
from pyke_pyxel.cell_auto.game import CellAutoGame
from .enemy import Enemy

class Bat(Enemy):

    def __init__(self) -> None:
        super().__init__("bat", Coord(21,8))
        
    def launch(self, game: CellAutoGame, position: Coord):
        self._from_x = position.x
        self._from_y = position.y
        self._to_x = game.map.center_x

        # linear interpolation
        # Calculate the change in coordinates
        self._delta_x = self._to_x - self._from_x
        self._delta_y = game.map.bottom_y - self._from_y

        super().launch(game, position)

    def _move_towards_target(self) -> tuple[int, int]:
        position = self._sprite.position

        if self._delta_x == 0: # vertical line
            return (0, 1)
        
        to_y = position.y + 1
        # --- Linear Interpolation ---
        # x = start_x + (given_y - start_y) * (delta_x / delta_y)
        to_x = self._from_x + (to_y - self._from_y) * (self._delta_x / self._delta_y)

        move_x = 0
        if position.x < to_x:
            move_x = 1
        elif position.x > to_x:
            move_x = -1
        
        return (move_x, 1)
        
