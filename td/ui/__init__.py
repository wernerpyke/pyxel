from dataclasses import dataclass
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame

from td.state import STATE
from . import title_screen
from . import weapon_select

def mouse_move(game: FieldGame, other: tuple[int, int]):
    # print(f"MOVE x:{other[0]} y:{other[1]}")
    x, y = other[0], other[1]
    UI = STATE.ui
    match UI.state:
        case "select_title_screen_option":
            title_screen.mouse_move(x, y)
        case "select_location":
            map = STATE.map
            location = map.weapon_location_at(x, y)
            if location:
                if map.selected_location and map.selected_location.name == location.name:
                    return # Current location
                
                map.selected_location = location 

                # Mark the location
                marker = UI.marker_sprite
                marker.set_position(Coord.with_center(
                    location.position.mid_x, 
                    location.position.mid_y, 
                    size=16))
                game.add_sprite(marker)
                
            else:
                map.selected_location = None # Clear the location
                game.remove_sprite(UI.marker_sprite)
        case "select_weapon":
            weapon_select.mouse_move(x, y)


def mouse_down(game: FieldGame, other: tuple[int, int]):
    x, y = other[0], other[1]
    UI = STATE.ui
    match UI.state:
        case "select_title_screen_option":
            title_screen.mouse_down(x, y)
        case "select_location":
            if STATE.map.selected_location:
                weapon_select.display(game)
                UI.state = "select_weapon"
        case "select_weapon":
            if not weapon_select.mouse_down(x, y):
                hide_weapons_ui(game)

def mouse_up(game: FieldGame):
    match STATE.ui.state:
        case "select_title_screen_option":
            title_screen.mouse_up()
        case "select_location":
            pass
        case "select_weapon":
            weapon_select.mouse_up()

def show_title_screen(game: FieldGame):
    title_screen.display(game)

def hide_title_screen(game: FieldGame):
    title_screen.hide(game)

def hide_weapons_ui(game: FieldGame):
    weapon_select.hide(game)
    STATE.map.selected_location = None
    game.remove_sprite(STATE.ui.marker_sprite)
    STATE.ui.state = "select_location"