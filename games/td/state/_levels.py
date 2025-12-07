from dataclasses import dataclass

from pyke_pyxel.math import RandomChoice

@dataclass
class _let:
    type: str
    probability: float

@dataclass
class _le:
    frequency: float
    max_count: int
    types: list[_let]

class EnemyLevel:
    def __init__(self) -> None:
        self._enemies: list[_le] = []
        self._choice = RandomChoice()

        self._enemies.append(_le( # 0
            frequency=2, 
            max_count=2, 
            types=[
                _let("skeleton", 1.0)
            ]))
        
        self._enemies.append(_le( # 1
            frequency=2, 
            max_count=3, 
            types=[
                _let("skeleton", 0.7),
                _let("mage", 0.3)
            ]))
        
        self._enemies.append(_le( # 2
            frequency=1.8, 
            max_count=5, 
            types=[
                _let("skeleton", 0.5),
                _let("mage", 0.4),
                _let("orb", 0.1)
            ]))
        
        self._enemies.append(_le( # 3
            frequency=1.5, 
            max_count=6, 
            types=[
                _let("skeleton", 0.5),
                _let("orb", 0.3),
                _let("mage", 0.2)
            ]))
        
        self._enemies.append(_le( # 4
            frequency=1.3, 
            max_count=8, 
            types=[
                _let("skeleton", 0.4),
                _let("orb", 0.2),
                _let("mage", 0.2),
                _let("tank", 0.2)
            ]))
        
        self._enemies.append(_le( # 5
            frequency=1.1, 
            max_count=10, 
            types=[
                _let("skeleton", 0.3),
                _let("orb", 0.2),
                _let("mage", 0.3),
                _let("tank", 0.2)
            ]))
        
        self._active = self._enemies[0]

        self.population: list[str] = []
        self.weights: list[float] = []
    
    def random_type(self) -> str:
        return self._choice.select_one()

    def activate(self, id: int):
        if id >= len(self._enemies):
            self._active = self._enemies[len(self._enemies)-1]
        else:
            self._active = self._enemies[id]

        self._choice.set(
            [t.type for t in self._active.types], 
            [t.probability for t in self._active.types])

    @property
    def frequency(self) -> float:
        return self._active.frequency
    
    @property
    def max_count(self) -> int:
        return self._active.max_count