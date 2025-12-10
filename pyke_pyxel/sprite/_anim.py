

from typing import Callable, Optional
from pyke_pyxel._base_types import GameSettings, coord


class Animation:
    """
    An animation for a Sprite.
    """
    def __init__(self, start_frame: coord, frames: int, loop: bool = True, flip: bool = False, fps: int|None = None, rotate: float|None = None):
        """
        Args:
            start_frame (coord): The position of the initial frame of the animation
            frames (int): The number of frames in the animation
            loop (bool): Whether the animation should loop or not
            flip (bool): Whether the animation image should be horizontally flipped
            fps (int): The FPS that the animation should run at. This value cannot be larger than the global animation FPS set in `GameSettings.fps.animation`
        """
        self._name = ""
        self._start_frame = start_frame
        self._frames = frames
        self._loop = loop
        self.flip = flip
        self.rotate = rotate

        self._current_frame_index:int = 0
        self._current_col = 0

        self._on_animation_end: Optional[Callable[[int], None]] = None
        self._skip_animation_frame_update: int|None = None
        self._skip_animation_frame_update_counter = 0

        if fps:
            settings = GameSettings.get()
            if fps < settings.fps.animation:
                # self.fps = fps
                self._skip_animation_frame_update = settings.fps.animation // fps
            else:
                raise ValueError(f"Animation() fps cannot be >= {settings.fps.animation}")

        # see Sprite.add_animation()
        self._sprite_id:int|None = None
        self._cols = 1
        

    def _activate(self, sprite_id: int, on_animation_end: Optional[Callable[[int], None]] = None):
        self._sprite_id = sprite_id
        self._on_animation_end = on_animation_end
        
        self._current_frame_index = 0
        self._current_col = self._start_frame._col + (self._current_frame_index * self._cols)

    def _update_frame(self) -> coord|None:
        if self._skip_animation_frame_update:
            if self._skip_animation_frame_update_counter < self._skip_animation_frame_update:
                self._skip_animation_frame_update_counter += 1
                return coord(self._current_col, self._start_frame._row)
            else:
                self._skip_animation_frame_update_counter = 0

        this_frame = self._current_frame_index

        if self._current_frame_index < (self._frames - 1):
            self._current_frame_index += 1
        else:
            if self._loop:
                self._current_frame_index = 0
            else:
                if self._on_animation_end:
                    self._on_animation_end(self._sprite_id) # type: ignore
                    self._on_animation_end = None
        
        self._current_col = self._start_frame._col + (this_frame * self._cols)
        return coord(self._current_col, self._start_frame._row)

class AnimationFactory:
    """Convenience class to create multiple `Animation` instances with the same number of frames and FPS."""
    def __init__(self, frames: int, fps: int|None = None, loop: bool = True):
        """
        Args:
            frames (int): The number of frames the created animations will have
            fps (int): The FPS of the created animations
        """
        self._frames = frames
        self._fps = fps
        self._loop = loop

    def at(self, position: coord, flip: bool = False, loop: bool|None = None, rotate: float|None = None) -> Animation:
        """
        Create an `Animation` instance at the given position.

        Args:
            position (coord): The `coord` of the top-left corner of the animation's graphic on the Pyxel resource sheet.
            loop (bool): Whether the animation should loop
            flip (bool): Whether the animation image should be horizontally flipped
            rotate (float): The number of degrees to rotate the sprite
        """

        l = loop if loop is not None else self._loop

        return Animation(position, frames=self._frames, fps=self._fps, loop=l, flip=flip, rotate=rotate)