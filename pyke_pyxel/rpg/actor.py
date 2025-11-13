from dataclasses import dataclass
from typing import Optional, Callable

from ..signals import Signals
from .projectile import Projectile
from ..sprite import Sprite, MovableSprite
from ..map import Map

from .. import DIRECTION, Coord, log_debug

class Actor:

    def __init__(self, sprite: Sprite):
        self._id: int = 0
        self._sprite = sprite

        self._projectiles: list[Projectile] = []

    def __eq__(self, other):
        return isinstance(other, Actor) and self._id == other._id

    def launch_projectile(self, spriteType: Callable[[], Sprite], movementSpeed: int, direction: str):
        sprite = spriteType()
        
        match direction:
            case DIRECTION.UP:
                sprite.set_position(self._sprite.position.clone_by(0, -4, direction))
            case DIRECTION.DOWN:
                sprite.set_position(self._sprite.position.clone_by(0, 4, direction))
            case DIRECTION.LEFT:
                sprite.set_position(self._sprite.position.clone_by(-4, 0, direction))
            case DIRECTION.RIGHT:
                sprite.set_position(self._sprite.position.clone_by(4, 0, direction))
        
        projectile = Projectile(sprite, movementSpeed, direction)
        self._projectiles.append(projectile)
        
        Signals._sprite_added(sprite)

    def _update(self, map: Map, update_movement: bool):
        for projectile in self._projectiles:
            if projectile.update(map) == False:
                log_debug(f"Actor.update() removing projectile")
                self._projectiles.remove(projectile)

    @property 
    def name(self):
        return self._sprite.name
    
    @property
    def position(self):
        return self._sprite.position

class MovableActor(Actor):

    def __init__(self, sprite: MovableSprite):
        super().__init__(sprite)

        self._movementSpeed = sprite.movementSpeed
        self._moveTo: Coord

        self.currentDirection = DIRECTION.DOWN
        self._moveInDirection: Optional[str] = None

    def set_position(self, col: int, row: int):
        self._sprite.set_position(Coord(col, row))

    def start_moving(self, direction: str):
        self._moveInDirection = direction

    def stop_moving(self):
        self._moveInDirection = None
        self._sprite.deactivate_animations()

    def _update(self, map: Map, update_movement: bool):
        if self._moveInDirection and update_movement:
            self.move(self._moveInDirection, map)

        super()._update(map, update_movement)

    def move(self, direction: str, map: Map):
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
        
        self._moveTo = sprite.position.clone_by(byX, byY, direction)
        if map.sprite_can_move_to(self._moveTo):
            sprite.set_position(self._moveTo)
            return True
        else:
            return False
