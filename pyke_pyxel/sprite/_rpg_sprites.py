from typing import Optional
from pyke_pyxel import coord
from ._sprite import Sprite
from ._anim import Anim

OPEN: int = 0
CLOSED: int = 1
CLOSING: int = 2
OPENING: int = 3

class OpenableSprite(Sprite):
    """A Sprite that supports open/close states (e.g., doors, chests).

    The OpenableSprite exposes simple open/close methods and manages an
    internal status value that determines which frame is shown.
    """
    def __init__(self, name: str, openFrame: coord, closedFrame: coord, openingAnimation: Anim):
        super().__init__(name, openFrame)
        self._openFrame = openFrame
        self._closedFrame = closedFrame
        self._openingAnimation = openingAnimation

        self._status = OPEN

    def close(self):
        self._status = CLOSED
        self._update_frame()

    def open(self):
        self._status = OPEN
        self._update_frame()

    @property
    def is_closed(self) -> bool:
        return self._status == CLOSED
    
    @property
    def is_open(self) -> bool:
        return self._status == OPEN
    
    def _update_frame(self):
        match self._status:
            case 0: # Open
                self.active_frame = self._openFrame
                return
            
            case 1: # Closed
                self.active_frame = self._closedFrame

class MovableSprite(Sprite):
    """Sprite with movement-related configuration and convenience setters.

    MovableSprite stores a movement speed and provides helper methods to
    create simple directional animations (up/down/left/right).
    """

    def __init__(self, name: str, idleFrame: coord, movement_speed: int):
        super().__init__(name, idleFrame)
        self.movementSpeed = movement_speed

    def set_up_animation(self, start_frame: coord, frame_count: int, flip: bool = False):
        self.add_animation("up", Anim(start_frame, frame_count, flip=flip))

    def set_down_animation(self, start_frame: coord, frame_count: int, flip: bool = False):
        self.add_animation("down", Anim(start_frame, frame_count, flip=flip))

    def set_left_animation(self, start_frame: coord, frame_count: int, flip: bool = False):
        self.add_animation("left", Anim(start_frame, frame_count, flip=flip))

    def set_right_animation(self, start_frame: coord, frame_count: int, flip: bool = False):
        self.add_animation("right", Anim(start_frame, frame_count, flip=flip))