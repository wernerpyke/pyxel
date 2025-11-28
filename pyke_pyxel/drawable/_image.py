import pyxel
from pyke_pyxel import Coord, GameSettings

from ._drawable import Drawable

class Image(Drawable):
    def __init__(self, frame: Coord, col_tile_count: int = 1, row_tile_count: int = 1, resource_image_index: int=0) -> None:
        super().__init__()
        self.frame = frame
        self.col_tile_count = col_tile_count
        self.row_tile_count = row_tile_count
        self.resource_image_index = resource_image_index

    def _draw(self, settings: GameSettings):
        width = settings.size.tile * self.col_tile_count
        height = settings.size.tile * self.row_tile_count

        position = self.position

        pyxel.blt(x=position.x,
                y=position.y,
                img=self.resource_image_index,
                u=self.frame.x,
                v=self.frame.y,
                w=width,
                h=height,
                colkey=settings.colours.sprite_transparency)
