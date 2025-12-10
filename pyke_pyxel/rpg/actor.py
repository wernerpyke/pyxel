from typing import Callable

from pyke_pyxel import GameSettings, DIRECTION, coord, log_debug
from pyke_pyxel.sprite import Sprite, MovableSprite
from pyke_pyxel.signals import Signals
from pyke_pyxel.map import Map

from ._projectile import Projectile

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
        
        Signals.send_add_sprite(sprite)

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

    def __init__(self, sprite: MovableSprite, speed_px_per_second: int):
        """
        Args:
            sprite (MovableSprite): the sprite that represents this actor
            speed_px_per_second (int): The speed of the actor's movements expressed as pixels per second
        """
        super().__init__(sprite)

        self._px_per_frame: float = speed_px_per_second / GameSettings.get().fps.game
        self._px_counter = 0
        self._move_to: coord|None = None
        self._blocked_by: coord|None = None

        self.active_dir: DIRECTION|None = None
        self.facing_dir: DIRECTION = DIRECTION.DOWN

    def set_position(self, position: coord):
        """Set the position of the actor"""
        self._sprite.set_position(position)

    def start_moving(self, direction: DIRECTION):
        """Start moving in the provided direction"""
        # self._is_moving = True

        if (self.active_dir == direction) and self._sprite.is_animating:
            return

        self._sprite.activate_animation(direction.value)
        self.active_dir = direction
        self.facing_dir = direction

        self._px_counter = 0

    def stop_moving(self):
        """Stop moving"""
        self._sprite.deactivate_animations()
        self.active_dir = None
        self._px_counter = 0
        # self._is_moving = False

    def move_to(self, position: coord):
        self._move_to = position
        self.active_dir = None
        self._px_counter = 0

    @property
    def is_moving(self) -> bool:
        """Return True if the actor is moving"""
        return self.active_dir is not None

    def _update(self, map: Map):
        # if self._is_moving:
        if self.active_dir or self._move_to:
            if self._move(map):
                pass
                # TODO - if, in future we want to send this signal
                # Then Player._move and Enemy._move should return False
                # and generate its own signals
                # Signals.send(Signals.ACTOR.MOVED, self)
        super()._update(map)

    def _move(self, map: Map) -> bool:
        # IMPORTANT: _move() is called once per frame
        self._px_counter += self._px_per_frame
        if self._px_counter < 1:
            return True
        self._px_counter = 0

        distance = round(self._px_per_frame) if self._px_per_frame > 1 else 1

        sprite = self._sprite

        next_pos: coord
        if direction := self.active_dir:
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
            
            next_pos = sprite.position.clone_by(by_x, by_y, direction)
        elif self._move_to:
            next_pos = sprite.position.clone_towards(self._move_to, distance)
            if next_pos.is_same_grid_location(self._move_to):
                self._move_to = None
        else:
            return False
        
        if map.sprite_can_move_to(next_pos):
            sprite.set_position(next_pos)
            return True
        else:
            self._blocked_by = next_pos
            return False
