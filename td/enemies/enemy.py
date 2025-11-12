import random
from pyke_pyxel import GLOBAL_SETTINGS, log_debug, log_error
from pyke_pyxel.base_types import Coord
from pyke_pyxel.cell_field import Cell
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.sprite import Animation, Sprite


class Enemy:
    def __init__(self, name: str, from_frame: Coord, power: float, speed: int, animation_frame_count:int = 2) -> None:
        sprite = Sprite(name, from_frame, 1, 1)
        
        sprite.add_animation("loop", Animation(from_frame, animation_frame_count))
        sprite.activate_animation("loop")

        sprite.add_animation("kill", Animation(Coord(5,9), 2))
        sprite.add_animation("die", Animation(Coord(7,9), 2))
        self._sprite = sprite

        self.power:float = power

        if speed > 10:
            log_error(f"Enemy({type}) speed > 10")
            speed = 10
        self._speed = speed

        # Calculate the boundaries of the win condition
        game_w = game_h = GLOBAL_SETTINGS.size.window
        self._plants_top_y = game_h - 24
        
        win_base_w = (game_w - 64) / 2
        self._base_top = game_h - 90
        self._base_left = win_base_w + 4
        self._base_right = game_w - win_base_w - 4

    def launch(self, game: FieldGame, position: Coord):
        # log_debug(f"Enemy.launch() {self._sprite._id} x:{position.x} y:{position.y}")
        self._sprite.set_position(position)
        game.add_sprite(self._sprite)

    def update(self, field_cells: list[Cell]) -> int: # 0: continue, -1: dies, 1: wins, 2: super wins
        if not self._should_skip_move():
            to = self._move_towards_target()
            self._sprite.position.move_by(to[0], to[1])
        
        if len(field_cells) > 0:
            #current_power = self.power
            for c in field_cells:
                if self.power > c.power:
                    self.power -= c.power
                    # TODO - there's a messy thing here, we're resetting a cell which may be in a weapon's active cells
                    # See Fungus.update(). Another possibility is to check if not c.can_propogate:
                    c.reset()
                    # c.power = 0
                else:
                    c.power -= self.power
                    self.power = 0
            #print(f"Enemy.update({self}) lost:{(current_power - self.power)} remaining:{self.power}")
        if self.power <= 0:
            return -1 # killed
        else:
            return self._calculate_win()
    
    def __str__(self):
        return f"{self._sprite.name}{self._sprite._id}"

    def _move_towards_target(self) -> tuple[int, int]:
        return (0, 1) # straight down

    def _calculate_win(self) -> int:
        max_y = self._sprite.position.max_y
        if max_y < self._base_top:
            return 0 # No

        if max_y >= self._plants_top_y: # in plants
            return 1 # Yes

        mid_x = self._sprite.position.mid_x
        if mid_x >= self._base_left and mid_x <= self._base_right: # in base
            return 2 # Super Yes
        else:
            return 0 # No
        
    def _should_skip_move(self) -> bool:
        speed = self._speed
        if speed == 10:
            return False
        
        skip_frequency = (10 - speed) / 10
        return random.random() < skip_frequency