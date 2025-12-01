from pyke_pyxel import coord, COLOURS, log_error
from pyke_pyxel.drawable import Image, Rect, Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import CompoundSprite
from td.state import STATE
from td.state.stats import STATS, WeaponPowerUp
from ._text import HUD_font

image = Image(coord(1, 19), cols=20, rows=3, image_index=1)
image.set_position(coord(10, 7))

bg = Rect(position=coord(8, 6), col_count=24, row_count=30)
bg.set_background(COLOURS.BLACK)
bg.set_border(COLOURS.BLUE_DARK, 2)

# We have to keep a reference to game to be able to unpause it prior to sending the Signal. 
# Otherwise update_queue_item will not be processed
_game = []

up_sprite = CompoundSprite(f"up", cols=22, rows=4)
up_sprite.fill(tile_cols=[10, 11], tile_rows=[9, 10, 11, 12])
up_sprite.fill_col(col=1, tile_col=9, tile_rows=[9, 10, 11, 12]) # left cap
up_sprite.fill_col(col=22, tile_col=12, tile_rows=[9, 10, 11, 12]) # right cap

down_sprite = CompoundSprite(f"down", cols=24, rows=4)
down_sprite.fill(tile_cols=[14, 15], tile_rows=[9, 10, 11, 12])
down_sprite.fill_col(col=1, tile_col=13, tile_rows=[9, 10, 11, 12]) # left cap
down_sprite.fill_col(col=22, tile_col=16, tile_rows=[9, 10, 11, 12]) # right cap

buttons: list[Button] = []
power_ups: list[tuple[str,WeaponPowerUp]] = []

def _show_options(game: Game):
    _game.append(game)

    buttons.clear()
    power_ups.clear()

    game.hud.add_bg(bg)
    game.hud.add_bg(image)

    row_index = 11
    ups = STATE.weapons.available_power_ups()
    for up in ups:
        print(f"POWER UP {up.weapon_type} {up.type} {up.value} {up.count}")

        button = _make_button(up)
        button.set_position(coord(9, row_index))

        power_ups.append((button.name, up))

        game.hud.add_button(button)
        row_index += 6

def _make_button(up: WeaponPowerUp):
    button = Button(f"{up.weapon_type}_{up.type}", up_sprite, down_sprite)

    up_icon = Image(coord(1, 13), cols=4, rows=4)
    down_icon = Image(coord(5, 13), cols=4, rows=4)
    
    up_icon: Image
    down_icon: Image
    match up.weapon_type:
        case "bolt":
            up_icon = Image(coord(1, 13), cols=4, rows=4)
            down_icon = Image(coord(5, 13), cols=4, rows=4)
        case "fungus":
            up_icon = Image(coord(9, 13), cols=4, rows=4)
            down_icon = Image(coord(13, 13), cols=4, rows=4)
        case "meteor":
            up_icon = Image(coord(17, 13), cols=4, rows=4)
            down_icon = Image(coord(21, 13), cols=4, rows=4)
        case "star":
            up_icon = Image(coord(25, 13), cols=4, rows=4)
            down_icon = Image(coord(29, 13), cols=4, rows=4)
    button.set_icon(up_icon, down_icon)

    button.set_text(text=make_up_label(up), 
                    font=HUD_font(), 
                    colour=COLOURS.WHITE, 
                    alignment="left", 
                    highlight_colour=COLOURS.GREEN)

    buttons.append(button)
    return button

def make_up_label(up: WeaponPowerUp):
    indicator = "+" if up.increases else "-"
    value = round(up.value * 100)
    return f"{up.type.capitalize()} {indicator}{value}%"

def display(game: Game):
    def intro_complete(sender):
        game.pause()
        Signals.disconnect("ui_power_up_intro_complete", intro_complete)
        _show_options(game)

    Signals.connect("ui_power_up_intro_complete", intro_complete)
    game.fx.scale_in(image, duration=0.3, completion_signal="ui_power_up_intro_complete")

def hide(game: Game):
    game.hud.remove_bg(image)
    game.hud.remove_bg(bg)
    for b in buttons:
        game.hud.remove_button(b)
    
    buttons.clear()
    power_ups.clear()

def mouse_down(x: int, y: int):
    for b in buttons:
        if b.contains(x, y):
            b.push_down()
            return

def mouse_up():
    for b in buttons:
        if b.is_down:
            b.pop_up()

            for u in power_ups:
                if b.name == u[0]:
                    up = u[1]
                    STATS.increment_weapon_power_up(up.weapon_type, up.type)
                    STATE.score_counter = 0
                    break
            
            _game[0].unpause()
            _game.clear()

            Signals.send("ui_power_up_selected", b.name)
            return

def mouse_move(x: int, y: int):
    for b in buttons:
        b.check_mouse_move(x, y)