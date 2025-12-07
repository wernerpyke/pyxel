from pathlib import Path

from pyke_pyxel import coord, log_error, COLOURS
from pyke_pyxel.game import Game
from pyke_pyxel.sprite import Sprite, TextSprite
from pyke_pyxel.drawable import Button, ImageFactory, Image

from games.td.state import STATE
from games.td.state.weapons import WeaponLocation

from .life_meter import LifeMeter
from . import title_screen
from . import weapon_select
from . import game_over_screen
from . import power_up
from ._text import HUD_font

class _UI:

    def __init__(self):
        self._state: str = ""
        self.marker_sprite = Sprite("location_marker", coord(5, 10), cols=2, rows=2)
        self.life_meter = LifeMeter()
        self.timer_text = TextSprite("", 
                            COLOURS.WHITE,
                            HUD_font())
        
        img = ImageFactory(cols=2, rows=2, image_index=1)
        self.pause_button = Button("pause_button", img.at(coord(27, 3)), img.at(coord(25, 3)))
    
    def show_title_screen(self, game: Game):
        title_screen.display(game)
        self.state_to( "select_title_option")

    def hide_title_screen(self, game: Game):
        title_screen.hide(game)

    def load_hud(self, game: Game):
        text = self.timer_text
        text.set_text("00:00")
        text.set_position(coord(2,2))
        game.hud.add_text(text)

        pause = self.pause_button
        pause.set_position(coord(38, 2))
        game.hud.add_button(pause)
        
        self.life_meter._sprite.set_position(coord(12, 1))
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

    def hide_power_up(self, game: Game):
        power_up.hide(game)
        self.state_to("select_location")

    def set_weapon_marker(self, name: str, location: WeaponLocation, game: Game):
        if location.marker:
            game.hud.remove_sprite(location.marker)

        match name:
            case "star":
                frame = coord(8, 11)
            case "bolt":
                frame = coord(7, 10)
            case "fungus":
                frame = coord(8, 10)
            case "meteor":
                frame = coord(7, 11)
            case _:
                log_error(f"ui.set_weapon_marker invalid weapon:{name}")
                return

        location.marker = Sprite(f"{name}_marker", frame)
        location.marker.set_position(location.position) # .clone_by(0, -8))
        game.add_sprite(location.marker)

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

