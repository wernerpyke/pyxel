
from pyke_pyxel import Coord, COLOURS
from pyke_pyxel.drawable import Image, Rect, CompoundButton, Button
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import CompoundSprite
from td.state import STATE
from td.state.stats import WeaponPowerUp

image = Image(Coord(1, 19), col_tile_count=20, row_tile_count=3, resource_image_index=1)
image.set_position(Coord(10, 7))

up_sprite = CompoundSprite(f"up", cols=22, rows=4)
up_sprite.fill(tile_cols=[10, 11], tile_rows=[9, 10, 11, 12])
up_sprite.fill_col(col=1, tile_col=9, tile_rows=[9, 10, 11, 12]) # left cap
up_sprite.fill_col(col=22, tile_col=12, tile_rows=[9, 10, 11, 12]) # right cap

down_sprite = CompoundSprite(f"down", cols=24, rows=4)
down_sprite.fill(tile_cols=[14, 15], tile_rows=[9, 10, 11, 12])
down_sprite.fill_col(col=1, tile_col=13, tile_rows=[9, 10, 11, 12]) # left cap
down_sprite.fill_col(col=22, tile_col=16, tile_rows=[9, 10, 11, 12]) # right cap

buttons: list[CompoundButton] = []

def _show_options(game: Game):
    buttons.clear()
    bg = Rect(position=Coord(8, 6), col_count=24, row_count=30)
    bg.set_background(COLOURS.BLACK)
    bg.set_border(COLOURS.BLUE_DARK, 2)
    game.hud.add_bg(bg)
    game.hud.add_bg(image)

    row_index = 11
    ups = STATE.weapons.available_power_ups()
    for up in ups:
        print(f"POWER UP {up._weapon_type} {up.type} {up.value} {up.count}")

        button = _make_button(up)
        button.set_position(Coord(9, row_index))

        game.hud.add_button(button)
        row_index += 6

def _make_button(up: WeaponPowerUp):
    button = CompoundButton(f"{up._weapon_type}_{up.type}", up_sprite, down_sprite)
    
    up_icon = CompoundSprite("up_icon", cols=4, rows=4)
    down_icon = CompoundSprite("down_icon", cols=4, rows=4)
    match up._weapon_type:
        case "bolt":
            up_icon.fill(tile_cols=[1,2,3,4], tile_rows=[13, 14, 15, 16])
            down_icon.fill(tile_cols=[5,6,7,8], tile_rows=[13, 14, 15, 16])
        case "fungus":
            up_icon.fill(tile_cols=[9,10,11,12], tile_rows=[13, 14, 15, 16])
            down_icon.fill(tile_cols=[13,14,15,16], tile_rows=[13, 14, 15, 16])
        case "meteor":
            up_icon.fill(tile_cols=[17,18,19,20], tile_rows=[13, 14, 15, 16])
            down_icon.fill(tile_cols=[21,22,23,24], tile_rows=[13, 14, 15, 16])
        case "star":
            up_icon.fill(tile_cols=[25,26,27,28], tile_rows=[13, 14, 15, 16])
            down_icon.fill(tile_cols=[29,30,31,32], tile_rows=[13, 14, 15, 16])
        
    button.set_icon(up_icon, down_icon)
    buttons.append(button)
    return button

def display(game: Game):
    def intro_complete(sender):
        game.pause()
        Signals.disconnect("ui_power_up_intro_complete", intro_complete)
        _show_options(game)

    Signals.connect("ui_power_up_intro_complete", intro_complete)
    game.fx.scale_in(image, duration=0.3, completion_signal="ui_power_up_intro_complete")

def mouse_down(x: int, y: int):
    for b in buttons:
        if b.contains(x, y):
            b.push_down()
            return

def mouse_up():
    for b in buttons:
        if b.is_down:
            b.pop_up()
            #    Signals.send("ui_game_start_selected", None)
            return

def mouse_move(x: int, y: int):
    for b in buttons:
        b.check_mouse_move(x, y)