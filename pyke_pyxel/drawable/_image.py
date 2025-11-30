import pyxel
from pyke_pyxel import Coord, GameSettings

from ._drawable import Drawable

class Image(Drawable):
    """
    Represents an image in the Pyxel resources image bank that can be positioned and rendered on the screen.

    Parameters
    ----------
    frame : Coord
        The `Coord` of the top-left corner of the image's graphic in the resource image.
    cols : int, optional
        The number of columns the image graphic occupies, by default 1.
    rows : int, optional
        The number of rows the image graphic occupies, by default 1.
    image_index : int, optional
        The index of the Pyxel resources image bank where the image graphics are located, by default 0.
    """
    def __init__(self, frame: Coord, cols: int = 1, rows: int = 1, image_index: int=0) -> None:
        super().__init__()
        self.frame = frame
        self.cols = cols
        self.rows = rows
        self.image_index = image_index

    def clone_to(self, frame: Coord) -> "Image":
        """
        Create a clone of this image but with a different `Coord` indicating the location 
        of the clone on the Pyxel image bank. The cloned instance will retain the 
        `cols`, `rows` and `image_index` values of this instance.
        The position of this image is not retained in the clone.
        """
        clone = Image(frame, self.cols, self.rows, self.image_index)
        return clone

    def _render_image(self, settings: GameSettings) -> pyxel.Image :
        width = settings.size.tile * self.cols
        height = settings.size.tile * self.rows

        img = pyxel.Image(width, height)
        # Set to transparent
        img.rect(0,0,width,height, settings.colours.sprite_transparency)
        
        img.blt(x=0,
                y=0,
                img=self.image_index,
                u=self.frame.x,
                v=self.frame.y,
                w=width,
                h=height,
                colkey=settings.colours.sprite_transparency)
        return img


    def _draw(self, settings: GameSettings):
        width = settings.size.tile * self.cols
        height = settings.size.tile * self.rows

        position = self.position

        pyxel.blt(x=position.x,
                y=position.y,
                img=self.image_index,
                u=self.frame.x,
                v=self.frame.y,
                w=width,
                h=height,
                colkey=settings.colours.sprite_transparency)
