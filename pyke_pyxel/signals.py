from dataclasses import dataclass

from typing import Callable, Optional, Any
from blinker import signal

class Signals:
    
    @dataclass
    class GAME:
        STARTED = "game_started"
        UPDATE = "game_update"
        SPRITE_REMOVED = "sprite_removed"

    @dataclass
    class PLAYER:
        BLOCKED = "player_blocked"
        INTERACT_OPENABLE = "player_interact_openable"
        ATTACK = "attack"

    @dataclass
    class ENEMY:
        BLOCKED = "enemy_blocked"

    @dataclass
    class MOUSE:
        DOWN = "mouse_down"
        UP = "mouse_up"
        MOVE = "mouse_move"

    @staticmethod
    def connect(name: str, listener: Callable):
        signal(name).connect(listener)

    @staticmethod
    def send(name: str, sender):
        signal(name).send(sender)

    @staticmethod
    def send_with(name: str, sender, other: Optional[Any] = None):
        signal(name).send(sender, other=other)

    @staticmethod
    def _sprite_added(sprite):
        signal("sprite_added").send(sprite)

    @staticmethod
    def _sprite_removed(sprite):
        signal("sprite_removed").send(sprite)

    @staticmethod
    def _enemy_added(sprite):
        signal("enemy_added").send(sprite)

    @staticmethod
    def _enemy_removed(sprite):
        signal("enemy_removed").send(sprite)

