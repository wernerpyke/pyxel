import math
import pyxel
from ._base_types import Coord, GameSettings, COLOURS
from .signals import Signals

class _Effect:    
    def __init__(self, completion_signal: str|None):
        self._completion_signal: str | None = completion_signal
        self._active = True

    def _complete(self):
        self._active = False
        if signal := self._completion_signal:
            Signals.send(signal, self)
            self._completion_signal = None

    def _draw(self):
        raise NotImplementedError("Effect._draw() not implemented")

class _CircularWipe(_Effect):
    def __init__(self, colour: int, wipe_closed: bool, completion_signal: str|None, settings: GameSettings):
        super().__init__(completion_signal)

        self._colour = colour
        self._wipe_closed = wipe_closed
        self._width = settings.size.window
        self._height = settings.size.window
        self._center_x = settings.size.window // 2
        self._center_y = settings.size.window // 2
        self._max_radius = math.floor(math.sqrt(self._center_x**2 + self._center_y**2))
        self._radius_step = 3
        self._current_radius = 0

        if self._wipe_closed:
            self._current_radius = self._max_radius
        else:
            self._current_radius = 0

    def _draw(self):
        for y in range(0, self._height):
            for x in range(0, self._width):
                distance = math.sqrt((x - self._center_x)**2 + (y - self._center_y)**2)
                delta = distance - self._current_radius
                if delta <= 0:
                    pass
                elif delta < 5 and (x % 2 == 0) and (y % 2 == 0):
                    pyxel.pset(x, y, self._colour)
                else:
                    pyxel.pset(x, y, self._colour)

        if self._wipe_closed:
            self._current_radius -= self._radius_step
            if self._current_radius <= 0:
                self._complete()
        else:
            self._current_radius += self._radius_step
            if self._current_radius >= self._max_radius:
               self._complete()

class _Splatter(_Effect):
    def __init__(self, position: Coord, colour: int):
        super().__init__(None)
        self._colour = colour
        self._position = position
        self._iteration = 0

        self._origin_x = position.mid_x
        self._origin_y = position.max_y - 2

    def _draw(self):
        # Assume 60 FPS
        if self._iteration < 5:
            pyxel.pset(self._origin_x-1, self._origin_y, self._colour)
            pyxel.pset(self._origin_x, self._origin_y, self._colour)
            pyxel.pset(self._origin_x+1, self._origin_y, self._colour)
        elif self._iteration < 10:
            pyxel.pset(self._origin_x-1, self._origin_y+1, self._colour)
            pyxel.pset(self._origin_x, self._origin_y, self._colour)
            pyxel.pset(self._origin_x+1, self._origin_y+1, self._colour)
        elif self._iteration < 20:
            pyxel.pset(self._origin_x-2, self._origin_y+2, self._colour)
            pyxel.pset(self._origin_x, self._origin_y, self._colour)
            pyxel.pset(self._origin_x+2, self._origin_y+2, self._colour)
        # elif self._iteration < 40:
        #    pyxel.pset(self._origin_x-2, self._origin_y+2, self._colour)
        #    pyxel.pset(self._origin_x, self._origin_y, self._colour)
        #    pyxel.pset(self._origin_x+2, self._origin_y+2, self._colour)
        else:
            self._complete()
            return

        self._iteration += 1

class FX:
    """
    FX class for managing visual effects in the game, specifically circular wipe transitions that can open or close,
    transitioning between scenes or states.

    This class should be accessed through the `game` instance via `game.fx`.
    """

    def __init__(self, settings: GameSettings):
        self._settings = settings
        self._effects: list[_Effect] = []

    def circular_wipe(self, colour: int, wipe_closed: bool, completion_signal: str):
        """
        Create a full-screen circular wipe animation.

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
        wipe = _CircularWipe(colour, wipe_closed, completion_signal, self._settings)
        self._effects.append(wipe)

    def splatter(self, colour: int, position: Coord):        
        """
        Create a splatter effect at the specified position. 
        The splatter effect animates within a single tile for 30 frames.

        Parameters
        ----------
        colour : int
            Colour index/value to use for the splatter.
        position : Coord
            The coordinate where the splatter effect should appear.
        """
        splatter = _Splatter(position, colour)
        self._effects.append(splatter)

    def _clear_all(self):
        self._effects.clear()

    def _draw(self):
        for effect in self._effects:
            effect._draw()
            if not effect._active:
                self._effects.remove(effect)

    @property
    def is_active(self):
        return any(effect._active for effect in self._effects)
        