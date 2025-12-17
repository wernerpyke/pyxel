import random
from typing import Any

class RandomChoice:
    """
    Convenience class to select a random item from a list of choices.
    """
    def __init__(self, choices: list[Any]) -> None:
        self._choices = choices

    def select_one(self) -> Any:
        """
        Select one choice from the list of choices.

        Returns:
                Any: The selected choice.
        """
        return random.choice(self._choices)

class WeightedChoice:
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

    def set(self, choices: list[Any], probabilities: list[float]):
        """
        Set the list of choices and their matching probabilities.

        Args:
                choices (list[Any]): A list of choices.
                probabilities (list[float]): A list of probabilities for each choice.
        """
        self._population = choices
        self._weights = probabilities

    def add(self, choice: Any, probability: float):
        """
        Add a choice and its matching probability to the list of choices and probabilities.

        Args:
                choice (Any): The choice to add.
                probability (float): The probability for the choice.
        """
        self._population.append(choice)
        self._weights.append(probability)

    def reset(self):
        """Reset the list of choices and probabilities."""
        self._population.clear()
        self._weights.clear()

    def select_one(self) -> Any:
        """
        Select one choice from the list of choices based on their matching probabilities.

        Returns:
                Any: The selected choice.
        """
        # random.choices() takes a population and a list of weights.
        # k=1 means it returns a list containing only one item.
        # We access the first element [0] to get the string directly.
        selected_list = random.choices(
            population=self._population, 
            weights=self._weights, 
            k=1
        )
        return selected_list[0]