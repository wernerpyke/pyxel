from pyke_pyxel import coord, area
from pyke_pyxel.rpg import RPGGame

from .spinner import Spinner

def launch_spinner(game: RPGGame):
    spinner = Spinner()

    a = area(1, 1, 1, 40)
    location = game.map.random_location(a)
    spinner.set_position(location.position) # type: ignore warning

    game.room.add_enemy(spinner)
    spinner.move_to(coord(32, 30), game.map)