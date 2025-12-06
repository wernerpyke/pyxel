from dataclasses import dataclass
from typing import Callable, Optional, Any
from blinker import signal

class Signals:
    """
    Signal management system for game events.
    This class provides a centralized signal dispatching mechanism for various game events,
    organizing signals into categories (GAME, MOUSE) and providing methods
    to connect listeners and send signals with optional parameters.
    
    Attributes:
        GAME: Dataclass containing game-level signal constants
            - WILL_START: Signal emitted before game initialization, Game instance is passed as the sender
            - UPDATE: Signal emitted on each game update cycle, Game instance is passed as the sender
        MOUSE: Dataclass containing mouse input signal constants
            - DOWN: Signal emitted on mouse button down, Game instance and a tuple (x, y) is passed
            - UP: Signal emitted on mouse button up
            - MOVE: Signal emitted on mouse movement, Game instance and a tuple (x, y) is passed
        
    RPG-Specific Attributes:   
        PLAYER: Dataclass containing player-related signal constants
            - BLOCKED: Signal emitted when player movement is blocked
            - INTERACT_OPENABLE: Signal emitted when player can interact with openable objects
            - ATTACK: Signal emitted when player performs an attack action
        ENEMY: Dataclass containing enemy-related signal constants
            - BLOCKED: Signal emitted when enemy movement is blocked
    """

    @dataclass
    class GAME:
        WILL_START = "game_will_start"
        UPDATE = "game_update"

    @dataclass
    class MOUSE:
        DOWN = "mouse_down"
        UP = "mouse_up"
        MOVE = "mouse_move"

    # TODO - the below are RPG-specific signals, move them
    @dataclass
    class PLAYER:
        BLOCKED = "player_blocked"
        INTERACT_OPENABLE = "player_interact_openable"
        ATTACK = "attack"

    @dataclass
    class ENEMY:
        BLOCKED = "enemy_blocked"

    @staticmethod
    def connect(name: str, listener: Callable):
        """Connect a listener callback to a named signal"""
        signal(name).connect(listener)

    @staticmethod
    def disconnect(name: str, listener: Callable):
        """Disconnect a listener callback from a named signal"""
        signal(name).disconnect(listener)

    @staticmethod
    def send(name: str, sender: Any|None = None):
        """
        Send a signal with an optional sender object

        Args:
            sender (Any): The object sending the signal.
        """
        signal(name).send(sender)

    @staticmethod
    def send_with(name: str, sender: Any, value: Any):
        """
        Send a signal with additional data/parameter value

        Args:
            sender (Any): The object sending the signal.
            value (Any): The additional data/parameter value
        """
        signal(name).send(sender, value=value)


    # TODO - the below are RPG-specific, move them
    
    @staticmethod
    def _sprite_added(sprite):
        signal("sprite_added").send(sprite)

    @staticmethod
    def _sprite_removed(sprite):
        signal("sprite_removed").send(sprite)

    # TODO - the below are RPG-specific signals, move them
    @staticmethod
    def _enemy_added(sprite):
        signal("enemy_added").send(sprite)

    @staticmethod
    def _enemy_removed(sprite):
        signal("enemy_removed").send(sprite)

