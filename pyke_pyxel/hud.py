from pyke_pyxel.game_settings import GameSettings
from .sprite import Sprite, TextSprite
from . import draw

class HUD:
    def __init__(self) -> None:
        self._text: list[TextSprite] = []

    def set_text(self, text: TextSprite):
       self._text.append(text)

    def get_text(self) -> TextSprite:
       return self._text[0] # type: ignore

    def _draw(self, settings: GameSettings):
       for t in self._text:
        draw.text(t, settings)