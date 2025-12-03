import random
from pyke_pyxel import GameSettings, log_debug, log_error
from pyke_pyxel import coord
from pyke_pyxel.cell_auto.matrix import Cell
from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.sprite import Anim, Sprite
from td.state.stats import STATS


class Enemy:
    def __init__(self, type: str, from_frame: coord, cols: int = 1, rows: int = 1, animation_frame_count:int = 2) -> None:
        self.type = type
        stats = STATS.enemy_stats(type)
        if not stats:
            log_error(f"Enemy() invalid type:{type}")
            return

        sprite = Sprite(type, from_frame, cols, rows)
        
        sprite.add_animation("loop", Anim(from_frame, animation_frame_count))
        sprite.activate_animation("loop")

        sprite.add_animation("kill", Anim(coord(5,9), 2, loop=False))
        sprite.add_animation("die", Anim(coord(7,9), 2, loop=False))
        self._sprite = sprite

        self.power = stats.power
        self._speed = stats.speed
        self.damage  = stats.damage
        self.bounty  = stats.bounty

        # Calculate the boundaries of the win condition
        game_w = game_h = GameSettings.get().size.window
        self._plants_top_y = game_h - 24
        
        win_base_w = (game_w - 64) / 2
        self._base_top = game_h - 90
        self._base_left = win_base_w + 4
        self._base_right = game_w - win_base_w - 4

    def launch(self, game: CellAutoGame, position: coord):
        # log_debug(f"Enemy.launch() {self._sprite._id} x:{position.x} y:{position.y}")
        position = coord.with_xy(position.x, position.y, self._sprite.width)

        self._sprite.set_position(position)
        game.add_sprite(self._sprite)

    def update(self, field_cells: list[Cell]) -> tuple[float, bool]: # 0: continue, -1: dies, 1: wins, 2: super wins
        if not self._should_skip_move():
            to = self._move_towards_target()
            self._sprite.position.move_by(to[0], to[1])
        
        was_hit = False
        if len(field_cells) > 0:
            # current_power = self.power
            for c in field_cells:
                if self.power > c.power:
                    self.power -= c.power
                    # TODO - there's a messy thing here, we're resetting a cell which may be in a weapon's active cells
                    # See Fungus.update(). Another possibility is to check if not c.can_propogate:
                    c.reset()
                    was_hit = True
                else:
                    c.power -= self.power
                    self.power = 0
            # if not self.power == current_power:
            #    print(f"Enemy.update({self}) lost:{(current_power - self.power)} remaining:{self.power}")
        if self.power <= 0:
            return (-1, False) # killed
        else:
            return (self._calculate_win(), was_hit)
    
    @property
    def position(self) -> coord:
        return self._sprite.position

    def __str__(self):
        return f"{self.type}{self._sprite._id}"

    def _move_towards_target(self) -> tuple[int, int]:
        return (0, 1) # straight down

    def _calculate_win(self) -> float:
        max_y = self._sprite.position.max_y
        if max_y < self._base_top:
            return 0 # No

        if max_y >= self._plants_top_y: # in plants
            return 1 # Yes

        mid_x = self._sprite.position.mid_x
        if mid_x >= self._base_left and mid_x <= self._base_right: # in base
            return 1.2 # Super Yes
        else:
            return 0 # No
        
    def _should_skip_move(self) -> bool:
        speed = self._speed
        if speed == 10:
            return False
        
        skip_frequency = (10 - speed) / 10
        return random.random() < skip_frequency