from typing import Optional, Callable
import pyxel

from pyke_pyxel import coord, GameSettings

from ._anim import Animation

class Sprite:
    """A drawable sprite with optional animations.

    A Sprite contains a set of named Animation objects, a current active_frame
    to draw, and a position. Animations may be started, paused, resumed and
    looped. Sprites are lightweight containers for animation state and drawing
    metadata.

    Args:
        name (str): Logical name for the sprite.
        default_frame (coord): The frame to use when no animation is active (idle frame).
        cols (int): Width in tiles for framed sprites (used when advancing frames).
        rows (int): Height in tiles for framed sprites (used when advancing frames).
        resource_image_index (int): Index of the image resource (if multiple images are used).
    """
    def __init__(self, name: str, default_frame: coord, cols: int = 1, rows: int = 1, resource_image_index: int=0):
        self._id: int = 0
        self.name = name
        self.idle_frame = default_frame

        self.animations: dict[str, Animation] = { }
        self._position: coord
        self.active_frame = self.idle_frame
        self._animation: Animation|None = None

        self.col_tile_count = cols
        self.row_tile_count = rows

        self._resource_image_index = resource_image_index

        tile_size = GameSettings.get().size.tile
        self._width = cols * tile_size
        self._height = rows * tile_size

    def add_animation(self, name: str, animation: Animation):
        """Add an animation to the sprite.
        
        Args:
            name (str): The name to associate with the animation.
            animation (Animation): The Animation object to add.


        """
        animation._name = name
        self.animations[name] = animation

        # The animation needs to know how 'wide' the sprite is
        # to be able to update frames correctly
        animation._col_tile_count = self.col_tile_count

    def activate_animation(self, name: str, on_animation_end: Optional[Callable[[int], None]] = None):
        """Start the named animation.

        If the named animation is already active this is a no-op. When
        started the animation is unpaused, flip state is applied and the
        optional `on_animation_end` callback will be invoked when a
        non-looping animation finishes.
        """
        if self._animation and self._animation._name == name:
            return

        self._animation = self.animations[name]
        self._animation._activate(self._id, on_animation_end)

    def deactivate_animations(self):
        """Stop any active animation and reset flip state."""
        self._animation = None

    def set_position(self, position: coord):
        """
        Sets the position of the sprite.

        Args:
            position (coord): The new coordinate for the sprite's top-left corner.
        """
        self._position = position # .clone()

    @property
    def position(self) -> coord:
        """
        Returns the current position of the sprite.

        Returns:
            coord: The coordinate of the sprite's top-left corner.
        """
        return self._position
    
    @property
    def width(self) -> int:
        """
        Returns the width of the sprite in pixels.
        """
        return self._width
    
    @property
    def height(self) -> int:
        """
        Returns the height of the sprite in pixels.
        """
        return self._height
    
    def __eq__(self, other):
        return isinstance(other, Sprite) and self._id == other._id

    def _update_frame(self):
        
        if anim := self._animation:
            if frame := anim._update_frame():
                self.active_frame = frame
            else:
                self._animation = None
                self.active_frame = self.idle_frame
                
        else:
            self.active_frame = self.idle_frame

    def _draw(self, settings: GameSettings):
        frame = self.active_frame
        position = self._position

        width = self._width
        if self._animation and self._animation.flip:
            width *= -1

        pyxel.blt(x=position.x,
                y=position.y,
                img=self._resource_image_index,
                u=frame.x,
                v=frame.y,
                w=width,
                h=self._height,
                colkey=settings.colours.sprite_transparency)
