from typing import Callable, Optional
import pyxel

import constants
from . import draw
from .signals import Signals, DIRECTION
from .map import Map, Coord
from .sprite import Sprite, OpenableSprite, Animation
from .actor import Actor
from .player import Player
from .projectile import Projectile
from .room import Room

class Game:
    def __init__(self, title: str, spriteSheet: str):
        self._sprites: list[Sprite] = []
        self.spriteTick = 0

        self._map = Map(constants.SIZE.WINDOW, constants.SIZE.WINDOW)
        self.room = Room(self._map)

        self._player: Player
        self._actors: list[Actor] = []

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)

        pyxel.init(constants.SIZE.WINDOW, constants.SIZE.WINDOW, fps=constants.FPS.GAME, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(f"../{spriteSheet}")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        pyxel.run(self.update, self.draw)

    def add_player(self, sprite: Sprite, movementSpeed: int) -> Player:
        self.player = Player(sprite, movementSpeed)
        self._sprites.append(sprite)

        self._actors.append(self.player)

        return self.player

    def _sprite_added(self, sprite: Sprite):
        sprite._id = self._sprites.__len__()
        print(f"GAME.sprite_added() {sprite._id}")
        self._sprites.append(sprite)

    def _sprite_removed(self, sprite: Sprite):
        if sprite in self._sprites:
            self._sprites.remove(sprite)
            print(f"GAME.sprite_removed() ${sprite._id}")

# ===== PYXEL =====

    def update(self):
        # Keyboard
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player.interact(self._map)
        elif pyxel.btnp(pyxel.KEY_X):
            Signals.send(Signals.PLAYER.ATTACK, self.player)

        # Movement    
        if pyxel.btn(pyxel.KEY_UP):
            self.player.move(DIRECTION.UP, self._map)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player.move(DIRECTION.DOWN, self._map)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.player.move(DIRECTION.LEFT, self._map)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move(DIRECTION.RIGHT, self._map)
        else:
            self.player.stop()

        for actor in self._actors:
            actor.update(self._map)

    def draw(self):
        # Sprite Animations
        if self.spriteTick < (constants.FPS.GAME / constants.FPS.ANIMATION):
            self.spriteTick += 1
        else:
            self.spriteTick = 0
            for sprite in self._sprites:
                sprite.update_frame()
            
        # Background
        draw.background()
        
        # Sprites
        for sprite in self._sprites:
            draw.sprite(sprite)

        pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)
        