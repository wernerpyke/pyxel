import pyxel
from pyke_pyxel import coord

class TextSprite:
    """A simple text sprite for rendering text using a pyxel font.
    """

    def __init__(self, text: str, colour: int, font_file: str):
        self._text = text
        self._colour = colour
        self._font = pyxel.Font(font_file)

        self._id = 0

    def _draw(self):
        pyxel.text(self.position.x, self.position.y, self._text, self._colour, font=self._font)

    def set_position(self, position: coord):
        """
        Sets the position of the sprite.

        Args:
            position (Coord): The new coordinate for the sprite's top-left corner.
        """
        self._position = position

    @property
    def position(self) -> coord:
        """
        Returns the current position of the sprite.

        Returns:
            Coord: The coordinate of the sprite's top-left corner.
        """
        return self._position

    def set_text(self, text: str):
        """
        Sets the text content of the sprite.

        Args:
            text (str): The new text content.
        """

        self._text = text

    def set_colour(self, colour: int):
        self._colour = colour