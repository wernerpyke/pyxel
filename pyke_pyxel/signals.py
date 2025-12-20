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


    @staticmethod
    def send_add_sprite(sprite):
        """
        Globally-available signal to notify the game that a Sprite should been added to the game.
        This can be used as a loosely-coupled alternative to `Game.add_sprite`

        Args:
            sprite (Sprite | CompoundSprite ): The sprite to be added to the game.
        """
        signal("sprite_added").send(sprite)

    @staticmethod
    def send_remove_sprite(sprite):
        """
        Globally-available signal to notify the game that a Sprite should been removed from the game.
        This can be used as a loosely-coupled alternative to `Game.remove_sprite`

        Args:
            sprite (Sprite | CompoundSprite | int ): The sprite to be removed from the game. The sprite can be identifed by an int `sprite_id`
        """
        signal("sprite_removed").send(sprite)


    # TODO - the below are RPG-specific signals, move them
    @dataclass
    class PLAYER:
        MOVED = "player_moved"
        BLOCKED = "player_blocked"

    @dataclass
    class ENEMY:
        STOPPED = "enemy_stopped"
        BLOCKED = "enemy_blocked"
