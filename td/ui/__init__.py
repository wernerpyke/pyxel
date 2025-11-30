from pyke_pyxel import coord
from pyke_pyxel.game import Game

from td.state import STATE

from ._ui import _UI
from . import title_screen
from . import weapon_select
from . import game_over_screen
from . import power_up


UI = _UI()

# Signals

def mouse_move(game: Game, other: tuple[int, int]):
    # print(f"MOVE x:{other[0]} y:{other[1]}")
    x, y = other[0], other[1]
    match UI._state:
        case "select_title_option":
            title_screen.mouse_move(x, y)
        case "select_location":
            if game.is_paused:
                return

            weapons = STATE.weapons
            location = weapons.location_at(x, y)
            if location:
                if weapons.selected_location and weapons.selected_location.id == location.id:
                    return # Current location
                
                weapons.selected_location = location 
                
                # Mark the location
                marker = UI.marker_sprite
                marker.set_position(coord.with_center(
                    location.position.mid_x, 
                    location.position.mid_y, 
                    size=16))
                game.hud.add_sprite(marker)
                
            else:
                weapons.selected_location = None # Clear the location
                game.hud.remove_sprite(UI.marker_sprite)

        case "select_weapon":
            weapon_select.mouse_move(x, y)
        case "select_power_up":
            power_up.mouse_move(x, y)
        case "select_game_over_option":
            game_over_screen.mouse_move(x, y)


def mouse_down(game: Game, other: tuple[int, int]):
    x, y = other[0], other[1]
    match UI._state:
        case "select_title_option":
            title_screen.mouse_down(x, y)
        case "select_location":
            pause = UI.pause_button
            if pause.contains(x, y):
                if pause.is_down:
                    pause.pop_up()
                    game.unpause()
                    STATE.unpause()
                else:
                    pause.push_down()
                    game.pause()
                    STATE.pause()
            elif not game.is_paused and STATE.weapons.selected_location:
                weapon_select.display(game)
                UI.state_to("select_weapon")
        case "select_weapon":
            if not weapon_select.mouse_down(x, y):
                UI.hide_weapons_ui(game)
        case "select_power_up":
            power_up.mouse_down(x, y)
        case "select_game_over_option":
            game_over_screen.mouse_down(x, y)

def mouse_up(game: Game):
    match UI._state:
        case "select_title_option":
            title_screen.mouse_up()
        case "select_location":
            pass
        case "select_weapon":
            weapon_select.mouse_up()
        case "select_power_up":
            power_up.mouse_up()
        case "select_game_over_option":
            game_over_screen.mouse_up()

__all__ = [
    "UI",
    "mouse_move",
    "mouse_down",
    "mouse_up"
]