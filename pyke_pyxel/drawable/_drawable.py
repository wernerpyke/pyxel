from pyke_pyxel import Coord, GameSettings

class Drawable:
    def __init__(self) -> None:
        self._id = 0

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