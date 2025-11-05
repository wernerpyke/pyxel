from dataclasses import dataclass
from pyke_pyxel.base_types import Coord
from pyke_pyxel.field_game import FieldGame
from game_state import STATE

from . import weapon_select

def mouse_move(game: FieldGame, other: tuple[int, int]):
    # print(f"MOVE x:{other[0]} y:{other[1]}")
    if STATE.ui_state == "select_location":
        location = STATE.map.launch_location_at(other[0], other[1])
        if location:
            if STATE.launch_location and STATE.launch_location.name == location.name:
                return # Current location
            
            STATE.launch_location = location 

            # Mark the location
            marker = STATE.ui_marker_sprite
            marker.set_position(Coord.with_center(
                location.position.mid_x, 
                location.position.mid_y, 
                size=16))
            game.add_sprite(marker)
            
        else:
            STATE.launch_location = None # Clear the location
            game.remove_sprite(STATE.ui_marker_sprite)


def mouse_down(game: FieldGame, other: tuple[int, int]):
    match STATE.ui_state:
        case "select_location":
            if STATE.launch_location:
                weapon_select.display(game)
                STATE.ui_state = "select_weapon"
        case "select_weapon":
            if not weapon_select.mouse_down(other[0], other[1]):
                hide_weapons_ui(game)

def mouse_up(game: FieldGame):
    match STATE.ui_state:
        case "select_location":
            pass
        case "select_weapon":
            weapon_select.mouse_up()

def hide_weapons_ui(game: FieldGame):
    weapon_select.hide(game)
    STATE.launch_location = None
    game.remove_sprite(STATE.ui_marker_sprite)
    STATE.ui_state = "select_location"