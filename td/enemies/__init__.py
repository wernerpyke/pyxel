import random

from pyke_pyxel import log_debug, log_error
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from pyke_pyxel.signals import Signals
from td.enemies.mage import Mage
from td.state import STATE
from .enemy import Enemy
from .skeleton import Skeleton
from .orb import Orb
from .bat import Bat

enemies: list[Enemy] = []

def _launch_skeleton(game: FieldGame):
    skeleton = Skeleton()
    skeleton.launch(game, _random_location())
    enemies.append(skeleton)

def _launch_orb(game: FieldGame):
    orb = Orb()
    orb.launch(game, _random_location())
    enemies.append(orb)

def _launch_mage(game: FieldGame):
    mage = Mage()
    mage.launch(game, _random_location())
    enemies.append(mage)

def launch_bat(game: FieldGame, position: Coord):
    bat = Bat()
    bat.launch(game, position)
    enemies.append(bat)

def update(game: FieldGame):
    def _remove_enemy_sprite(sprite_id: int):
        game.remove_sprite_by_id(sprite_id)
    
    field = game.field
    for e in enemies:
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

    type = STATE.enemies.launch_enemy_type(len(enemies))
    if type:
        match type:
            case "skeleton":
                _launch_skeleton(game)
            case "orb":
                _launch_orb(game)
            case "mage":
                _launch_mage(game)
            case _:
                log_error(f"enemies.update invalid enemy type:{type}")
        

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