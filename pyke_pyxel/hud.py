from pyke_pyxel.button import Button
from pyke_pyxel.game_settings import GameSettings
from .sprite import CompoundSprite, Sprite, TextSprite
from . import draw

class HUD:
   def __init__(self) -> None:
      self._text: list[TextSprite] = []
      self._sprites: list[Sprite|CompoundSprite] = []
      self._sprite_id = 0
      self._buttons: list[Button] = []

   def add_text(self, text: TextSprite):
      self._text.append(text)

   def add_sprite(self, sprite: Sprite|CompoundSprite):
      self._sprite_id += 1
      sprite._id = self._sprite_id
      self._sprites.append(sprite)

   def remove_sprite(self, sprite: Sprite):
      # TODO - see Game.remove_sprite
      if sprite in self._sprites:
            self._sprites.remove(sprite)

   def add_button(self, button: Button):
      self._sprite_id += 1
      button._id = self._sprite_id
      self._buttons.append(button)

   def remove_button(self, button: Button):
      # TODO - see Game.remove_sprite
      if button in self._buttons:
            self._buttons.remove(button)

   def _draw(self, settings: GameSettings):
      for s in self._sprites:
         if isinstance(s, Sprite):
            draw.sprite(s, settings)
         else:
            draw.compound_sprite(s, settings)

      for b in self._buttons:
         draw.button(b, settings)

      for t in self._text:
         draw.text(t)