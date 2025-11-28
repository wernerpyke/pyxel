import pyxel
from pyke_pyxel import GameSettings, Coord
from ._drawable import Drawable

class Button(Drawable):
    def __init__(self, name: str, up_frame: Coord, down_frame: Coord, col_tile_count: int = 1, row_tile_count: int = 1, resource_image_index: int=0) -> None:
        super().__init__()
        self.name = name
        self._up_frame = up_frame
        self._down_frame = down_frame
        self._col_tile_count = col_tile_count
        self._row_tile_count = row_tile_count
        self._resource_image_index = resource_image_index

        self._up_icon: Coord|None = None
        self._down_icon: Coord|None = None

        # TODO - this is only needed because Coord.contains() does not know how many tiles wide it is
        # Another possibility is to allow Coord() to be created with col_tile_count & row_tile_count
        size = GameSettings.get().size.tile
        self.width = col_tile_count * size 
        self.height = row_tile_count * size

        self._highlighted = False
        self.is_down = False
    
    def set_icon(self, up_icon: Coord, down_icon: Coord):
        self._up_icon = up_icon
        self._down_icon = down_icon

    def contains(self, x: int, y: int) -> bool:
        """
        Checks if the given coordinates are within the bounds of the button.

        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.

        Returns:
            bool: True if the coordinates are within the button's bounds, False otherwise.
        """
        min_x = self.position._x
        max_x = self.position._x + self.width
        if x < min_x or x > max_x:
            return False
        
        min_y = self.position._y
        max_y = self.position._y + self.height
        if y < min_y or y > max_y:
            return False
        return True

    def highlight(self, active: bool):
        """
        Highlight the button. This sets the icon of the button to its down/active state.
        No effect if the button does not have an icon
        
        Args:
            active (bool): Enable or disable highlighting

        """
        self._highlighted = active

    def push_down(self):        
        """Sets the button's state to 'down', drawing the down frame."""
        self.is_down = True
    
    def pop_up(self):
        """Sets the button's state to 'up', drawing the up frame."""
        self.is_down = False

    def check_mouse_move(self, x: int, y: int):
        """
        Ask the button to respond to mouse movement. The default reaction is:
        - MOUSE_IN: highlight=True
        - MOUSE_OUT: highlight=False, is_down=False
        
        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.
        """
        if self.contains(x, y):
            self.highlight(True)
        else:
            self.highlight(False)
            if self.is_down:
                self.pop_up()

    def _draw(self, settings: GameSettings):
        frame = self._up_frame
        icon_frame = self._up_icon
        if self.is_down:
            frame = self._down_frame
            icon_frame = self._down_icon
        elif self._highlighted:
            icon_frame = self._down_icon
        
        position = self.position

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
        
        if icon_frame:
            pyxel.blt(x=position.x,
                y=position.y,
                img=self._resource_image_index,
                u=icon_frame.x,
                v=icon_frame.y,
                w=width,
                h=height,
                colkey=settings.colours.sprite_transparency)