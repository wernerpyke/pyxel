from typing import Callable, Optional
import pyxel
import constants
from . import draw
from .objects.sprite import Sprite, OpenableSprite, Animation
from .objects.map import Map, Coord

class Player:
    def __init__(self, sprite: Sprite, movementSpeed: int):
        self._sprite = sprite
        self._movementSpeed = movementSpeed

        self._canOpenSprite: Optional[OpenableSprite] = None

    def set_position(self, col: int, row: int):
        self._sprite.position = Coord(col, row)

    def move(self, direction, doors: list[OpenableSprite], walls: list[Sprite]):
        sprite = self._sprite
        byX = 0
        byY = 0
        match direction:
            case "up":
                sprite.activate_animation("up")
                byY = self._movementSpeed * -1
            case "down":
                sprite.activate_animation("down")
                byY = self._movementSpeed
            case "left":
                sprite.activate_animation("left")
                byX = self._movementSpeed * -1
            case "right":
                sprite.activate_animation("right")
                byX = self._movementSpeed
        
        moveTo = sprite.position.clone_by(byX, byY)

        for door in doors:
            if door.is_closed and moveTo.collides_with(door.position):
                print(f"PLAYER.move() COLLIDES WITH CLOSED DOOR col:{door.position._col} row:{door.position._row}")
                self._canOpenSprite = door
                return

        #print(f"PLAYER.move() TO col:{moveTo._col} row:{moveTo._row} walls:{len(walls)}")
        for wall in walls:
            if moveTo.collides_with(wall.position):
                #print(f"PLAYER.move() COLLIDES WITH WALL col:{wall.position._col} row:{wall.position._row}")
                return
            
        sprite.move(byX, byY)


    def stop(self):
        self._sprite.deactivate_animations()

    def interact(self):
        if self._canOpenSprite:
            print(f"Player.interact() Opening {self._canOpenSprite.position._col} {self._canOpenSprite.position._row}")
            self._canOpenSprite.open()
            self._canOpenSprite = None

class Game:
    def __init__(self, title: str, spriteSheet: str):
        self._player: Player

        self.sprites: list[Sprite] = []
        self.spriteTick = 0

        self.walls: list[Sprite] = []
        self.doors: list[OpenableSprite] = []

        pyxel.init(constants.SIZE.WINDOW, constants.SIZE.WINDOW, fps=constants.FPS.GAME, title=title, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load(f"../{spriteSheet}")
        # pyxel.images[0].load(0, 0, "assets/pyxel_logo_38x16.png")
    
    def start(self):
        pyxel.run(self.update, self.draw)

    def add_wall_sprite(self, wallType: Callable[[], Sprite], col: int, row: int):
        sprite = wallType()
        self.add_sprite(sprite, col, row)
        self.walls.append(sprite)

    def add_door_sprite(self, doorType: Callable[[], OpenableSprite], col: int, row: int, closed: bool = True):
        sprite = doorType()
        self.add_sprite(sprite, col, row)
        sprite.close() if closed else sprite.open()

        self.doors.append(sprite)

    def add_player_sprite(self, 
                   idleFrame: Coord,
                   downAnimation: Animation,
                   upAnimation: Animation,
                   leftAnimation: Animation,
                   rightAnimation: Animation,
                   movementSpeed: int) -> Player:
        
        sprite = Sprite(idleFrame)
        sprite.add_animation("down", downAnimation)
        sprite.add_animation("up", upAnimation)
        sprite.add_animation("left", leftAnimation)
        sprite.add_animation("right", rightAnimation)

        self.player = Player(sprite, movementSpeed)
        self.sprites.append(sprite)
    
        return self.player
    
    def add_sprite(self, sprite: Sprite, col: int, row: int):
        sprite.position = Coord(col, row)
        self.sprites.append(sprite)
        

# ===== PYXEL =====

    def update(self):
        # Keyboard
        walls = Map.find_nearby(self.walls, self.player._sprite)

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player.interact()
        if pyxel.btn(pyxel.KEY_UP):
            self.player.move("up", self.doors, walls)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.player.move("down", self.doors, walls)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.player.move("left", self.doors, walls)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move("right", self.doors, walls)
        else:
            self.player.stop()


        # Animation
        if self.spriteTick < (constants.FPS.GAME / constants.FPS.ANIMATION):
            self.spriteTick += 1
        else:
            self.spriteTick = 0

    def draw(self):
        # Sprite Animations
        if self.spriteTick == 0:
            for sprite in self.sprites:
                sprite.update_frame()

        # Background
        draw.background()
        # pyxel.bltm(0, 0, 0, 0, 0, constants.SIZE.WINDOW, constants.SIZE.WINDOW)
        
        # Sprites
        for sprite in self.sprites:
            draw.sprite(sprite)

        pyxel.text(10, 6, "Hello, PYKE!", pyxel.frame_count % 16)
        