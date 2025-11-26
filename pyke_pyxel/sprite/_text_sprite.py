import pyxel
from pyke_pyxel import Coord

class TextSprite:
    """A simple text sprite for rendering text using a pyxel font.
    """

    def __init__(self, text: str, colour: int, font_file: str):
        self._text = text
        self._colour = colour
        self._font = pyxel.Font(font_file)

        self._id = 0

    def draw(self):
        pyxel.text(self.position.x, self.position.y, self._text, self._colour, font=self._font)

    def set_position(self, position: Coord):
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position

    def set_text(self, text: str):
        self._text = text

    def set_colour(self, colour: int):
        self._colour = colour