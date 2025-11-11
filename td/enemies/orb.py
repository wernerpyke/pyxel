import math
import random

from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from td.state import STATE
from .enemy import Enemy

class Orb(Enemy):

    def __init__(self) -> None:
        super().__init__("orb", Coord(11,8), 
                         animation_frame_count=4,
                         power=1000, 
                         speed=2)

    def launch(self, game: FieldGame, position: Coord):
        start_x = position.x
        start_y = position.y

        self._center_x = start_x # Horizontal center line of the wave (D in the formula)

        # 1. Calculate Amplitude
        self._max_amplitude = game.map.shortest_distance_to_sides(start_x) - 10
        if self._max_amplitude < 1:
            self._amplitude = 1
        else:
            self._amplitude = random.randint(1, self._max_amplitude)
        
        cycles = 3 # Number of full sine cycles over the height
        # Frequency factor (B in the formula: B = (Cycles * 2*pi) / Total_Height)
        self._frequency_factor = (cycles * 2 * math.pi) / (STATE.map.height - start_y)
        
        return super().launch(game, position)

    def _move_towards_target(self) -> tuple[int, int]:
        at_x = self._sprite.position.x
        at_y = self._sprite.position.y

        # The X-coordinate is calculated using the sine function
        to_x = self._amplitude * math.sin(self._frequency_factor * at_y) + self._center_x

        # TODO - increase the amplitude
        # 1. in launch() amplitude = rand(1, max_amplitude/2)
        # 2. each time the orb changes direction (left to right etc), increase the amplitude by 50%

        delta_x = round(to_x) - at_x
        return (delta_x, 1)