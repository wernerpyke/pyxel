from pyke_pyxel import DIRECTION
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import Sprite
from pyke_pyxel.rpg import RPGGame, Player

import sprites

class _Player:

    def __init__(self) -> None:
        self.player: Player
        self.game: RPGGame
        self.trail: Sprite|None = None

        self.active_dir: DIRECTION|None = None
        self.second_dir: DIRECTION|None = None

    def start(self, game: RPGGame):
        self.game = game
        self.player = game.player

    # Enemies
    def check_enemies_to_attack(self):
        enemies = self.game.enemies_at(self.player.position)
        for e in enemies:
            print(f"ATTACK {e.name}")

    # Movement

    def check_input(self, key: int, direction: DIRECTION):
        keyboard = self.game.keyboard

        if self.active_dir: # Moving
            if self.active_dir == direction: # Check for release
                if not keyboard.is_down(key):
                    # print(f"RELEASED {direction}")
                    self.active_dir = self.second_dir
                    self.second_dir = None
            elif keyboard.was_pressed(key): # Check for press
                # print(f"SWITCHED to {direction} from {self.active_dir}")
                self.second_dir = self.active_dir
                self.active_dir = direction
        else: # Not moving
            if keyboard.was_pressed(key):
                # print(f"PRESSED {direction}")
                self.active_dir = direction

    def update_movement(self):
        player = self.player
        if self.active_dir:
            if not player.active_dir == self.active_dir:
                self._start_movement()
        else:
            self.stop_movement()

    def stop_movement(self):
        self.player.stop_moving()

        if trail := self.trail:
            self.player._sprite.unlink_sprite(trail)
            Signals.send_remove_sprite(trail)
            self.trail = None

        self.active_dir = None
        self.second_dir = None

    def _start_movement(self):
        player = self.player
        player.start_moving(self.active_dir) # type: ignore warning
        if trail:= self.trail:
            Signals.send_remove_sprite(trail)
        
        trail = sprites.trail(player)
        Signals.send_add_sprite(trail)
        player._sprite.link_sprite(trail)

        self.trail = trail

    @property
    def is_moving(self) -> bool:
        return self.active_dir is not None
    
    """
    def check_input_none(self, *keys: int):
        # TODO - this may no longer be necessary
        # Because of the order in which we call check_input()
        # There is an edge case in which, e.g. UP is released af
        #
        one_pressed = False
        keyboard = self.game.keyboard
        for key in keys:
            if keyboard.is_down(key):
                one_pressed = True
                break
        if not one_pressed:
            self.stop_movement()
    """

PLAYER = _Player()