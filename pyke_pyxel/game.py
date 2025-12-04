from typing import Optional
import pyxel


from ._base_types import GameSettings, coord, GameSettings
from ._log import log_debug
from ._keyboard import Keyboard
from .drawable._tilemap import TileMap
from .signals import Signals
from .map import Map
from .sprite import Sprite, CompoundSprite
from .hud import HUD
from .fx import FX

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
        Args:
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
        _settings.colours.sprite_transparency = settings.colours.sprite_transparency
        _settings.colours.background = settings.colours.background
        _settings.display_smoothing_enabled = settings.display_smoothing_enabled
        _settings.full_screen_enabled = settings.full_screen_enabled
        _settings.mouse_enabled = settings.mouse_enabled


        self._settings = settings

        self._sprites: list[Sprite|CompoundSprite] = []
        self._frames_per_animation_tick = round(settings.fps.game / settings.fps.animation)
        self._animation_tick = 0

        self._map = Map(settings)

        self._tile_map: Optional[TileMap] = None

        self._hud: Optional[HUD] = None
        self._fx: Optional[FX] = None

        self._keyboard = Keyboard()

        Signals.connect("sprite_added", self._sprite_added)
        Signals.connect("sprite_removed", self._sprite_removed)

        pyxel.init(settings.size.window, settings.size.window, fps=settings.fps.game, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(resources)
        if settings.display_smoothing_enabled:
            pyxel.screen_mode(1)
        if settings.full_screen_enabled:
            pyxel.fullscreen(True)
        
        self._send_mouse_events = False
        self._mouse_at_x: int = 0
        self._mouse_at_y: int = 0
        if settings.mouse_enabled:
            pyxel.mouse(True)
            self._send_mouse_events = True

        self._sprite_id = 0 # TODO is it ok for this to just increment?

        self._paused = False
    
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

    def clear_all(self):
        """Clear all sprites, TileMap, HUD and FX"""
        self._sprites.clear()
        self._sprite_id =0

        self._tile_map = None

        if self._hud:
            self._hud._clear_all()

        if self._fx and self._fx.is_active:
            self._fx._clear_all()

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

    def set_tilemap(self, resource_position: coord, tiles_wide: int, tiles_high: int, resource_tilemap_index: int = 0):
        """
        Set a simplified version of standard Pyxel tilemaps as a background layer.
        The tilemap is horizontally and vertically repeated to fill up the screen width/height.

        For example:
            `game.set_tilemap(coord(10, 8), 4, 6)`
            will fetch a tilemap starting at column 10 and row 8 of the resource sheet and 
            load 4 columns and 6 rows which will then be repeated to fill the screen.
            
        Parameters:
        resource_position : coord
            The col/row position of the tilemap in the loaded resource sheet
        tiles_wide : int
            The width of the tilemap on the resource sheet
        tiles_high : int
            The height of the tilemap on the resource sheet
        resource_tilemap_index : int
            The index of the tilemap in the resource bundle
        """
        self._tile_map = TileMap(resource_position, tiles_wide, tiles_high, resource_tilemap_index, self._settings)
        # log_debug(f"GAME.add_tilemap() at {resource_position.x},{resource_position.y} size {tiles_wide}x{tiles_high}")

    def pause(self):
        """Pause the game loop. 
        This will pause:
        - Game logic update signals
        - Sprite animation
        
        But will not halt:
        - Keyboard and mouse input signals
        - Screen draw
        - Music
        """
        self._paused = True
    
    def unpause(self):
        """Unpause the game loop."""
        self._paused = False

    @property
    def is_paused(self):
        return self._paused

    def start_music(self, number: int):
        """Starts the music identified by the provided number. Music loops until `stop_music` is called."""
        pyxel.playm(number, loop=True)

    def stop_music(self):
        """Stops the currently playing music"""
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
    
    @property
    def keyboard(self) -> Keyboard:
        """Returns the `Keyboard` instance for this game"""
        return self._keyboard

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

        # keyboard
        self._keyboard._update(self)

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

        if not self._paused:
            Signals.send(Signals.GAME.UPDATE, self)
        else:
            return

        # Sprite Animations
        if self._animation_tick < self._frames_per_animation_tick:
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

        self._draw_hud()

        self._draw_fx()

        # pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)

    def _draw_background(self):
        pyxel.cls(self._settings.colours.background)

        if self._tile_map:
            self._tile_map._draw(self._settings)

    def _draw_sprites(self):
        for sprite in self._sprites:
            sprite._draw(self._settings)

    def _draw_hud(self):
        if hud := self._hud:
            hud._draw(self._settings)

    def _draw_fx(self):
        if self._fx and self._fx.is_active:
            self._fx._draw()
        