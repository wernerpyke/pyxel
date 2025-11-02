import pyxel

from typing import Optional, Callable
from .base_types import Coord

class Animation:
    def __init__(self, start_frame: Coord, frames: int, flip: Optional[bool] = False):
        self.start_frame = start_frame
        self.frames = frames
        self.flip: bool = True if flip else False
        self._name: str
        self._current_frame_index:int = 0

        self.paused = False

class Sprite:
    """
    Represents a game sprite
    
    Args:
        sheetCoordinate (Coordinate): The x/y-coordinate of the sprite on the resource sheet.
    """
    def __init__(self, name: str, idle_frame: Coord, col_tile_count: int = 1, row_tile_count: int = 1):
        self._id: int = 0
        self.name = name
        self.idle_frame = idle_frame

        self.animations: dict[str, Animation] = { }
        self._position: Coord
        self.active_frame = self.idle_frame
        self.is_flipped: bool = False

        self._animation: Optional[Animation] = None
        self._loop_animation: bool = True
        self._on_animation_end: Optional[Callable[[int], None]] = None

        self.col_tile_count: int = col_tile_count
        self.row_tile_count: int = row_tile_count

    def __eq__(self, other):
        return isinstance(other, Sprite) and self._id == other._id

    def add_animation(self, name: str, animation: Animation):
        animation._name = name
        self.animations[name] = animation
        
    def activate_animation(self, name: str, loop: bool = True, on_animation_end: Optional[Callable[[int], None]] = None):
        self._animation = self.animations[name]
        self._animation.paused = False
        self.is_flipped = self._animation.flip
        self._loop_animation = loop
        self._on_animation_end = on_animation_end

        self._animation._current_frame_index = 0

    def pause_animation(self):
        if self._animation:
            self._animation.paused = True

    def unpause_animation(self):
        if self._animation:
            self._animation.paused = False

    def deactivate_animations(self):
        if self._animation:
            self._animation.paused = False
        self._animation = None
        self.is_flipped = False

    def set_position(self, position: Coord):
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position

    def update_frame(self):
        anim = self._animation
        
        if anim:
            if anim._current_frame_index >= anim.frames:
                if self._loop_animation:
                    anim._current_frame_index = 0
                else:
                    if self._on_animation_end:
                        id = self._id
                        self._on_animation_end(id)
                        self._on_animation_end = None
                    else:
                        self.deactivate_animations()
            
            col = anim.start_frame._col + (anim._current_frame_index * self.col_tile_count)
            self.active_frame = Coord(col, anim.start_frame._row)

            anim._current_frame_index += 1

            # print(f"Sprite.update_frame() frame:{self._animation.startFrame._col}+{animation._currentFrame}={col} frameCol:{self.active_frame._col} x:{self.active_frame.x}")
        else:
            self.active_frame = self.idle_frame

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

class MovableSprite(Sprite):

    def __init__(self, name: str, idleFrame: Coord, movementSpeed: int):
        super().__init__(name, idleFrame)
        self.movementSpeed = movementSpeed

    def set_up_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("up", Animation(start_frame, frame_count, flip))

    def set_down_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("down", Animation(start_frame, frame_count, flip))

    def set_left_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("left", Animation(start_frame, frame_count, flip))

    def set_right_animation(self, start_frame: Coord, frame_count: int, flip: Optional[bool] = False):
        self.add_animation("right", Animation(start_frame, frame_count, flip))

class CompoundSprite:
    def __init__(self, name: str, cols: int, rows: int):
        self.name = name
        self._id: int = 0
        self._position: Coord

        self.cols: list[list[Coord]] = []
        for c in range(0, cols):
            row: list[Coord] = []
            for r in range(0, rows):
                row.append(Coord(c, r))
            self.cols.append(row)

    def __eq__(self, other):
        return isinstance(other, Sprite) and self._id == other._id

    def fill_tiles(self, tile: Coord):
        for c in range(0, len(self.cols)):
            row = self.cols[c]
            for r in range(0, len(row)):
                row[r] = tile

    # def fill_row(self, col: int, tile: Coord):
    #    rows = self.cols[(col-1)]
    #    for r in range(0, len(rows)):
    #            rows[r] = tile

    def fill_col(self, col: int, from_row: int, to_row: int, tile_col: int, tile_rows: list[int]):
        rows = self.cols[(col-1)]
        tile_index = 0
        for r in range((from_row-1), to_row):
            rows[r] = Coord(tile_col, tile_rows[tile_index])
            tile_index += 1
            tile_index = tile_index % len(tile_rows)

    def fill_row(self, row: int, from_col: int, to_col: int, tile_row: int, tile_cols: list[int]):
        tile_index = 0
        for col_i in range((from_col-1), to_col):
            col = self.cols[col_i]
            col[(row-1)] = Coord(tile_cols[tile_index], tile_row)
            tile_index += 1
            tile_index = tile_index % len(tile_cols)

    def set_tile(self, col: int, row: int, tile: Coord):
        self.cols[(col-1)][(row-1)] = tile

    def set_position(self, position: Coord):
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position

class TextSprite:
    def __init__(self, text: str, colour: int, font_file: str):
        self._text = text
        self._colour = colour
        self._font = pyxel.Font(font_file)

    def set_text(self, text: str):
        self._text = text

    def set_colour(self, colour: int):
        self._colour = colour