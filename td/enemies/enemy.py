from pyke_pyxel import log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.sprite import Animation, Sprite


class Enemy:
    def __init__(self, name: str, from_frame: Coord, power: int) -> None:
        self._sprite = Sprite(name, from_frame, 1, 1)
        self._sprite.add_animation("loop", Animation(from_frame, 2))
        self._sprite.activate_animation("loop")

        self.power = power
        self.skip_move_updates = 4 # this number reduces as speed increases
        self.skip_counter = 0 # self.skip_move_updates # to ensure that the first update draws

    def launch(self, game: FieldGame, position: Coord):
        log_debug(f"Enemy.launch() move {self._sprite._id}")
        self._sprite.set_position(position)
        game.add_sprite(self._sprite)

    def update(self) -> bool:
        self.skip_counter += 1
        if self.skip_counter >= self.skip_move_updates:
            log_debug(f"Enemy.update() move {self._sprite._id}")
            self._sprite.position.move_by(0, 1)
            self.skip_counter = 0
        
        self.power -= 1
        if self.power == 0:
            return False
        else:
            return True