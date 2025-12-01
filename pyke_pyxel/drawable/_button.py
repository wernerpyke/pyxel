from typing import Literal
import pyxel
from pyke_pyxel.drawable import Drawable, Image
from pyke_pyxel.sprite import CompoundSprite

class Button(Drawable):
    """
    This class represents a clickable button in the UI. It is constructed from either `Image` or `CompoundSprite`
    objects for its 'up' and 'down' states. It can also have an optional icon, which can also be a
    `CompoundSprite` or a simple `Image`.

    The button's state changes in response to mouse interactions, such as
    highlighting when hovered over and appearing pressed ('down') when clicked.
    """
    def __init__(self, name: str, up: CompoundSprite|Image, down: CompoundSprite|Image):
        """
        Args:
            up (CompoundSprite|Image): The icon to display when the button is in its 'up' state.
            down (CompoundSprite|Image): The icon to display when the button is in its 'down' or highlighted state.
        """
        super().__init__()
        self.name = name

        self._up = up
        self._down = down

        self._icon_up: CompoundSprite|Image|None = None
        self._icon_down: CompoundSprite|Image|None = None

        self._text: str = ""
        self._text_font: pyxel.Font|None = None
        self._text_colour: int|None = None
        self._text_highlight_colour: int|None = None

        self._up_image: pyxel.Image|None = None
        self._down_image: pyxel.Image|None = None

        self._icon_up_image: pyxel.Image|None = None
        self._icon_down_image: pyxel.Image|None = None

        self._highlighted = False
        self.is_down = False

    def set_icon(self, up: CompoundSprite|Image, down: CompoundSprite|Image):
        """
        Sets the icon for the button.

        Args:
            up (CompoundSprite|Image): The icon to display when the button is in its 'up' state.
            down (CompoundSprite|Image): The icon to display when the button is in its 'down' or highlighted state.
        """
        self._icon_up = up
        self._icon_down = down

    def set_text(self, text: str, font: str, colour: int, alignment: Literal['left', 'center', 'right'] = 'left', highlight_colour: int|None = None):
        self._text = text
        self._text_font = pyxel.Font(font)
        self._text_colour = colour
        self._text_alignment = alignment
        self._text_highlight_colour = highlight_colour

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

    def _draw(self, settings):

        if not self._up_image:
            self._up_image = self._up._render_image(settings)
            self._down_image = self._down._render_image(settings)
            self.width = self._up_image.width
            self.height = self._up_image.height

        if self._icon_up and not self._icon_up_image:
            self._icon_up_image = self._icon_up._render_image(settings)
            self._icon_down_image = self._icon_down._render_image(settings) # type: ignore warning

        image = self._up_image
        icon_image = self._icon_up_image
        text_colour = self._text_colour
        
        if self.is_down:
            image = self._down_image
            icon_image = self._icon_down_image
            text_colour = self._text_highlight_colour
        elif self._highlighted:
            icon_image = self._icon_down_image
            text_colour = self._text_highlight_colour
        
        position = self.position

        pyxel.blt(x=position.x,
                y=position.y,
                img=image, # type: ignore warning
                u=0,
                v=0,
                w=self.width,
                h=self.height,
                colkey=settings.colours.sprite_transparency)
        
        if icon_image:
            pyxel.blt(x=position.x,
                    y=position.y,
                    img=icon_image,
                    u=0,
                    v=0,
                    w=icon_image.width,
                    h=icon_image.height,
                    colkey=settings.colours.sprite_transparency)
        
        if text_colour:
            width = self._text_font.text_width(self._text) # type: ignore warning
            height = 14 # TODO - this is a crappy guess
            
            match self._text_alignment:
                case "left":
                    text_x = icon_image.width if icon_image else 0
                case "center":
                    text_x = (self.width - width) / 2
                case "right":
                    text_x = self.width - width
                case _:
                    text_x = 0
            
            text_y = (self.height - height) / 2
            text_x = position.x + text_x
            text_y = position.y + text_y
            pyxel.text(text_x, text_y, self._text, text_colour, font=self._text_font)


    
