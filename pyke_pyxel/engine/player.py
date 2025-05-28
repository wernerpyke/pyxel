from typing import Optional

from .actor import Actor
from .signals import Signals, DIRECTION
from .sprite import Sprite, OpenableSprite
from .map import Map, Coord

class Player(Actor):
    def __init__(self, sprite: Sprite, movementSpeed: int):
        super().__init__(sprite)
        self._movementSpeed = movementSpeed
        self.currentDirection = DIRECTION.DOWN
        self._canOpenSprite: Optional[OpenableSprite] = None

    def set_position(self, col: int, row: int):
        self._sprite.set_position(Coord(col, row))

    def move(self, direction, map: Map):
        sprite = self._sprite
        byX = 0
        byY = 0
        match direction:
            case DIRECTION.UP:
                sprite.activate_animation(direction)
                byY = self._movementSpeed * -1
                self.currentDirection = direction
            case DIRECTION.DOWN:
                sprite.activate_animation(direction)
                byY = self._movementSpeed
                self.currentDirection = direction
            case DIRECTION.LEFT:
                sprite.activate_animation(direction)
                byX = self._movementSpeed * -1
                self.currentDirection = direction
            case DIRECTION.RIGHT:
                sprite.activate_animation(direction)
                byX = self._movementSpeed
                self.currentDirection = direction
        
        moveTo = sprite.position.clone_by(byX, byY, direction)
        if map.sprite_can_move_to(moveTo):
            sprite.set_position(moveTo)
        else:
            if map.is_openable(moveTo):
                self._canOpenSprite = map.openable_sprite_at(moveTo)

            sprite = map.sprite_at(moveTo)
            if sprite:
                Signals.send(Signals.PLAYER.BLOCKED, sprite)

    def stop(self):
        self._sprite.deactivate_animations()

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