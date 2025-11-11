from dataclasses import dataclass
from typing import Any, Optional
from pyke_pyxel import COLOURS, log_error
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

from pyke_pyxel.sprite import Sprite
from td.state import STATE
from game_load import load_level

import weapons
import enemies
import ui

DEBUG_SKIP_TITLE_SCREEN=True

@dataclass
class UpdateQueueItem:
    type: str
    params: Optional[Any] = None

update_queue: list[UpdateQueueItem] = []

def game_started(game: FieldGame):
    if DEBUG_SKIP_TITLE_SCREEN:
        load_level(game)
        STATE.ui.state = "select_location"
        STATE.start()
    else:
        ui.show_title_screen(game)
        STATE.ui.state = "select_title_screen_option"

    if STATE.music_enabled:
        game.start_music(0)

def game_update(game: FieldGame):
    _process_update_queue(game)

    if STATE.ui.state == "select_title_screen_option" or STATE.ui.state == "wait":
        return # TODO - this is not super robust
    
    STATE.update()
    enemies.update(game)
    STATE.weapons.update(game.field)

def _process_update_queue(game: FieldGame):
    for u in update_queue:
        match u.type:
            case "ui_fade_from_title_to_game":
                game.fx.circular_wipe(COLOURS.BLUE_DARK, True, "ui_title_screen_fade_out_complete")
                STATE.ui.state = "wait"
            case "load_level":
                ui.hide_title_screen(game)
                load_level(game)
                game.fx.circular_wipe(COLOURS.BLUE_DARK, False, "ui_game_screen_fade_in_complete")
                STATE.ui.state = "wait"
            case "hide_weapon_ui":
                ui.hide_weapons_ui(game)
            case "launch_weapon":
                _process_launch_weapon(u.params, game) # type: ignore
            case "launch_enemy":
                type: str = u.params[0] # type: ignore
                x: int = u.params[1] # type: ignore
                y: int = u.params[2] # type: ignore
                _process_launch_enemy(type, x, y, game)
            case _:
                log_error(f"game_loop._process_update_queue() unrecognised type:{u.type}")
    update_queue.clear()

def _process_launch_weapon(type: str, game: FieldGame):
    location = STATE.weapons.selected_location
    if not location:
        log_error("game_loop._process_launch_weapon no launch location")
        return

    match type:
        case "bolt":
            ui.set_weapon_marker(type, location, game)
            location.activate(type)
        case "fungus":
            ui.set_weapon_marker(type, location, game)
            location.activate(type)
        case "meteor":
            ui.set_weapon_marker(type, location, game)
            location.activate(type)
        case _:
            log_error(f"game_loop._process_launch_weapon unrecognised name:{type}")

def _process_launch_enemy(type: str, x: int, y: int, game: FieldGame):
    match type:
        case "bat":
            enemies.launch_bat(game, Coord.with_xy(x, y))
        case _:
            log_error(f"game_loop._process_launch_enemy unrecognised name {type}")

#
# Signals
#

def enemy_killed(game: FieldGame):
    STATE.score += 1
    text = STATE.ui.score_text
    text.set_colour(COLOURS.GREEN_MINT)
    text.set_text(f"{STATE.score}")

def enemy_attacks(game: FieldGame, other: int):
    damage = other
    # print(f"ENEMY SCORES damage:{damage}")
    STATE.score -= damage
    text = STATE.ui.score_text
    text.set_colour(COLOURS.RED)
    text.set_text(f"{STATE.score}")

def enemy_spawns_enemy(sender, other):
    name: str = sender
    x: int = other[0]
    y: int = other[1]
    update_queue.append(UpdateQueueItem("launch_enemy", (name, x, y)))

def ui_game_start_selected(sender):
    update_queue.append(UpdateQueueItem("ui_fade_from_title_to_game"))

def ui_title_screen_fade_out_complete(sender):
    update_queue.append(UpdateQueueItem("load_level"))

def ui_game_screen_fade_in_complete(sender):
    STATE.start()
    STATE.ui.state = "select_location"

def ui_weapon_selected(name: str):
    # The order is important - hide_weapon_ui clears STATE.launch_location
    # which is required by launch_weapon
    update_queue.append(UpdateQueueItem(f"launch_weapon", name))
    update_queue.append(UpdateQueueItem("hide_weapon_ui"))
