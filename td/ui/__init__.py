from pathlib import Path

from pyke_pyxel import Coord, GameSettings, log_error
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import Sprite, TextSprite

from td.state import STATE
from td.state.weapons import WeaponLocation

from .life_meter import LifeMeter
from . import title_screen
from . import weapon_select

class UI:
    _instance = None

    def __init__(self):
        self.state: str = ""
        self.marker_sprite = Sprite("location_marker", Coord(5, 10), col_tile_count=2, row_tile_count=2)
        self.life_meter = LifeMeter()
        self.score_text = TextSprite("*", 
                            GameSettings.get().colours.hud_text,
                            f"{Path(__file__).parent.resolve()}/../assets/t0-14b-uni.bdf")

    @classmethod
    def get(cls) -> "UI":
        # return _global_ui_instance
        if not cls._instance:
            cls._instance = UI()
        return cls._instance
    
    def show_title_screen(self, game: Game):
        title_screen.display(game)
        self.state = "select_title_screen_option"

    def hide_title_screen(self, game: Game):
        title_screen.hide(game)

    def show_life_meter(self, game: Game):
        self.life_meter.show(game)

    def hide_weapons_ui(self, game: Game):
        weapon_select.hide(game)
        STATE.weapons.selected_location = None
        game.hud.remove_sprite(self.marker_sprite)
        self.state = "select_location"

    def set_weapon_marker(self, name: str, location: WeaponLocation, game: Game):
        if location.marker:
            game.hud.remove_sprite(location.marker)

        match name:
            case "bolt":
                frame = Coord(7, 10)
            case "fungus":
                frame = Coord(8, 10)
            case "meteor":
                frame = Coord(7, 11)
            case _:
                log_error(f"ui.set_weapon_marker invalid weapon:{name}")
                return

        location.marker = Sprite(f"{name}_marker", frame)
        location.marker.set_position(location.position) # .clone_by(0, -8))
        game.hud.add_sprite(location.marker)
        
# _global_ui_instance = UI()

# Signals

def mouse_move(game: Game, other: tuple[int, int]):
    # print(f"MOVE x:{other[0]} y:{other[1]}")
    x, y = other[0], other[1]
    ui = UI.get()
    match ui.state:
        case "select_title_screen_option":
            title_screen.mouse_move(x, y)
        case "select_location":
            weapons = STATE.weapons
            location = weapons.location_at(x, y)
            if location:
                if weapons.selected_location and weapons.selected_location.name == location.name:
                    return # Current location
                
                weapons.selected_location = location 

                # Mark the location
                marker = ui.marker_sprite
                marker.set_position(Coord.with_center(
                    location.position.mid_x, 
                    location.position.mid_y, 
                    size=16))
                game.hud.add_sprite(marker)
                
            else:
                weapons.selected_location = None # Clear the location
                game.hud.remove_sprite(ui.marker_sprite)
        case "select_weapon":
            weapon_select.mouse_move(x, y)


def mouse_down(game: Game, other: tuple[int, int]):
    x, y = other[0], other[1]
    ui = UI.get()
    match ui.state:
        case "select_title_screen_option":
            title_screen.mouse_down(x, y)
        case "select_location":
            if STATE.weapons.selected_location:
                weapon_select.display(game)
                ui.state = "select_weapon"
        case "select_weapon":
            if not weapon_select.mouse_down(x, y):
                ui.hide_weapons_ui(game)

def mouse_up(game: Game):
    match UI.get().state:
        case "select_title_screen_option":
            title_screen.mouse_up()
        case "select_location":
            pass
        case "select_weapon":
            weapon_select.mouse_up()
