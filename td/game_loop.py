from dataclasses import dataclass
from typing import Any, Optional
from pyke_pyxel import COLOURS, Coord, log_error
from pyke_pyxel.cell_auto.game import CellAutoGame

from td.state import STATE
from game_load import load_level

from ui import UI # Note: important that this not be imported as td.ui to preserve singleton weirdness

DEBUG_SKIP_TITLE_SCREEN=True

@dataclass
class UpdateQueueItem:
    type: str
    params: Optional[Any] = None

update_queue: list[UpdateQueueItem] = []

def start(game: CellAutoGame):
    ui = UI.get()
    if DEBUG_SKIP_TITLE_SCREEN:
        load_level(game)
        ui.state = "select_location"
        ui.life_meter.set_percentage(STATE.health_percentage)
        STATE.start()
    else:
        ui.show_title_screen(game)

    if STATE.music_enabled:
        game.start_music(0)

def update(game: CellAutoGame):
    _process_update_queue(game)

    state = UI.get().state
    if state == "select_title_screen_option" or state == "wait":
        return # TODO - this is not super robust
    
    STATE.update()
    STATE.enemies.update(game)
    STATE.weapons.update(game.matrix)

def _process_update_queue(game: CellAutoGame):
    for u in update_queue:
        match u.type:
            case "ui_fade_from_title_to_game":
                game.fx.circular_wipe(COLOURS.BLUE_DARK, True, "ui_title_screen_fade_out_complete")
                UI.get().state = "wait"
            case "load_level":
                UI.get().hide_title_screen(game)
                load_level(game)
                game.fx.circular_wipe(COLOURS.BLUE_DARK, False, "ui_game_screen_fade_in_complete")
                UI.get().state = "wait"
            case "hide_weapon_ui":
                UI.get().hide_weapons_ui(game)
            case "launch_weapon":
                _launch_weapon(u.params, game) # type: ignore
            case "launch_enemy":
                type: str = u.params[0] # type: ignore
                x: int = u.params[1] # type: ignore
                y: int = u.params[2] # type: ignore
                _launch_enemy(type, x, y, game)
            case _:
                log_error(f"game_loop._process_update_queue() unrecognised type:{u.type}")
    update_queue.clear()

def _launch_weapon(type: str, game: CellAutoGame):
    location = STATE.weapons.selected_location
    if not location:
        log_error("game_loop._process_launch_weapon no launch location")
        return

    match type:
        case "bolt":
            UI.get().set_weapon_marker(type, location, game)
            location.activate(type)
        case "fungus":
            UI.get().set_weapon_marker(type, location, game)
            location.activate(type)
        case "meteor":
            UI.get().set_weapon_marker(type, location, game)
            location.activate(type)
        case _:
            log_error(f"game_loop._process_launch_weapon unrecognised name:{type}")

def _launch_enemy(type: str, x: int, y: int, game: CellAutoGame):
    match type:
        case "bat":
            STATE.enemies.launch_bat(game, Coord.with_xy(x, y))
        case _:
            log_error(f"game_loop._process_launch_enemy unrecognised name {type}")

#
# Signals
#

def enemy_killed(game: CellAutoGame):
    STATE.score += 1
    ui = UI.get()
    text = ui.score_text
    text.set_colour(COLOURS.GREEN_MINT)
    text.set_text(f"{STATE.score}")
    ui.life_meter.set_percentage(STATE.health_percentage)

def enemy_attacks(game: CellAutoGame, other: int):
    damage = other
    # print(f"ENEMY SCORES damage:{damage}")
    STATE.score -= damage
    ui = UI.get()
    text = ui.score_text
    text.set_colour(COLOURS.RED)
    text.set_text(f"{STATE.score}")
    ui.life_meter.set_percentage(STATE.health_percentage)

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
    UI.get().state = "select_location"

def ui_weapon_selected(name: str):
    # The order is important - hide_weapon_ui clears STATE.launch_location
    # which is required by launch_weapon
    update_queue.append(UpdateQueueItem(f"launch_weapon", name))
    update_queue.append(UpdateQueueItem("hide_weapon_ui"))
