from typing import Optional
import pyxel

from pyke_pyxel.fx import FX

from . import GameSettings, Coord, GameSettings
from . import TileMap
from . import draw, log_debug
from .signals import Signals
from .map import Map
from .sprite import Sprite, CompoundSprite
from .hud import HUD

class Game:
    """
    Game class that manages the core game loop, sprite management, and rendering.
    This class serves as the main controller for a Pyxel-based game, handling initialization,
    sprite lifecycle management, signal connections, and the update/draw loop. It manages
    game settings, sprites, tile maps, HUD, and visual effects.
    
    Signals:
        - `GAME.WILL_START`: Emitted before the game loop begins.
        - `GAME.UPDATE`: Emitted on every update frame.
        - `MOUSE.MOVE`: Sent when mouse position changes, enabled by `GameSettings.mouse_enabled`.
        - `MOUSE.DOWN`: Sent on left mouse button press, enabled by `GameSettings.mouse_enabled`.
        - `MOUSE.UP`: Sent on left mouse button release, enabled by `GameSettings.mouse_enabled`.
    """

    def __init__(self, settings: GameSettings, title: str, resources: str):
        """
        Initialize the Game instance.
        Parameters:
            settings (GameSettings): Configuration object containing debug flag, window and tile sizes,
                and FPS settings (game and animation). Also used to determine whether mouse input is enabled.
            title (str): Window title passed to pyxel.init.
            resources (str): Path to a resources file that will be loaded with pyxel.load.
        """

        _settings = GameSettings.get()
        _settings.debug = settings.debug
        _settings.size.window = settings.size.window
        _settings.size.tile = settings.size.tile
        _settings.fps.game = settings.fps.game
        _settings.fps.animation = settings.fps.animation

        self._settings = settings

        self._sprites: list[Sprite|CompoundSprite] = []
        self._animation_tick = 0

        self._map = Map(settings)

        self._tile_map: Optional[TileMap] = None

        self._hud: Optional[HUD] = None
        self._fx: Optional[FX] = None

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)

        pyxel.init(settings.size.window, settings.size.window, fps=settings.fps.game, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(resources)
        
        self._send_mouse_events = False
        self._mouse_at_x: int = 0
        self._mouse_at_y: int = 0
        if settings.mouse_enabled:
            pyxel.mouse(True)
            self._send_mouse_events = True

        self._sprite_id = 0 # TODO is it ok for this to just increment?
    
    def start(self):
        """
        Initializes and starts the game loop.

        Sends a signal indicating the game is about to start, then begins the main
        update and draw loop using Pyxel's run function.

        Signals:
            Signals.GAME.WILL_START: Sent before the game loop starts.
        """
        Signals.send(Signals.GAME.WILL_START, self)
        pyxel.run(self.update, self.draw)

    def add_sprite(self, sprite: Sprite|CompoundSprite):
        """
        Add a sprite to the game's sprite collection.

        Parameters:
            sprite (Sprite | CompoundSprite): The sprite object to add to the game.
                Can be either a single Sprite or a CompoundSprite containing multiple sprites.
        """
        self._sprite_id += 1
        sprite._id = self._sprite_id # self._sprites.__len__()
        self._sprites.append(sprite)

    def remove_sprite(self, sprite: Sprite|CompoundSprite):
        """
        Remove a sprite from the game's active sprite collection.
        
        Parameters:
        sprite : Sprite | CompoundSprite
            The sprite (or compound sprite) instance to remove from the game's internal
            sprite list.
        """
        
        # TODO
        # for both here, in remove_sprite_by_id and _sprite_removed
        # it might be cleaner to mark sprite._to_be_removed = True
        # and then removing them in update()
        #
        if sprite in self._sprites:
            self._sprites.remove(sprite)
            # log_debug(f"GAME.remove_sprite() {sprite._id}")

    def remove_sprite_by_id(self, sprite_id: int):
        """Remove the first sprite with the specified identifier from the game's sprite list.

        Parameters:
        sprite_id : int
            The identifier of the sprite to remove.
        """
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
    def map(self) -> Map:
        """Returns the `Map` instance for this game"""
        return self._map

    @property
    def hud(self) -> HUD:
        """Returns the `HUD` instance for this game"""
        if self._hud == None:
            self._hud = HUD()
        return self._hud
    
    @property
    def fx(self) -> FX:
        """Returns the `FX` instance for this game"""
        if self._fx == None:
            self._fx = FX(self._settings)
        return self._fx

    #
    # Signals
    #

    def _sprite_added(self, sprite: Sprite|CompoundSprite):
        sprite._id = self._sprites.__len__()
        log_debug(f"GAME.sprite_added() {sprite._id}")
        self._sprites.append(sprite)

    def _sprite_removed(self, sprite: Sprite|CompoundSprite):
        if sprite in self._sprites:
            self._sprites.remove(sprite)
            log_debug(f"GAME.sprite_removed() {sprite._id}")

# ===== PYXEL =====

    def update(self):
        """
        Pyxel lifecycle handler. Updates the game state for each frame.

        Signals:
            - GAME.UPDATE: Sent every update.
            - MOUSE.MOVE: Emitted when mouse position changes (if mouse_enabled).
            - MOUSE.DOWN: Emitted on left mouse button press (if mouse_enabled).
            - MOUSE.UP: Emitted on left mouse button release (if mouse_enabled).
        """

        Signals.send(Signals.GAME.UPDATE, self)

        # mouse
        if self._send_mouse_events:
            x = pyxel.mouse_x
            y = pyxel.mouse_y
            if (not x == self._mouse_at_x) or (not y == self._mouse_at_y):
                self._mouse_at_x = x
                self._mouse_at_y = y
                Signals.send_with(Signals.MOUSE.MOVE, self, (self._mouse_at_x, self._mouse_at_y))

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                Signals.send_with(Signals.MOUSE.DOWN, self, (self._mouse_at_x, self._mouse_at_y))
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                Signals.send(Signals.MOUSE.UP, self)

        # Sprite Animations
        if self._animation_tick < (self._settings.fps.game / self._settings.fps.animation):
            self._animation_tick += 1
        else:
            self._animation_tick = 0
            for sprite in self._sprites:
                if isinstance(sprite, Sprite):
                    sprite._update_frame()
                # TODO support CompoundSprite animations?

    def draw(self):    
        """
        Pyxel lifecycle handler. Render the current frame by drawing all visual components in order.
        Draws the background, sprites, HUD, and active visual effects.
        """
        self._draw_background()
        
        self._draw_sprites()

        if self._hud:
            self._hud._draw(self._settings)

        if self._fx and self._fx._is_active:
            self._fx._draw()

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
        