import random

from pyke_pyxel import log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.signals import Signals
from .enemy import Enemy
from .skeleton import Skeleton

enemies: list[Enemy] = []

launch_locations = [
    # left
    Coord(1, 4),
    Coord(3, 2),

    Coord(4, 4),
    Coord(5, 6),

    Coord(7, 11),
    Coord(8, 8),

    Coord(9, 11),
    Coord(11, 11),
    Coord(12, 10),
    Coord(13, 10),
    Coord(14, 11),
    Coord(15, 11),

    Coord(16, 11),
    Coord(17, 10),
    Coord(18, 11),
    Coord(19, 12),
    
    # mid
    Coord(20, 11),
    Coord(21, 11),
    Coord(22, 12),
    Coord(23, 13),
    Coord(24, 12),
    Coord(25, 9),
    Coord(26, 9),

    # right
    Coord(27, 10),
    Coord(28, 11),
    Coord(29, 11),
    Coord(30, 11),
    Coord(31, 11),
    Coord(32, 11),
    
    Coord(33, 7),
    Coord(34, 3),
    Coord(35, 6),
    Coord(36, 4),
    Coord(37, 2),
]

def _random_location() -> Coord:
    pos = launch_locations[random.randint(0, (len(launch_locations)-1))]
    return pos.clone()

def launch_skeleton(game: FieldGame):
    skeleton = Skeleton()
    skeleton.launch(game, _random_location()) # positions[0].clone()) # _random_location())
    enemies.append(skeleton)

def update(game: FieldGame):
    field = game.field
    for e in enemies:
        cells = field.cells_at(e._sprite.position, include_empty=False)

        match e.update(cells):
            case 0: # continue
                pass
            case -1: # killed
                # log_debug(f"enemies.update() remove {e._sprite._id}")
                game.remove_sprite(e._sprite)
                enemies.remove(e)
                Signals.send("enemy_killed", game)
            case 1: # wins
                print(f"ENEMY WINS {e.power}")
                game.remove_sprite(e._sprite)
                enemies.remove(e)
                Signals.send("enemy_wins", game)

    if len(enemies) <= 8:
        launch_skeleton(game)