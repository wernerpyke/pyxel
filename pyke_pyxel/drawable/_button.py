import pyxel
from pyke_pyxel import GameSettings, Coord
from ._drawable import Drawable

class Button(Drawable):
    """
    A UI button that can be in an 'up' or 'down' state, and can display an icon.

    Parameters
    ----------
    name : str
        A unique identifier for the button.
    up_frame : Coord
        The `Coord` of the top-left corner of the button's graphic when in the 'up' state.
    down_frame : Coord
        The `Coord` of the top-left corner of the button's graphic when in the 'down' state.
    col_count : int, optional
        The number of tile columns the button graphic occupies, by default 1.
    row_count : int, optional
        The number of tile rows the button graphic occupies, by default 1.
    resource_image_index : int, optional
        The index of the Pyxel image bank where the button graphics are located, by default 0.
    """
    def __init__(self, name: str, up_frame: Coord, down_frame: Coord, cols: int = 1, rows: int = 1, resource_image_index: int=0) -> None:
        super().__init__()
        self.name = name
        self._up_frame = up_frame
        self._down_frame = down_frame
        self._col_count = cols
        self._row_count = rows
        self._resource_image_index = resource_image_index

        self._icon_up_frame: Coord|None = None
        self._icon_down_frame: Coord|None = None

        # TODO - this is only needed because Coord.contains() does not know how many tiles wide it is
        # Another possibility is to allow Coord() to be created with col_tile_count & row_tile_count
        size = GameSettings.get().size.tile
        self.width = cols * size 
        self.height = rows * size

        self._highlighted = False
        self.is_down = False
    
    def set_icon(self, up_frame: Coord, down_frame: Coord):
        self._icon_up_frame = up_frame
        self._icon_down_frame = down_frame

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
        icon_frame = self._icon_up_frame
        if self.is_down:
            frame = self._down_frame
            icon_frame = self._icon_down_frame
        elif self._highlighted:
            icon_frame = self._icon_down_frame
        
        position = self.position

        width = settings.size.tile * self._col_count
        height = settings.size.tile * self._row_count

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