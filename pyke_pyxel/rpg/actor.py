from typing import Callable

from pyke_pyxel import GameSettings, DIRECTION, coord, log_debug
from pyke_pyxel.sprite import Sprite, MovableSprite
from pyke_pyxel.signals import Signals
from pyke_pyxel.map import Map

from .projectile import Projectile

class Actor:

    def __init__(self, sprite: Sprite):
        self._id: int = 0
        self._sprite = sprite

        self._projectiles: list[Projectile] = []

    def __eq__(self, other):
        return isinstance(other, Actor) and self._id == other._id

    def launch_projectile(self, sprite_type: Callable[[], Sprite], speed_px_per_second: int, direction: DIRECTION):
        sprite = sprite_type()
        
        d_x = 0
        d_y = 0
        tile_size = round(GameSettings.get().size.tile * 0.5)
        match direction:
            case DIRECTION.UP:
                d_y = tile_size * -1
            case DIRECTION.DOWN:
                d_y = tile_size
            case DIRECTION.LEFT:
                d_x = tile_size * -1
            case DIRECTION.RIGHT:
                d_x = tile_size

        pos = self._sprite.position
        sprite.set_position(coord.with_xy(pos.x + d_x, pos.y + d_y))
        
        projectile = Projectile(sprite, speed_px_per_second, direction)
        self._projectiles.append(projectile)
        
        Signals._sprite_added(sprite)

    def _update(self, map: Map):
        for projectile in self._projectiles:
            if projectile._update(map) == False:
                log_debug("Actor.update() removing projectile")
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

        self._px_per_frame: float = sprite.speed_px_per_second / GameSettings.get().fps.game
        self._px_counter = 0
        self._is_moving = False
        self._move_to: coord

        # log_debug(f"MovableActor({sprite.name}) frames_per_pixel:{self._frames_per_pixel}")

        self.current_direction: DIRECTION = DIRECTION.DOWN

    def set_position(self, col: int, row: int):
        """Set the position of the actor"""
        self._sprite.set_position(coord(col, row))

    def start_moving(self, direction: DIRECTION):
        """Start moving in the provided direction"""
        self._is_moving = True

        if self.current_direction == direction:
            return

        self._sprite.activate_animation(direction.value)
        self.current_direction = direction
        self._px_counter = 0

    def stop_moving(self):
        """Stop moving"""
        self._sprite.deactivate_animations()
        self._px_counter = 0
        self._is_moving = False

    def _update(self, map: Map):
        if self._is_moving:
            self._move(map)
        super()._update(map)

    def _move(self, map: Map):
        # IMPORTANT: _move() is called once per frame
        self._px_counter += self._px_per_frame
        if self._px_counter < 1:
            return True
        self._px_counter = 0

        distance = round(self._px_per_frame) if self._px_per_frame > 1 else 1

        direction = self.current_direction
        sprite = self._sprite
        by_x = 0
        by_y = 0
        match direction:
            case DIRECTION.UP:
                by_y = distance * -1
            case DIRECTION.DOWN:
                by_y = distance
            case DIRECTION.LEFT:
                by_x = distance * -1
            case DIRECTION.RIGHT:
                by_x = distance
        
        self._move_to = sprite.position.clone_by(by_x, by_y, direction)
        if map.sprite_can_move_to(self._move_to):
            sprite.set_position(self._move_to)
            return True
        else:
            return False
