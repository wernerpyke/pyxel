import pyxel

from . import draw, log_debug
from .game_settings import GameSettings
from .signals import Signals
from .map import Map
from .sprite import Sprite
from .actor import Actor
from .enemy import Enemy

GLOBAL_SETTINGS: GameSettings = GameSettings()

class Game:
    def __init__(self, settings: GameSettings, title: str, sprite_sheet: str):
        GLOBAL_SETTINGS.debug = settings.debug
        GLOBAL_SETTINGS.size.window = settings.size.window
        GLOBAL_SETTINGS.size.tile = settings.size.tile
        GLOBAL_SETTINGS.fps.game = settings.fps.game
        GLOBAL_SETTINGS.fps.animation = settings.fps.animation
        self._settings = settings

        self._sprites: list[Sprite] = []
        self._animation_tick = 0

        self._map = Map()
        self.movement_tick: bool = False

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)

        # TODO - should the below move to CharacterGame?
        self._actors: list[Actor] = []
        Signals.connect("enemy_added", self._enemy_added)
        Signals.connect("enemy_removed", self._enemy_removed)
        # End TODO

        pyxel.init(settings.size.window, settings.size.window, fps=settings.fps.game, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(sprite_sheet)
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        Signals.send(Signals.GAME.STARTED, self)
        pyxel.run(self.update, self.draw)

    def _sprite_added(self, sprite: Sprite):
        sprite._id = self._sprites.__len__()
        log_debug(f"GAME.sprite_added() {sprite._id}")
        self._sprites.append(sprite)

    def _sprite_removed(self, sprite: Sprite):
        if sprite in self._sprites:
            self._sprites.remove(sprite)
            log_debug(f"GAME.sprite_removed() {sprite._id}")

    def _enemy_added(self, enemy: Enemy):
        self._actors.append(enemy)

    def _enemy_removed(self, enemy: Enemy):
        if enemy in self._actors:
            self._actors.remove(enemy)
            log_debug(f"GAME._enemy_removed() {enemy._id}")

# ===== PYXEL =====

    def update(self):
        # movement
        self.movement_tick = not self.movement_tick

        for actor in self._actors:
            actor._update(self._map, self.movement_tick)

        # Sprite Animations
        if self._animation_tick < (self._settings.fps.game / self._settings.fps.animation):
            self._animation_tick += 1
        else:
            self._animation_tick = 0
            for sprite in self._sprites:
                sprite.update_frame()

    def draw(self):    
        self._draw_background()
        
        self._draw_sprites()

        # pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)

    def _draw_background(self):
        draw.background(self._settings)

    def _draw_sprites(self):
        for sprite in self._sprites:
            draw.sprite(sprite, self._settings)
        