from dataclasses import dataclass
from pathlib import Path

import pyxel

from pyke_pyxel import GameSettings, COLOURS, coord
from pyke_pyxel.game import Game
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite, TextSprite, AnimationFactory


# Game State

@dataclass
class _state:
    text_colour: int = 0 # COLOURS.BLACK
    destination: coord = coord(1, 1)

STATE = _state()

# Game settings and initialisation

settings = GameSettings()
settings.size.window = 160
settings.size.tile = 8
settings.mouse_enabled = True
settings.colours.background = COLOURS.BLUE
settings.colours.sprite_transparency = COLOURS.BEIGE

game = Game(settings, title="Hello, World", resources=f"{Path(__file__).parent.resolve()}/assets/resources.pyxres")

# Sprites

sprite = Sprite("skeleton", default_frame=coord(1,1))

anims = AnimationFactory(frames=2)

sprite.add_animation("down", anims.at(coord(2,1)))
sprite.add_animation("up", anims.at(coord(4,1)))
sprite.add_animation("right", anims.at(coord(6,1)))
sprite.add_animation("left", anims.at(coord(6,1), flip=True))

text = TextSprite("Click anywhere and then press 'Q'", STATE.text_colour)

# Mouse handler

def mouse_down(game: Game, value: tuple[int, int]):
    x, y = value[0], value[1]
    STATE.destination = coord.with_xy(x, y)
    text.set_text(f"Clicked {STATE.destination}")

Signals.connect(Signals.MOUSE.DOWN, mouse_down)

# Keyboard

def q_key_pressed(game: Game):
    map = game.map
    STATE.destination = coord.with_center(map.center_x, map.center_y)

    text.set_text("Click again")

Signals.connect("q_key_pressed", q_key_pressed)
game.keyboard.signal_for_key(pyxel.KEY_Q, "q_key_pressed")

# Game Start and Loop handlers

def game_start(game: Game):
    # Walker
    map = game.map
    position = coord.with_center(map.center_x, map.center_y)
    sprite.set_position(position)
    game.add_sprite(sprite)

    STATE.destination = position

    # Instructions
    text.set_position(coord(2, 2))
    game.hud.add_text(text)

def game_update(game: Game):
    # Update the walker position and animation
    pos = sprite.position
    dest = STATE.destination

    if not pos.is_at(dest):
        x = 0
        x_direction: str|None = None
        if pos.is_left_of(dest):
            x = 1
            x_direction = "right"
        elif pos.is_right_of(dest):
            x = -1
            x_direction = "left"

        y = 0
        y_direction: str|None = None
        if pos.is_above(dest):
            y = 1
            y_direction = "down"
        elif pos.is_below(dest):
            y = -1
            y_direction = "up"
        
        if x_direction:
            sprite.activate_animation(x_direction)
        elif y_direction: 
            sprite.activate_animation(y_direction)
        
        pos.move_by(x, y)
    else:
        sprite.deactivate_animations()


    # Update the colour of the instructions text
    STATE.text_colour += 1
    STATE.text_colour %= 16
    text.set_colour(STATE.text_colour)

Signals.connect(Signals.GAME.WILL_START, game_start)
Signals.connect(Signals.GAME.UPDATE, game_update)

game.start()