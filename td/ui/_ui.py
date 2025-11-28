from pathlib import Path

from pyke_pyxel import Coord, GameSettings, log_error
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import Sprite, TextSprite
from pyke_pyxel.drawable import Button

from td.state import STATE
from td.state.weapons import WeaponLocation

from .life_meter import LifeMeter
from . import title_screen
from . import weapon_select
from . import game_over_screen
from . import power_up

class _UI:

    def __init__(self):
        self._state: str = ""
        self.marker_sprite = Sprite("location_marker", Coord(5, 10), col_tile_count=2, row_tile_count=2)
        self.life_meter = LifeMeter()
        self.timer_text = TextSprite("", 
                            GameSettings.get().colours.hud_text,
                            f"{Path(__file__).parent.resolve()}/../assets/t0-14b-uni.bdf")
        
        self.pause_button = Button("pause", 
                                   up_frame=Coord(27, 3), 
                                   down_frame=Coord(25, 3), 
                                   col_tile_count=2, 
                                   row_tile_count=2, 
                                   resource_image_index=1)
    
    def show_title_screen(self, game: Game):
        title_screen.display(game)
        self.state_to( "select_title_option")

    def hide_title_screen(self, game: Game):
        title_screen.hide(game)

    def load_hud(self, game: Game):
        text = self.timer_text
        text.set_text("00:00")
        text.set_position(Coord(2,2))
        game.hud.add_text(text)

        pause = self.pause_button
        pause.set_position(Coord(38, 2))
        game.hud.add_button(pause)
        
        self.life_meter._sprite.set_position(Coord(12, 1))
        game.hud.add_sprite(self.life_meter._sprite)

    def hide_weapons_ui(self, game: Game):
        weapon_select.hide(game)
        STATE.weapons.selected_location = None
        game.hud.remove_sprite(self.marker_sprite)
        self.state_to("select_location")

    def show_game_over_screen(self, game: Game):
        game_over_screen.display(game)
        self.state_to("select_game_over_option")
    
    def hide_game_over_screen(self, game: Game):
        game_over_screen.hide(game)

    def show_power_up(self, game: Game):
        power_up.display(game)
        self.state_to("select_power_up")

    def set_weapon_marker(self, name: str, location: WeaponLocation, game: Game):
        if location.marker:
            game.hud.remove_sprite(location.marker)

        match name:
            case "star":
                frame = Coord(8, 11)
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

    def remove_weapon_marker(self, location: WeaponLocation, game: Game):
        if location.marker:
            game.hud.remove_sprite(location.marker)
            location.marker = None

    def state_to(self, state):
        self._state = state

    def state_to_waiting(self):
        self._state = "wait"

    def state_is_waiting(self):
        return self._state == "wait" or self._state == "select_title_option" or self._state == "select_game_over_option" or self._state == "select_power_up"

UI = _UI()

