from .actor import MovableActor
from pyke_pyxel.signals import Signals
from pyke_pyxel.sprite import OpenableSprite, MovableSprite
from pyke_pyxel.map import Map

class Player(MovableActor):
    def __init__(self, sprite: MovableSprite):
        super().__init__(sprite)
        self._can_open_sprite: OpenableSprite|None = None

    def _move(self, map: Map):
        if super()._move(map):
            # Signals.send(Signals.PLAYER.MOVED, self)
            return True
        else:
            if map.is_openable(self._move_to):
                self._can_open_sprite = map.openable_sprite_at(self._move_to)

            Signals.send_with(Signals.PLAYER.BLOCKED, self, value=map.sprite_at(self._move_to))
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