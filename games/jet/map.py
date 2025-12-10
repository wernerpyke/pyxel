from pyke_pyxel import coord
from pyke_pyxel.rpg import RPGGame, Player

import sprites

def add_house(game: RPGGame):
    house = sprites.house()
    
    game.room.add_wall(house, 20, 20)
    game.map.mark_open(coord(20,20))
    game.map.mark_open(coord(21,20))
    game.map.mark_open(coord(22,20))
    game.map.mark_open(coord(23,20))