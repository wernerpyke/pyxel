from .actor import MovableActor
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import OpenableSprite, MovableSprite
from pyke_pyxel.map import Map

class Player(MovableActor):
    def __init__(self, sprite: MovableSprite, speed_px_per_second: int):
        """
        Args:
            sprite (MovableSprite): the sprite that represents the player
            speed_px_per_second (int): The speed of the player's movements expressed as pixels per second
        """
        super().__init__(sprite, speed_px_per_second)
        self._can_open_sprite: OpenableSprite|None = None

    def _move(self, map: Map) -> bool:
        if super()._move(map):
            Signals.send(Signals.PLAYER.MOVED, self)
            return True
        else:
            if to := self._blocked_by:
                if map.is_openable(to):
                    self._can_open_sprite = map.openable_sprite_at(to)

                Signals.send_with(Signals.PLAYER.BLOCKED, self, value=map.sprite_at(to))
            return False

    def adjacent_openable(self, map: Map) -> OpenableSprite|None:
        """
        Find an `OpenableSprite` adjacent to the player's current position
        """
        openable = self._can_open_sprite if self._can_open_sprite else map.adjacent_openable(self._sprite.position)        
        # There is an interesting side effect here whereby, because once you open a door we set self._can_open_sprite = None
        # and map.adjacent_openable() only finds doors around you, you cannot close a door while standing on top of it.
        # Closing a door while standing on top of it would cause a bug, trapping the player
        self._can_open_sprite = None
        return openable