

from typing import Callable, Optional
from pyke_pyxel._base_types import GameSettings, coord


class Anim:
    """
    An animation for a Sprite.

    Parameters
    ----------
    start_frame: coord
        The position of the initial frame of the animation
    frames: int
        The number of frames in the animation
    loop: bool
        Whether the animation should loop or not
    flip: bool
        Whether the animation image should be horizontally flipped
    fps: int
        The FPS that the animation should run at. This value cannot be larger than the global animation FPS set in `GameSettings.fps.animation`
    """
    def __init__(self, start_frame: coord, frames: int, loop: bool = True, flip: bool = False, fps: int|None = None):
        self._name = ""
        self._start_frame = start_frame
        self._frames = frames
        self._loop = loop
        self.flip = flip

        if fps:
            settings = GameSettings.get()
            if fps < settings.fps.animation:
                self.fps = fps
            else:
                raise ValueError(f"Animation() fps cannot be >= {settings.fps.animation}")

        self._current_frame_index:int = 0
        self._current_col = 0

        self._on_animation_end: Optional[Callable[[int], None]] = None
        self._skip_animation_frame_update: int|None = None
        self._skip_animation_frame_update_counter = 0

        # see Sprite.add_animation()
        self._sprite_id:int|None = None
        self._col_tile_count = 1
        

    def _activate(self, sprite_id: int, on_animation_end: Optional[Callable[[int], None]] = None):
        self._sprite_id = sprite_id
        self._on_animation_end = on_animation_end
        
        self._current_frame_index = 0
        self._current_col = self._start_frame._col + (self._current_frame_index * self._col_tile_count)

    def _update_frame(self) -> coord|None:
        if self._skip_animation_frame_update:
            if self._skip_animation_frame_update_counter < self._skip_animation_frame_update:
                self._skip_animation_frame_update_counter += 1
                return coord(self._current_col, self._start_frame._row)
            else:
                self._skip_animation_frame_update_counter = 0

        if self._current_frame_index >= self._frames:
            if self._loop:
                self._current_frame_index = 0
            else:
                if self._on_animation_end:
                    self._on_animation_end(self._sprite_id) # type: ignore
                    self._on_animation_end = None
                return None

        self._current_col = self._start_frame._col + (self._current_frame_index * self._col_tile_count)
        self._current_frame_index += 1
        return coord(self._current_col, self._start_frame._row)

class AnimationFactory:
    """
    Convenience class to create multiple `Animation` instances with the same number of frames and FPS.

    Parameters
    ----------
    frames : int
        The number of frames the created animations will have
    fps   : int
        The FPS of the created animations
    """
    def __init__(self, frames: int, fps: int|None = None):
        self._frames = frames
        self._fps = fps

    """
    Create an `Animation` instance at the given position.

    Parameters
    ----------
    position : coord
        The `coord` of the top-left corner of the animation's graphic on the Pyxel resource sheet.
    loop: bool
        Whether the animation should loop
    flip: bool
        Whether the animation image should be horizontally flipped
    Returns
    -------
    Animation
        The created `Animation` instance.
    """
    def at(self, position: coord, loop: bool = True, flip: bool = False) -> Anim:
        return Anim(position, frames=self._frames, fps=self._fps, loop=loop, flip=flip)