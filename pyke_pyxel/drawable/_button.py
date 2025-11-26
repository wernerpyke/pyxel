import pyxel
from pyke_pyxel import GameSettings, Coord

class Button:
    def __init__(self, name: str, up_frame: Coord, down_frame: Coord, col_tile_count: int = 1, row_tile_count: int = 1, resource_image_index: int=0) -> None:
        self._id = 0
        
        self.name = name
        self._up_frame = up_frame
        self._down_frame = down_frame
        self._col_tile_count = col_tile_count
        self._row_tile_count = row_tile_count
        self._resource_image_index = resource_image_index

        # TODO - this is only needed because Coord.contains() does not know how many tiles wide it is
        # Another possibility is to allow Coord() to be created with col_tile_count & row_tile_count
        size = GameSettings.get().size.tile
        self.width = col_tile_count * size 
        self.height = row_tile_count * size

        self.is_down = False
    
    def contains(self, x: int, y: int):
        min_x = self.position._x
        max_x = self.position._x + self.width
        if x < min_x or x > max_x:
            return False
        
        min_y = self.position._y
        max_y = self.position._y + self.height
        if y < min_y or y > max_y:
            return False
        return True

    def push_down(self):
        self.is_down = True
    
    def pop_up(self):
        self.is_down = False

    def set_position(self, position: Coord):
        self._position = position

    def _draw(self, settings: GameSettings):
        frame = self._up_frame
        if self.is_down:
            frame = self._down_frame
        position = self._position

        width = settings.size.tile * self._col_tile_count
        height = settings.size.tile * self._row_tile_count

        pyxel.blt(x=position.x,
                y=position.y,
                img=self._resource_image_index,
                u=frame.x,
                v=frame.y,
                w=width,
                h=height,
                colkey=settings.colours.sprite_transparency)

    def __eq__(self, other):
        return isinstance(other, Button) and self._id == other._id

    @property
    def position(self) -> Coord:
        return self._position