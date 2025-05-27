from typing import Optional
from .coord import Coord

class Animation:
    def __init__(self, startFrame: Coord, frames: int, flip: Optional[bool] = False):
        self.startFrame = startFrame
        self.frames = frames
        self.flip: bool = True if flip else False
        self._name: str
        self._currentFrame:int = 0

        # self.flip 

class Sprite:
    """
    Represents a game sprite
    
    Args:
        sheetCoordinate (Coordinate): The x/y-coordinate of the sprite on the resource sheet.
    """
    def __init__(self, name: str, idleFrame: Coord):
        self.name = name
        self.idleFrame = idleFrame

        self.animations: dict[str, Animation] = { }
        self._position: Coord # = Coord(0, 0)
        self.active_frame = self.idleFrame
        self.is_flipped: bool = False

        self._animation: Optional[Animation] = None
        self._loop_animation: bool = True

    def add_animation(self, name: str, animation: Animation):
        animation._name = name
        self.animations[name] = animation
        
    def activate_animation(self, name, loop: bool = True):
        self._animation = self.animations[name]
        self.is_flipped = self._animation.flip
        self._loop_animation = loop

    def deactivate_animations(self):
        self._animation = None
        self.is_flipped = False

    def set_position(self, position: Coord):
        # if self._position and self._position.is_different_grid_location(position):
        #     self._previousPosition = self._position
        self._position = position

    # def return_to_previous_position(self):
    #     if self._previousPosition:
    #         self._position = self._previousPosition
    #         self._previousPosition = None

    @property
    def position(self) -> Coord:
        return self._position

    def update_frame(self):
        anim = self._animation
        
        if anim:
            anim._currentFrame += 1
            if anim._currentFrame >= anim.frames:
                if self._loop_animation == False:
                    self.deactivate_animations()
                    return

                anim._currentFrame = 0
            
            col = anim.startFrame._col + anim._currentFrame
            self.active_frame = Coord(col, anim.startFrame._row)

            # print(f"Sprite.update_frame() frame:{self._animation.startFrame._col}+{animation._currentFrame}={col} frameCol:{self.active_frame._col} x:{self.active_frame.x}")
        else:
            self.active_frame = self.idleFrame

OPEN: int = 0
CLOSED: int = 1
CLOSING: int = 2
OPENING: int = 3

class OpenableSprite(Sprite):
    def __init__(self, name: str, openFrame: Coord, closedFrame: Coord, openingAnimation: Animation):
        super().__init__(name, openFrame)
        self._openFrame = openFrame
        self._closedFrame = closedFrame
        self._openingAnimation = openingAnimation
        
        self._status = OPEN

    def close(self):
        self._status = CLOSED
        self.update_frame()

    def open(self):
        self._status = OPEN
        self.update_frame()

    @property
    def is_closed(self) -> bool:
        return self._status == CLOSED
    
    @property
    def is_open(self) -> bool:
        return self._status == OPEN
    
    def update_frame(self):
        match self._status:
            case 0: # Open
                self.active_frame = self._openFrame
                return
            
            case 1: # Closed
                self.active_frame = self._closedFrame
