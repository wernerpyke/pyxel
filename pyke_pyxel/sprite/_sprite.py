from typing import Optional, Callable
import pyxel

from pyke_pyxel import Coord, GameSettings

class Animation:
    """Represents a sequence of frames for a sprite animation.

    Parameters
    ----------
    start_frame : Coord
        The coordinate of the first frame in the animation strip.
    frames : int
        Number of frames in the animation.
    flip : Optional[bool]
        If True, the animation should be drawn flipped horizontally.
    """
    def __init__(self, start_frame: Coord, frames: int, flip: Optional[bool] = False):
        self._start_frame = start_frame
        self._frames = frames
        self.flip: bool = True if flip else False

        self._name: str
        self._current_frame_index:int = 0

        self._paused = False

class Sprite:
    """A drawable sprite with optional animations.

    A Sprite contains a set of named Animation objects, a current
    active_frame to draw, and a position. Animations may be started,
    paused, resumed and looped. Sprites are lightweight containers for
    animation state and drawing metadata.

    Parameters
    ----------
    name : str
        Logical name for the sprite.
    default_frame : Coord
        The frame to use when no animation is active (idle frame).
    col_tile_count, row_tile_count : int
        Width/height in tiles for framed sprites (used when advancing frames).
    resource_image_index : int
        Index of the image resource (if multiple images are used).
    """
    
    def __init__(self, name: str, default_frame: Coord, col_tile_count: int = 1, row_tile_count: int = 1, resource_image_index: int=0):
        self._id: int = 0
        self.name = name
        self.idle_frame = default_frame

        self.animations: dict[str, Animation] = { }
        self._position: Coord
        self.active_frame = self.idle_frame
        self.is_flipped: bool = False

        self._animation: Optional[Animation] = None
        self._loop_animation: bool = True
        self._on_animation_end: Optional[Callable[[int], None]] = None

        self.col_tile_count = col_tile_count
        self.row_tile_count = row_tile_count

        self._resource_image_index = resource_image_index

    def add_animation(self, name: str, animation: Animation):
        """Add an animation to the sprite.

        Parameters
        ----------
        name : str
            The name to associate with the animation.
        animation : Animation
            The Animation object to add.
        """
        animation._name = name
        self.animations[name] = animation
        
    def activate_animation(self, name: str, loop: bool = True, on_animation_end: Optional[Callable[[int], None]] = None):
        """Start the named animation.

        If the named animation is already active this is a no-op. When
        started the animation is unpaused, flip state is applied and the
        optional `on_animation_end` callback will be invoked when a
        non-looping animation finishes.
        """
        if self._animation and self._animation._name == name:
            return

        self._animation = self.animations[name]
        self._animation._paused = False
        self.is_flipped = self._animation.flip
        self._loop_animation = loop
        self._on_animation_end = on_animation_end

        self._animation._current_frame_index = 0

    def pause_animation(self):
        """Pause the currently active animation, if any."""
        if self._animation:
            self._animation._paused = True

    def unpause_animation(self):
        """Unpause the currently active animation, if any."""
        if self._animation:
            self._animation._paused = False

    def deactivate_animations(self):
        """Stop any active animation and reset flip state."""
        if self._animation:
            self._animation._paused = False
        self._animation = None
        self.is_flipped = False

    def set_position(self, position: Coord):
        """
        Sets the position of the sprite.

        Args:
            position (Coord): The new coordinate for the sprite's top-left corner.
        """
        self._position = position

    @property
    def position(self) -> Coord:
        """
        Returns the current position of the sprite.

        Returns:
            Coord: The coordinate of the sprite's top-left corner.
        """
        return self._position
    
    def __eq__(self, other):
        return isinstance(other, Sprite) and self._id == other._id

    def _update_frame(self):
        anim = self._animation

        if anim:
            if anim._current_frame_index >= anim._frames:
                if self._loop_animation:
                    anim._current_frame_index = 0
                else:
                    if self._on_animation_end:
                        id = self._id
                        self._on_animation_end(id)
                        self._on_animation_end = None
                    else:
                        self.deactivate_animations()

            col = anim._start_frame._col + (anim._current_frame_index * self.col_tile_count)
            self.active_frame = Coord(col, anim._start_frame._row)
            # print(f"Sprite.update_frame() frame:{anim._start_frame._col}+({anim._current_frame_index}*{self.col_tile_count})={col} frameCol:{self.active_frame._col} x:{self.active_frame.x}")

            anim._current_frame_index += 1
        else:
            self.active_frame = self.idle_frame

    def _draw(self, settings: GameSettings):
        frame = self.active_frame
        position = self._position

        width = settings.size.tile * self.col_tile_count
        height = settings.size.tile * self.row_tile_count
        if self.is_flipped:
            width *= -1

        pyxel.blt(x=position.x,
                y=position.y,
                img=self._resource_image_index,
                u=frame.x,
                v=frame.y,
                w=width,
                h=height,
                colkey=settings.colours.sprite_transparency)

