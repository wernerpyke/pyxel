from typing import Optional
from .map import Coord

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
    def __init__(self, idleFrame: Coord):
        self.idleFrame = idleFrame

        self.animations: dict[str, Animation] = { }
        self.position: Coord
        self.active_frame = self.idleFrame
        self.is_flipped: bool = False

        self._animation: Optional[Animation] = None

    def add_animation(self, name: str, animation: Animation):
        animation._name = name
        self.animations[name] = animation
        
    def activate_animation(self, name):
        # if self._animation and self._animation._name == name:
        #    return
        
        self._animation = self.animations[name]
        self.is_flipped = self._animation.flip

    def deactivate_animations(self):
        self._animation = None
        self.is_flipped = False

    def move(self, x: int, y: int):
        self.position.move(x, y)

    def update_frame(self):
        if self._animation:
            animation = self._animation
            animation._currentFrame += 1
            if animation._currentFrame >= animation.frames:
                animation._currentFrame = 0

            col = animation.startFrame._col + animation._currentFrame
            self.active_frame = Coord(col, animation.startFrame._row)

            # print(f"Sprite.update_frame() frame:{self._animation.startFrame._col}+{animation._currentFrame}={col} frameCol:{self.active_frame._col} x:{self.active_frame.x}")
        else:
            self.active_frame = self.idleFrame