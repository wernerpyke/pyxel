from dataclasses import dataclass
from typing import Optional

from .signals import Signals, DIRECTION
from .projectile import Projectile
from .sprite import Sprite, OpenableSprite
from .map import Map, Coord

class Actor:

    def __init__(self, sprite: Sprite):
        self._sprite = sprite

        self._projectiles: list[Projectile] = []

    def launch_projectile(self, sprite: Sprite, movementSpeed: int, direction: str):
        
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

    def update(self, map: Map):
        for projectile in self._projectiles:
            if projectile.update(map) == False:
                print(f"Actor.update() removing projectile")
                self._projectiles.remove(projectile)
