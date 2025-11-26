from ._base_types import GameSettings
from .drawable._image import Image
from .drawable._button import Button
from .sprite import CompoundSprite, Sprite, TextSprite

class HUD:
   """
   HUD manages on-screen heads-up display elements for a game.
   
   This class should be accessed through the `game` instance via `game.hud`.
   """
   
   def __init__(self) -> None:
      self._text: list[TextSprite] = []
      self._images: list[Image] = []
      self._buttons: list[Button] = []
      self._sprite_id = 0
      self._sprites: list[Sprite|CompoundSprite] = []

   def add_text(self, text: TextSprite):
      """ Add a TextSprite to the HUD."""
      self._sprite_id += 1
      text._id = self._sprite_id
      self._text.append(text)

   def add_sprite(self, sprite: Sprite|CompoundSprite):
      """Add a Sprite or CompoundSprite to the HUD and assign a unique ID."""
      self._sprite_id += 1
      sprite._id = self._sprite_id
      self._sprites.append(sprite)

   def remove_sprite(self, sprite: Sprite):
      """
      Remove a Sprite or CompoundSprite from the HUD.

      Behavior:
      - If the provided sprite is present in the _sprites list, it is removed.
      - If the sprite is not present, the method does nothing (no exception raised).
      """
      # TODO - see Game.remove_sprite
      if sprite in self._sprites:
            self._sprites.remove(sprite)

   def add_button(self, button: Button):
      """Add a Button to the HUD and assign a unique ID."""
      self._sprite_id += 1
      button._id = self._sprite_id
      self._buttons.append(button)

   def remove_button(self, button: Button):
      """
      Remove a Button from the HUD.

      Behavior:
      - If the button is not present, the method does nothing (no exception raised).
      """
      # TODO - see Game.remove_sprite
      if button in self._buttons:
            self._buttons.remove(button)

   def add_image(self, image: Image):
      """Add an Image to the HUD and assign a unique ID."""
      self._sprite_id += 1
      image._id = self._sprite_id
      self._images.append(image)

   def remove_image(self, image: Image):
      """
      Remove an Image from the HUD.

      Behavior:
      - If the image is not present, the method does nothing (no exception raised).
      """
      # TODO - see Game.remove_sprite
      if image in self._images:
            self._images.remove(image)

   def _clear_all(self):
       self._sprites.clear()
       self._text.clear()
       self._buttons.clear()
       self._images.clear()
       self._sprite_id = 0

   def _draw(self, settings: GameSettings):
      for i in self._images:
          i._draw(settings)

      for s in self._sprites:
         s._draw(settings)

      for b in self._buttons:
         b._draw(settings)

      for t in self._text:
         t.draw()