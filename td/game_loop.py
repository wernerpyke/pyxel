from dataclasses import dataclass
from pyke_pyxel import COLOURS, log_error
from pyke_pyxel.button import Button
from pyke_pyxel.cell_field import CellField, Cell
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame


import weapons
import enemies
import ui
from game_state import STATE
from game_load import load_level

update_queue: list[str] = []

def game_started(game: FieldGame):
    if STATE.music_enabled:
        game.start_music(0)

    ui.show_title_screen(game)

def game_update(game: FieldGame):
    _process_update_queue(game)

    if STATE.ui_state == "select_title_screen_option": # TODO - this is not super robust
        return
    
    enemies.update(game)
    weapons.update(game.field)

def _process_update_queue(game):
    for u in update_queue:
        match u:
            case "load_level":
                ui.hide_title_screen(game)
                load_level(game)
            case "hide_weapon_ui":
                ui.hide_weapons_ui(game)
            case "launch_bolt":
                location = STATE.launch_location
                if location:
                    weapons.launch_bolt(location, game.field)
                else:
                    log_error("game_loop.game_update no launch location")
            case "launch_fungus":
                location = STATE.launch_location
                if location:
                    weapons.launch_fungus(
                        location.position, 
                        game.field)
                else:
                    log_error("game_loop.game_update no launch location")
            case "launch_meteor":
                location = STATE.launch_location
                if location:
                    weapons.launch_meteor(
                        location.position, 
                        game.field)
                else:
                    log_error("game_loop.game_update no launch location")
    update_queue.clear()

#
# Signals
#

def enemy_killed(game: FieldGame):
    STATE.score += 1
    text = STATE.score_text
    text.set_colour(COLOURS.GREEN_MINT)
    text.set_text(f"{STATE.score}")

def enemy_wins(game: FieldGame, other: int):
    damage = other
    # print(f"ENEMY SCORES damage:{damage}")
    STATE.score -= damage
    text = STATE.score_text
    text.set_colour(COLOURS.RED)
    text.set_text(f"{STATE.score}")

def ui_game_start_selected(sender):
    update_queue.append("load_level")

def ui_weapon_selected(name: str):
    # The order is important - hide_weapon_ui clears STATE.launch_location
    # which is required by launch_weapon
    update_queue.append(f"launch_{name}")
    update_queue.append("hide_weapon_ui")
    