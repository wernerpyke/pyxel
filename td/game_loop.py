from dataclasses import dataclass
from typing import Any, Optional
from pyke_pyxel import COLOURS, Coord, log_error
from pyke_pyxel.cell_auto.game import CellAutoGame

from td.state import STATE
from game_load import load_level

from ui import UI

DEBUG_SKIP_TITLE_SCREEN=False
DEBUG_TRIGGER_POWER_UP= False
DEBUG_TRIGGER_GAME_OVER=False

@dataclass
class _Update:
    type: str
    params: Optional[Any] = None

update_queue: list[_Update] = []

def start(game: CellAutoGame):
    if DEBUG_SKIP_TITLE_SCREEN:
        load_level(game)
        ui_game_screen_fade_in_complete(None)
    elif DEBUG_TRIGGER_GAME_OVER:
        UI.show_game_over_screen(game)
    else:
        UI.show_title_screen(game)

    if STATE.music_enabled:
        game.start_music(0)

def update(game: CellAutoGame):
    _process_update_queue(game)

    if UI.state_is_waiting():
        return
    
    STATE.update(game)
    text = UI.timer_text
    text.set_text(STATE.running_time_text)

def _process_update_queue(game: CellAutoGame):
    for u in update_queue:
        match u.type:
            case "ui_display_title_screen":
                UI.show_title_screen(game)
            case "ui_fade_from_title_to_game":
                game.fx.circular_wipe(COLOURS.BLUE_DARK, True, "ui_title_screen_fade_out_complete")
                UI.state_to_waiting()
            case "load_level":
                UI.hide_title_screen(game)
                load_level(game)
                game.fx.circular_wipe(COLOURS.BLUE_DARK, False, "ui_game_screen_fade_in_complete")
                UI.state_to_waiting()
            case "hide_weapon_ui":
                UI.hide_weapons_ui(game)
            case "launch_weapon":
                _launch_weapon(u.params, game) # type: ignore
            case "deactivate_weapon":
                _deactivate_weapon(u.params, game) # type: ignore
            case "launch_enemy":
                type: str = u.params[0] # type: ignore
                x: int = u.params[1] # type: ignore
                y: int = u.params[2] # type: ignore
                _launch_enemy(type, x, y, game)
            case "game_over":
                STATE.enemies.clear_all()
                STATE.weapons.clear_all()
                UI.state_to_waiting()
                game.fx.circular_wipe(COLOURS.PURPLE, True, "ui_game_over_fade_out_complete")
            case "ui_display_game_over_screen":
                game.clear_all() # Required to clear out any sprites from the previous game after game-over
                UI.show_game_over_screen(game)
            case "ui_hide_game_over_screen":
                UI.hide_game_over_screen(game)
            case "ui_display_power_up":
                UI.show_power_up(game)
            case _:
                log_error(f"game_loop._process_update_queue() unrecognised type:{u.type}")
    update_queue.clear()

def _launch_weapon(type: str, game: CellAutoGame):
    location = STATE.weapons.selected_location
    if not location:
        log_error("game_loop._process_launch_weapon no launch location")
        return

    if STATE.acquire_weapon(type):
        UI.life_meter.set_percentage(STATE.health_percentage)
        UI.set_weapon_marker(type, location, game)
        location.activate(type)

def _deactivate_weapon(location_id: str, game: CellAutoGame):
    location = STATE.weapons.location_by_id(location_id)
    if location:
        location.deactivate()
        UI.remove_weapon_marker(location, game)
    else:
        log_error(f"game_loop._deactivate_weapon() invalid location_id:{location_id}")

def _launch_enemy(type: str, x: int, y: int, game: CellAutoGame):
    match type:
        case "bat":
            STATE.enemies.launch_bat(game, Coord.with_xy(x, y))
        case _:
            log_error(f"game_loop._process_launch_enemy unrecognised name {type}")

#
# Signals
#

def enemy_killed(game: CellAutoGame, other: float):
    bounty = other
    STATE.score_counter += bounty
    UI.life_meter.set_percentage(STATE.health_percentage)

def enemy_attacks(game: CellAutoGame, other: float):
    percentage = STATE.health_percentage
    if percentage <= 0:
        # Important: we don't trigger game over as soon as the health % == 0
        # Once it hits zero the player still has one more chance to survive.
        # It is only the first attack below zero that causes game over
        update_queue.append(_Update("game_over"))
        return
    
    damage = other
    STATE.score_counter -= damage
    print(f"game_loop.enemy_attacks() damage:{damage} score:{STATE.score_counter}")

    UI.life_meter.set_percentage(STATE.health_percentage)

def enemy_spawns_enemy(sender, other):
    name: str = sender
    x: int = other[0]
    y: int = other[1]
    update_queue.append(_Update("launch_enemy", (name, x, y)))

def weapon_deactivate_at_location(sender):
    location_id = sender
    update_queue.append(_Update("deactivate_weapon", location_id))

def ui_title_screen_selected(sender):
    update_queue.append(_Update("ui_display_title_screen"))

def ui_game_start_selected(sender):
    update_queue.append(_Update("ui_fade_from_title_to_game"))

def ui_title_screen_fade_out_complete(sender):
    update_queue.append(_Update("load_level"))

def ui_game_screen_fade_in_complete(sender):
    STATE.start()
    UI.state_to("select_location")
    UI.life_meter.set_percentage(STATE.health_percentage)

    if DEBUG_TRIGGER_POWER_UP:
        update_queue.append(_Update("ui_display_power_up"))

def ui_weapon_selected(type: str):
    # The order is important - hide_weapon_ui clears STATE.launch_location
    # which is required by launch_weapon
    update_queue.append(_Update("launch_weapon", type))
    update_queue.append(_Update("hide_weapon_ui"))

def ui_game_over_fade_out_complete(sender):
    update_queue.append(_Update("ui_display_game_over_screen"))

def ui_game_over_restart_selected(sender):
    update_queue.append(_Update("ui_hide_game_over_screen"))
    update_queue.append(_Update("ui_display_title_screen"))