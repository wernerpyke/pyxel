from typing import Callable, Optional
import pyxel
import constants
from . import draw
from .objects.map import Map, Coord
from .objects.sprite import Sprite, OpenableSprite, Animation
from .objects.player import Player

class Game:
    def __init__(self, title: str, spriteSheet: str):
        self._player: Player

        self.sprites: list[Sprite] = []
        self.spriteTick = 0

        self._map = Map(constants.SIZE.WINDOW, constants.SIZE.WINDOW)

        pyxel.init(constants.SIZE.WINDOW, constants.SIZE.WINDOW, fps=constants.FPS.GAME, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(f"../{spriteSheet}")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        pyxel.run(self.update, self.draw)

    def add_wall_sprite(self, wallType: Callable[[], Sprite], col: int, row: int):
        position = Coord(col, row)
        sprite = wallType()
        sprite.set_position(position)
        
        self.sprites.append(sprite)
        self._map.mark_blocked(position)

    def add_door_sprite(self, doorType: Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        position = Coord(col, row)
        sprite = doorType()
        sprite.set_position(position)
        
        if closed:
            sprite.close()
        else:
            sprite.open()

        self.sprites.append(sprite)

        self._map.mark_openable(position, sprite, closed)

    def add_player_sprite(self, 
                   idleFrame: Coord,
                   downAnimation: Animation,
                   upAnimation: Animation,
                   leftAnimation: Animation,
                   rightAnimation: Animation,
                   movementSpeed: int) -> Player:
        
        sprite = Sprite(idleFrame)
        sprite.add_animation("down", downAnimation)
        sprite.add_animation("up", upAnimation)
        sprite.add_animation("left", leftAnimation)
        sprite.add_animation("right", rightAnimation)

        self.player = Player(sprite, movementSpeed)
        self.sprites.append(sprite)
    
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
            for sprite in self.sprites:
                sprite.update_frame()

        # Background
        draw.background()
        # pyxel.bltm(0, 0, 0, 0, 0, constants.SIZE.WINDOW, constants.SIZE.WINDOW)
        
        # Sprites
        for sprite in self.sprites:
            draw.sprite(sprite)

        pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)
        