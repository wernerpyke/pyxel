
from pyke_pyxel.signals import Signals

def _enemy_added(sprite):
    Signals.send("enemy_added", sprite)

def _enemy_removed(sprite):
    Signals.send("enemy_removed", sprite)