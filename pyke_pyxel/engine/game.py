from typing import Callable, Optional
import pyxel

import constants
from . import draw
from .signals import Signals
from .map import Map, Coord
from .sprite import Sprite, OpenableSprite, Animation
from .player import Player

class Game:
    def __init__(self, title: str, spriteSheet: str): # , events: type[Events]):
        self._player: Player

        self._sprites: list[Sprite] = []
        self.spriteTick = 0

        self._map = Map(constants.SIZE.WINDOW, constants.SIZE.WINDOW)

        # self._events = events

        pyxel.init(constants.SIZE.WINDOW, constants.SIZE.WINDOW, fps=constants.FPS.GAME, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(f"../{spriteSheet}")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        pyxel.run(self.update, self.draw)

    def add_wall(self, wallType: Callable[[], Sprite], col: int, row: int):
        position = Coord(col, row)
        sprite = wallType()
        sprite.set_position(position)
        
        self._sprites.append(sprite)
        self._map.mark_blocked(position, sprite)

    def add_door(self, doorType: Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        position = Coord(col, row)
        sprite = doorType()
        sprite.set_position(position)
        
        if closed:
            sprite.close()
        else:
            sprite.open()

        self._sprites.append(sprite)

        self._map.mark_openable(position, sprite, closed)

    def add_player(self, sprite: Sprite, movementSpeed: int) -> Player:
        self.player = Player(sprite, movementSpeed)
        self._sprites.append(sprite)
    
        return self.player
        

# ===== PYXEL =====

    def update(self):
        # Keyboard
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player.interact(self._map)
        if pyxel.btn(pyxel.KEY_UP):
            self.player.move("up", self._map)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player.move("down", self._map)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.player.move("left", self._map)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move("right", self._map)
        else:
            self.player.stop()


        # Animation
        if self.spriteTick < (constants.FPS.GAME / constants.FPS.ANIMATION):
            self.spriteTick += 1
        else:
            self.spriteTick = 0

    def draw(self):
        # Sprite Animations
        if self.spriteTick == 0:
            for sprite in self._sprites:
                sprite.update_frame()

        # Background
        draw.background()
        # pyxel.bltm(0, 0, 0, 0, 0, constants.SIZE.WINDOW, constants.SIZE.WINDOW)
        
        # Sprites
        for sprite in self._sprites:
            draw.sprite(sprite)

        pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)
        