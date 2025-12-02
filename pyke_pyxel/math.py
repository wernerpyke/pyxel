import random
from typing import Any

class RandomChoice:
    """
    Convenience class to select a random choice based on a set of probabilities.
    For example:
    - choices = ["A", "B", "C"]
    - probabilities = [0.3, 0.4, 0.3]

    The sum of the probabilities should be 1.0.
    """
    def __init__(self) -> None:
        self._population: list[Any] = []
        self._weights: list[float] = []

    """
    Set the list of choices and their matching probabilities.

    Args:
            choices (list[Any]): A list of choices.
            probabilities (list[float]): A list of probabilities for each choice.
    """
    def set(self, choices: list[Any], probabilities: list[float]):
        self._population = choices
        self._weights = probabilities

    """
    Add a choice and its matching probability to the list of choices and probabilities.

    Args:
            choice (Any): The choice to add.
            probability (float): The probability for the choice.
    """
    def add(self, choice: Any, probability: float):
        self._population.append(choice)
        self._weights.append(probability)

    """
    Select one choice from the list of choices based on their matching probabilities.

    Returns:
            Any: The selected choice.
    """
    def select_one(self) -> Any:
        # random.choices() takes a population and a list of weights.
        # k=1 means it returns a list containing only one item.
        # We access the first element [0] to get the string directly.
        selected_list = random.choices(
            population=self._population, 
            weights=self._weights, 
            k=1
        )
        return selected_list[0]