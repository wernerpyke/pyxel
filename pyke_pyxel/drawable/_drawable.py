import pyxel
from pyke_pyxel import Coord, GameSettings

class Drawable:
    def __init__(self) -> None:
        self._id = 0
        self.width = 0
        self.height = 0

        self._position: Coord|None = None

    def contains(self, x: int, y: int) -> bool:
        """
        Checks if the given coordinates are within the bounds of the button.

        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.

        Returns:
            bool: True if the coordinates are within the button's bounds, False otherwise.
        """
        min_x = self.position._x
        max_x = self.position._x + self.width
        if x < min_x or x > max_x:
            return False
        
        min_y = self.position._y
        max_y = self.position._y + self.height
        if y < min_y or y > max_y:
            return False
        return True

    def _render_image(self, settings: GameSettings) -> pyxel.Image:
        raise NotImplementedError("_Drawable._render_image() not implemented")

    def _draw(self, settings: GameSettings):
        raise NotImplementedError("_Drawable._draw() not implemented")

    @property
    def position(self) -> Coord:
        """
        Returns the current position of the drawable.

        Returns:
            Coord: The coordinate of the drawable's top-left corner.
        """
        if not self._position:
            raise ValueError(f"Drawable position not set via .set_position()")

        return self._position

    def set_position(self, position: Coord):        
        """
        Sets the position of the drawable.

        Args:
            position (Coord): The new coordinate for the drawable's top-left corner.
        """
        self._position = position

    def __eq__(self, other):
        return (not other._id == None) and self._id == other._id