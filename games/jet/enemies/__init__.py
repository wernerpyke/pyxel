import random

from pyke_pyxel import coord, area
from pyke_pyxel.rpg import RPGGame

from .spinner import Spinner

launch_areas: list[area] = [
    area(1, 1, 1, 40), # left

    area(1, 1, 40, 1), # top

    area(40, 1, 40, 40), #right

    area(1, 40, 40, 40) # bottom
    ]

targets: list[coord] = [
    coord(19, 21),
    coord(24, 21),

    coord(20, 24),
    coord(24, 24)
]

def random_launch_area() -> area:
    return random.choice(launch_areas)

def random_target() -> coord:
    return random.choice(targets)

def launch_spinner(game: RPGGame):
    spinner = Spinner()

    location = game.map.random_location(random_launch_area())
    spinner.set_position(location.position) # type: ignore warning

    # spinner.set_position(coord(1,2)

    game.room.add_enemy(spinner)
    spinner.move_to(random_target(), game.map)
