from dataclasses import dataclass
from typing import Optional
import pyxel

from . import GLOBAL_SETTINGS
from .base_types import Coord, TileMap
from . import draw, log_debug
from .game_settings import GameSettings
from .signals import Signals
from .map import Map
from .sprite import Sprite, CompoundSprite
from .actor import Actor
from .enemy import Enemy
from .hud import HUD

class Game:
    def __init__(self, settings: GameSettings, title: str, resources: str):
        GLOBAL_SETTINGS.debug = settings.debug
        GLOBAL_SETTINGS.size.window = settings.size.window
        GLOBAL_SETTINGS.size.tile = settings.size.tile
        GLOBAL_SETTINGS.fps.game = settings.fps.game
        GLOBAL_SETTINGS.fps.animation = settings.fps.animation
        self._settings = settings

        self._sprites: list[Sprite|CompoundSprite] = []
        self._animation_tick = 0

        self._map = Map()
        self.movement_tick: bool = False

        self._tile_map: Optional[TileMap] = None

        self._hud: Optional[HUD] = None

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)

        # TODO - should the below move to CharacterGame?
        self._actors: list[Actor] = []
        Signals.connect("enemy_added", self._enemy_added)
        Signals.connect("enemy_removed", self._enemy_removed)
        # End TODO

        pyxel.init(settings.size.window, settings.size.window, fps=settings.fps.game, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(resources)
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")

        self._sprite_id = 0 # TODO is it ok for this to just increment?
    
    def start(self):
        Signals.send(Signals.GAME.STARTED, self)
        pyxel.run(self.update, self.draw)

    def add_sprite(self, sprite: Sprite|CompoundSprite):
        self._sprite_id += 1
        sprite._id = self._sprite_id # self._sprites.__len__()
        # log_debug(f"GAME.add_sprite() {sprite._id} {sprite.name}")
        # if sprite.name == "skeleton":
        #    print("YUCK")
        self._sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite|CompoundSprite):
        # TODO
        # for both here, in remove_sprite_by_id and _sprite_removed
        # it might be cleaner to mark sprite._to_be_removed = True
        # and then removing them in update()
        #
        if sprite in self._sprites:
            self._sprites.remove(sprite)
            # log_debug(f"GAME.remove_sprite() {sprite._id}")

    def remove_sprite_by_id(self, sprite_id: int):
        for s in self._sprites:
            if s._id == sprite_id:
                # log_debug(f"GAME.remove_sprite_by_id() {sprite_id}")
                self._sprites.remove(s)
                return

    def set_tilemap(self, resource_position: Coord, tiles_wide: int, tiles_high: int):
        self._tile_map = TileMap(resource_position, tiles_wide, tiles_high)
        # log_debug(f"GAME.add_tilemap() at {resource_position.x},{resource_position.y} size {tiles_wide}x{tiles_high}")

    def start_music(self, number: int):
        pyxel.playm(number, loop=True)

    def stop_music(self):
        pyxel.stop()

    @property
    def hud(self) -> HUD:
        if self._hud == None:
            self._hud = HUD()
        return self._hud

    def _sprite_added(self, sprite: Sprite|CompoundSprite):
        sprite._id = self._sprites.__len__()
        log_debug(f"GAME.sprite_added() {sprite._id}")
        self._sprites.append(sprite)

    def _sprite_removed(self, sprite: Sprite|CompoundSprite):
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
        Signals.send(Signals.GAME.UPDATE, self)

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
                if isinstance(sprite, Sprite):
                    sprite.update_frame()
                # TODO support CompoundSprite animations?

    def draw(self):    
        self._draw_background()
        
        self._draw_sprites()

        if self._hud:
            self._hud._draw(self._settings)

        # pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)

    def _draw_background(self):
        draw.background(self._settings.colours.background)

        if self._tile_map:
            draw.tile_map(self._tile_map, self._settings)

    def _draw_sprites(self):
        for sprite in self._sprites:
            if isinstance(sprite, Sprite):
                draw.sprite(sprite, self._settings)
            elif isinstance(sprite, CompoundSprite):
                draw.compound_sprite(sprite, self._settings)
        