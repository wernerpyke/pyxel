import random

from pyke_pyxel import log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from .enemy import Enemy
from .skeleton import Skeleton

enemies: list[Enemy] = []

positions = [
    # left
    Coord(4, 4),
    Coord(7, 11),
    Coord(8, 8),
    
    # mid
    Coord(20, 11),
    Coord(24, 12),
    Coord(26, 9),

    # right
    Coord(34, 3),
    Coord(35, 6),
    Coord(34, 8),
]

def _random_location() -> Coord:
    pos = positions[random.randint(0, (len(positions)-1))]
    return pos.clone()

def launch_skeleton(game: FieldGame):
    skeleton = Skeleton()
    skeleton.launch(game, _random_location())
    enemies.append(skeleton)

def update(game: FieldGame):
    for e in enemies:
        if not e.update():
            log_debug(f"enemies.update() remove {e._sprite._id}")
            game.remove_sprite(e._sprite)
            enemies.remove(e)

    if len(enemies) <= 3:
        launch_skeleton(game)