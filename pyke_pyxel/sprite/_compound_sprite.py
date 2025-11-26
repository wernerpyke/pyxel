import pyxel
from pyke_pyxel import Coord, GameSettings, log_error

class CompoundSprite:
    """A multi-tile sprite composed of a grid of `Coord` tiles with optional overlay graphics.

    CompoundSprite manages a matrix of tile coordinates (cols x rows)
    and provides helpers to fill tiles or set individual tiles. Useful for
    larger objects built from multiple sprite tiles.

    The class also provides a graphics buffer allowing geometric shapes to be drawn over the sprite tiles
    """
    def __init__(self, name: str, cols: int, rows: int, resource_image_index: int=0):
        self.name = name
        self._id: int = 0
        self._position: Coord
        self._resource_image_index = resource_image_index

        self.cols: list[list[Coord|None]] = [[None for r in range(rows)] for c in range(cols)]

        self._graphics: list[tuple] = []

        self._img: pyxel.Image|None = None

    def fill_tiles(self, tile: Coord):
        """Fill the sprite with a tile"""
        for c in range(0, len(self.cols)):
            row = self.cols[c]
            for r in range(0, len(row)):
                row[r] = tile
        self._img = None

    def fill_col(self, col: int, from_row: int, to_row: int, tile_col: int, tile_rows: list[int]):
        """Fill one column (all rows) of a sprite with a sequence of tiles"""
        rows = self.cols[(col-1)]
        tile_index = 0
        for r in range((from_row-1), to_row):
            rows[r] = Coord(tile_col, tile_rows[tile_index])
            tile_index += 1
            tile_index = tile_index % len(tile_rows)
        self._img = None

    def fill_row(self, row: int, from_col: int, to_col: int, tile_row: int, tile_cols: list[int]):
        """Fill one row (all columns) of a sprite with a sequence of tiles"""
        tile_index = 0
        for col_i in range((from_col-1), to_col):
            col = self.cols[col_i]
            col[(row-1)] = Coord(tile_cols[tile_index], tile_row)
            tile_index += 1
            tile_index = tile_index % len(tile_cols)
        self._img = None

    def set_tile(self, col: int, row: int, tile: Coord):
        """Set one tile in the sprite"""
        self.cols[(col-1)][(row-1)] = tile
        self._img = None

    def clear_graphics(self):
        """Clear the graphics buffer"""
        self._graphics = []
        # TODO - PERFORMANCE in-memory pyxel.Image to render graphics only when they change

    def graph_rect(self, x: int, y: int, width_px: int, height_px: int, colour: int):
        """Draw a rectangle to the graphics buffer"""
        self._graphics.append(("rect", x, y, width_px, height_px, colour))

    def graph_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, colour: int):
        """Draw a triangle to the graphics buffer"""
        self._graphics.append(("tri", x1, y1, x2, y2, x3, y3, colour))

    def _draw(self, settings: GameSettings):
        # PERFORMANCE: use an in-memory pyxel Image to cache the rendered sprite
        # However, if we want to add animation to CompoundSprite does that mean that we need to store an Image per frame?
        if not self._img:
            self._img = self._cache_image(settings)
        
        pyxel.blt(x=self.position.x, 
                  y=self.position.y, 
                  img=self._img, 
                  u=0, 
                  v=0, 
                  w=self._img.width, 
                  h=self._img.height, 
                  colkey=settings.colours.sprite_transparency)

        for g in self._graphics:
            match g[0]:
                case "rect":
                    x = self._position.x + g[1]
                    y = self._position.y + g[2]
                    pyxel.rect(x,y,g[3],g[4],g[5])
                case "tri":
                    x1 = self._position.x + g[1]
                    y1 = self._position.y + g[2]
                    x2 = self._position.x + g[3]
                    y2 = self._position.y + g[4]
                    x3 = self._position.x + g[5]
                    y3 = self._position.y + g[6]
                    col = g[7]
                    pyxel.tri(x1,y1,x2,y2,x3,y3,col)
                case _:
                    log_error(f"CompoundSprite.draw() invalid graphics type {g[0]}")

    def _cache_image(self, settings: GameSettings) -> pyxel.Image:
        total_width = len(self.cols) * settings.size.tile
        total_height = len(self.cols[0]) * settings.size.tile
        img = pyxel.Image(total_width, total_height)
        
        # Set to transparent
        img.rect(0,0,total_width,total_height, settings.colours.sprite_transparency)

        for c in range(0, len(self.cols)):
            row = self.cols[c] 
            for r in range(0, len(row)):
                tile = row[r]
                if tile:
                    width = settings.size.tile
                    height = settings.size.tile
                    # if tile.is_flipped: TODO sprite.is_flipped
                    #    width *= -1

                    img.blt(x=(c * settings.size.tile),
                                y=(r * settings.size.tile),
                                img=self._resource_image_index,
                                u=tile.x,
                                v=tile.y,
                                w=width,
                                h=height,
                                colkey=settings.colours.sprite_transparency)
        return img
    
    def __eq__(self, other):
        return isinstance(other, CompoundSprite) and self._id == other._id

    def set_position(self, position: Coord):
        self._position = position

    @property
    def position(self) -> Coord:
        return self._position