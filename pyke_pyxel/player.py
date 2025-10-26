from typing import Optional

from .actor import MovableActor
from .signals import Signals, DIRECTION
from .sprite import Sprite, OpenableSprite, MovableSprite
from .map import Map, Coord

class Player(MovableActor):
    def __init__(self, sprite: MovableSprite):
        super().__init__(sprite)
        self._canOpenSprite: Optional[OpenableSprite] = None

    def move(self, direction: str, map: Map):
        
        if not super().move(direction, map):
            if map.is_openable(self._moveTo):
                self._canOpenSprite = map.openable_sprite_at(self._moveTo)

            sprite = map.sprite_at(self._moveTo)
            if sprite:
                Signals.send(Signals.PLAYER.BLOCKED, sprite)

    def interact(self, map: Map):
        openable = self._canOpenSprite if self._canOpenSprite else map.adjacent_openable(self._sprite.position)

        if openable:
            Signals.send(Signals.PLAYER.INTERACT_OPENABLE, openable)
            if openable.is_closed:
                map.mark_closed(openable.position)
            else:
                map.mark_open(openable.position)
                
        # There is an interesting side effect here whereby, because once you open a door we set self._canOpenSprite = None
        # and map.adjacent_openable() only finds doors around you, you cannot close a door while standing on top of it.
        # Closing a door while standing on top of it would cause a bug, trapping the player
        self._canOpenSprite = None