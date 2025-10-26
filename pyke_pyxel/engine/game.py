from typing import Callable
import pyxel

from . import draw
from .game_settings import GAME_SETTINGS
from .signals import Signals, DIRECTION
from .map import Map
from .sprite import Sprite, MovableSprite
from .actor import Actor
from .player import Player
from .enemy import Enemy
from .projectile import Projectile
from .room import Room

GLOBAL_SETTINGS: GAME_SETTINGS = GAME_SETTINGS()

class Game:
    def __init__(self, settings: GAME_SETTINGS, title: str, spriteSheet: str):
        GLOBAL_SETTINGS = settings
        self._settings = settings

        self._sprites: list[Sprite] = []
        self.movementTick = False
        self.spriteTick = 0

        self._map = Map()
        self.room = Room(self._map)

        self._player: Player
        self._actors: list[Actor] = []

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)
        Signals.connect("enemy_added", self._enemy_added)
        Signals.connect("enemy_removed", self._enemy_removed)

        pyxel.init(settings.size.window, settings.size.window, fps=settings.fps.game, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(f"../{spriteSheet}")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        pyxel.run(self.update, self.draw)

    def add_player(self, sprite: Callable[[], MovableSprite]) -> Player:
        _sprite = sprite()

        self.player = Player(_sprite)

        self._sprites.append(_sprite)

        self.player._id = self._actors.__len__()
        self._actors.append(self.player)

        return self.player

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
        # Keyboard
        if pyxel.btnp(pyxel.KEY_X):
            self.player.interact(self._map)
        elif pyxel.btnp(pyxel.KEY_Z):
            Signals.send(Signals.PLAYER.ATTACK, self.player)

        # Player Movement
        self.movementTick = not self.movementTick
        if self.movementTick:
            if pyxel.btn(pyxel.KEY_UP):
                self.player.move(DIRECTION.UP, self._map)
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.player.move(DIRECTION.DOWN, self._map)
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.player.move(DIRECTION.LEFT, self._map)
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.player.move(DIRECTION.RIGHT, self._map)
            else:
                self.player.stop_moving()

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

        pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)
        