import random

from pyke_pyxel import log_debug
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.signals import Signals
from .enemy import Enemy
from .skeleton import Skeleton

enemies: list[Enemy] = []

def launch_skeleton(game: FieldGame):
    skeleton = Skeleton()
    skeleton.launch(game, _random_location())
    enemies.append(skeleton)

def update(game: FieldGame):
    def _remove_enemy_sprite(sprite_id: int):
        game.remove_sprite_by_id(sprite_id)
    
    field = game.field
    for e in enemies:
        if not _should_skip_update(e):
            cells = field.cells_at(e._sprite.position, include_empty=False)
            result = e.update(cells)
            match result:
                case 0: # continue
                    pass
                case -1: # killed
                    # log_debug(f"enemies.update() remove {e._sprite._id}")
                    enemies.remove(e)
                    e._sprite.activate_animation("die", loop=False, on_animation_end=_remove_enemy_sprite)
                    Signals.send("enemy_dies", game)
                case _: # win with damage
                    enemies.remove(e)
                    e._sprite.activate_animation("kill", loop=False, on_animation_end=_remove_enemy_sprite)
                    Signals.send_with("enemy_attacks", game, result)

    if len(enemies) <= 8:
        launch_skeleton(game)

launch_locations = [
    Coord(2, 4), Coord(3, 2), Coord(4, 4), Coord(5, 6), Coord(7, 11), Coord(8, 8), Coord(9, 11), 
    Coord(10, 11), Coord(11, 11), Coord(12, 10), Coord(13, 10), Coord(14, 11), Coord(15, 11), Coord(16, 11), Coord(17, 10), Coord(18, 11), Coord(19, 12),
    Coord(20, 11), Coord(21, 11), Coord(22, 12), Coord(23, 13), Coord(24, 12), Coord(25, 9), Coord(26, 9),
    Coord(27, 10), Coord(28, 11), Coord(29, 11), Coord(30, 11), Coord(31, 11), Coord(32, 11),
    Coord(33, 7), Coord(34, 3), Coord(35, 6), Coord(36, 4), Coord(37, 2), Coord(38, 1)
]

def _random_location() -> Coord:
    pos = launch_locations[random.randint(0, (len(launch_locations)-1))]
    return pos.clone()

def _should_skip_update(enemy: Enemy) -> bool:
    speed = enemy._speed
    if speed == 10:
        return False
    
    skip_frequency = (10 - speed) / 10
    return random.random() < skip_frequency