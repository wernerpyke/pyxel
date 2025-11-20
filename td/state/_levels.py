import random
from dataclasses import dataclass

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
                _let("orb", 0.3)
            ]))
        
        self._enemies.append(_le( # 2
            frequency=1.8, 
            max_count=5, 
            types=[
                _let("skeleton", 0.5),
                _let("orb", 0.3),
                _let("mage", 0.2)
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
                _let("skeleton", 0.5),
                _let("orb", 0.2),
                _let("mage", 0.3)
            ]))
        
        self._enemies.append(_le( # 5
            frequency=1.1, 
            max_count=10, 
            types=[
                _let("skeleton", 0.4),
                _let("orb", 0.3),
                _let("mage", 0.3)
            ]))
        
        self._active = self._enemies[0]

        self.population: list[str] = []
        self.weights: list[float] = []
    
    def random_type(self) -> str:
        # random.choices() takes a population and a list of weights.
        # k=1 means it returns a list containing only one item.
        # We access the first element [0] to get the string directly.
        selected_list = random.choices(
            population=self.population, 
            weights=self.weights, 
            k=1
        )
        return selected_list[0]

    def activate(self, id: int):
        if id >= len(self._enemies):
            self._active = self._enemies[len(self._enemies)-1]
        else:
            self._active = self._enemies[id]

        self.population = [t.type for t in self._active.types]
        self.weights = [t.probability for t in self._active.types]

    @property
    def frequency(self) -> float:
        return self._active.frequency
    
    @property
    def max_count(self) -> int:
        return self._active.max_count