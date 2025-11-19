import math
import pyxel
from ._base_types import GameSettings, COLOURS
from .signals import Signals


class FX:
    """
    FX class for managing visual effects in the game, specifically circular wipe transitions that can open or close,
    transitioning between scenes or states.

    This class should be accessed through the `game` instance via `game.fx`.
    """

    def __init__(self, settings: GameSettings) -> None:
        self._completion_signal: str|None = None
        
        # TODO - move the circular wipe code out to either a class or functions
        self._colour: int = COLOURS.BLACK
        self._wipe_closed: bool = True
        self._width = settings.size.window
        self._height = settings.size.window
        self._center_x = settings.size.window // 2
        self._center_y = settings.size.window // 2

        # Calculate the maximum possible distance from the center to any corner
        self._max_radius = math.floor(math.sqrt(self._center_x**2 + self._center_y**2))
        self._radius_step = 3
        self._current_radius = 0

    def circular_wipe(self, colour: int, wipe_closed: bool, completion_signal: str):
        """
        Initialize and configure a circular wipe animation.

        Parameters
        ----------
        colour : int
            Colour index/value to use when rendering the wipe.
        wipe_closed : bool
            If True, the wipe is configured to close (shrink) toward the centre.
            If False, the wipe is configured to open (expand) outward.
        completion_signal : str
            Identifier of the signal/event to emit when the wipe animation finishes.
        """
        self._colour = colour
        self._wipe_closed = wipe_closed

        self._completion_signal = completion_signal

        if self._wipe_closed:
            self._current_radius = self._max_radius
        else:
            self._current_radius = 0

    @property
    def _is_active(self):
        return not self._completion_signal == None

    def _clear_all(self):
        pass

    def _draw(self):
        # Iterate through every pixel (y=row, x=column)
        for y in range(0, self._height):
            for x in range(0, self._width):
                # Calculate the distance of the pixel from the center (Euclidean distance)
                # Distance = sqrt((x - Cx)^2 + (y - Cy)^2)
                distance = math.sqrt(
                    (x - self._center_x)**2 + (y - self._center_y)**2
                )
                
                delta = distance - self._current_radius
                if delta <= 0: # If the pixel is inside the circle, leave transparent
                    pass
                elif delta < 5 and (x % 2 == 0) and (y % 2 == 0): # Create a ragged edge
                    pyxel.pset(x, y, self._colour)
                else:
                    pyxel.pset(x, y, self._colour)

        # 3. Update radius
        if self._wipe_closed:
            self._current_radius -= self._radius_step
            if (self._current_radius <= 0) and (signal := self._completion_signal):
                Signals.send(signal, self)                    
                self._completion_signal = None
        else:
            self._current_radius += self._radius_step
            if (self._current_radius >= self._max_radius) and (signal := self._completion_signal):
                Signals.send(signal, self)      
                self._completion_signal = None