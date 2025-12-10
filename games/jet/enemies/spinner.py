from pyke_pyxel import coord
from pyke_pyxel.map import Map
from pyke_pyxel.rpg.enemy import Enemy

import games.jet.sprites as sprites


class Spinner(Enemy):

    def __init__(self):
        sprite = sprites.spinner()

        super().__init__(sprite, 50)

        sprite.activate_animation("up")

    def _update(self, map: Map):


        return super()._update(map)