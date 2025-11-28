import pyxel

from pyke_pyxel import Coord, GameSettings

class TileMap:

    def __init__(self, resource_position: Coord, tiles_wide: int, tiles_high: int, resource_index: int, settings: GameSettings):
        super().__init__()
        screen_width = settings.size.window
        screen_height = settings.size.window
        
        # Cache the rendered map into an image
        repeat_cols = (screen_width // (tiles_wide * settings.size.tile)) + 1
        repeat_rows = (screen_height // (tiles_high * settings.size.tile)) + 1

        tm = pyxel.tilemaps[resource_index]
        tm_x = resource_position.x
        tm_y = resource_position.y
        tm_w = tiles_wide * settings.size.tile
        tm_h = tiles_high * settings.size.tile

        self._img = pyxel.Image(screen_width, screen_height)
        for col in range(repeat_cols):
            for row in range(repeat_rows):
                x = col * tm_w
                y = row * tm_h

                self._img.bltm(x, y, tm, tm_x, tm_y, tm_w, tm_h, settings.colours.sprite_transparency)

    def _draw(self, settings: GameSettings):
        screen_width = settings.size.window
        screen_height = settings.size.window
    
        pyxel.blt(0, 0, self._img, 0, 0, screen_width, screen_height, settings.colours.sprite_transparency)
    