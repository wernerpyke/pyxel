from typing import Callable, Optional
import pyxel

from . import draw
from .game_settings import GAME_SETTINGS
from .signals import Signals
from .map import Map
from .sprite import Sprite
from .actor import Actor
from .enemy import Enemy

GLOBAL_SETTINGS: GAME_SETTINGS = GAME_SETTINGS()

class Game:
    def __init__(self, settings: GAME_SETTINGS, title: str, sprite_sheet: str):
        GLOBAL_SETTINGS = settings
        self._settings = settings

        self._sprites: list[Sprite] = []
        self.movementTick = False
        self.spriteTick = 0

        self._map = Map()

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)

        # TODO - should the below move to CharacterGame?
        self._actors: list[Actor] = []
        Signals.connect("enemy_added", self._enemy_added)
        Signals.connect("enemy_removed", self._enemy_removed)

        pyxel.init(settings.size.window, settings.size.window, fps=settings.fps.game, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(sprite_sheet)
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        pyxel.run(self.update, self.draw)

    def _sprite_added(self, sprite: Sprite):
        sprite._id = self._sprites.__len__()
        print(f"GAME.sprite_added() {sprite._id}")
        self._sprites.append(sprite)

    def _sprite_removed(self, sprite: Sprite):
        if sprite in self._sprites:
            self._sprites.remove(sprite)
            print(f"GAME.sprite_removed() {sprite._id}")

    def _enemy_added(self, enemy: Enemy):
        self._actors.append(enemy)

    def _enemy_removed(self, enemy: Enemy):
        if enemy in self._actors:
            self._actors.remove(enemy)
            print(f"GAME._enemy_removed() {enemy._id}")

# ===== PYXEL =====

    def update(self):
        for actor in self._actors:
            actor.update(self._map, self.movementTick)

    def draw(self):
        # Sprite Animations
        if self.spriteTick < (self._settings.fps.game / self._settings.fps.animation):
            self.spriteTick += 1
        else:
            self.spriteTick = 0
            for sprite in self._sprites:
                sprite.update_frame()
            
        # Background
        draw.background(self._settings)
        
        # Sprites
        for sprite in self._sprites:
            draw.sprite(sprite, self._settings)

        # pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)
        