import sys
import time

from pyinstrument import Profiler

from pyke_pyxel.cell_auto.game import CellAutoGame
from pyke_pyxel.settings import GameSettings

RUN_MINUTES = 0.5

class ProfileGame(CellAutoGame):

    def __init__(self, settings: GameSettings, title: str, resources: str):
        super().__init__(settings, title, resources)
        self._profiler = Profiler()
        self._profiler.start()
        self._count = 0

    def start(self):
        super().start()

    def update(self):
        # time.sleep(0.0001)  # Simulate a small delay
        super().update()

    def draw(self):
        super().draw()
        self._profile()
        
    def _profile(self):
        self._count += 1
        if self._profiler.is_running and self._count >= (RUN_MINUTES * 60 * 60): # Assumes 60 FPS
            self._profiler.stop()
            self._profiler.print(time='percent_of_total')
            sys.exit(0)