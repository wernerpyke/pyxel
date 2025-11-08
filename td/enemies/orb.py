import math
import random

from pyke_pyxel import GLOBAL_SETTINGS
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from .enemy import Enemy

class Orb(Enemy):

    def __init__(self) -> None:
        super().__init__("orb", Coord(11,8), 
                         animation_frame_count=4,
                         power=1000, 
                         speed=3)

    def launch(self, game: FieldGame, position: Coord):
        start_x = position.x
        start_y = position.y
        end_y = 320

        self._center_x = start_x # Horizontal center line of the wave (D in the formula)

        # 1. Dynamically Calculate Amplitude
        distance_to_left = start_x - 10
        distance_to_right = 320 - start_x - 10
        self._max_amplitude = min(distance_to_left, distance_to_right)
        if self._max_amplitude < 1:
            self._amplitude = 1
        else:
            self._amplitude = random.randint(1, self._max_amplitude)
        
        
        cycles = 3 # Number of full sine cycles over the height
        # Frequency factor (B in the formula: B = (Cycles * 2*pi) / Total_Height)
        self._frequency_factor = (cycles * 2 * math.pi) / (end_y - start_y)
        
        return super().launch(game, position)

    def _move_towards_target(self) -> tuple[int, int]:
        at_y = self._sprite.position.y
        at_x = self._sprite.position.x

        # The X-coordinate is calculated using the sine function
        to_x = self._amplitude * math.sin(self._frequency_factor * at_y) + self._center_x

        # TODO - increase the amplitude
        # 1. in launch() amplitude = rand(1, max_amplitude/2)
        # 2. each time the orb changes direction (left to right etc), increase the amplitude by 50%

        delta_x = round(to_x) - at_x
        return (delta_x, 1)