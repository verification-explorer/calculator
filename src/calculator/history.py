"""Calculation history management.

This module provides classes for tracking and managing calculation history,
including storage of expressions, results, and timestamps.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Union

Number = Union[int, float]


@dataclass
class HistoryEntry:
    """A single calculation history entry.

    Attributes:
        expression: The mathematical expression that was evaluated.
        result: The result of the calculation.
        timestamp: When the calculation was performed.
    """

    expression: str
    result: Number
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        """Return a human-readable string representation.

        Returns:
            A formatted string showing the expression and result.
        """
        return f"{self.expression} = {self.result}"


class CalculationHistory:
    """Manages a list of calculation history entries.

    This class provides methods to add, retrieve, and clear calculation
    history entries. History is stored in chronological order.

    Attributes:
        _entries: Internal list storing HistoryEntry objects.

    Examples:
        >>> history = CalculationHistory()
        >>> history.add("2 + 3", 5)
        >>> history.get_all()
        [HistoryEntry(expression='2 + 3', result=5, ...)]
    """

    def __init__(self) -> None:
        """Initialize an empty calculation history."""
        self._entries: list[HistoryEntry] = []

    def add(self, expression: str, result: Number) -> HistoryEntry:
        """Add a new calculation to the history.

        Args:
            expression: The mathematical expression that was evaluated.
            result: The result of the calculation.

        Returns:
            The newly created HistoryEntry.

        Examples:
            >>> history = CalculationHistory()
            >>> entry = history.add("5 * 3", 15)
            >>> entry.result
            15
        """
        entry = HistoryEntry(expression=expression, result=result)
        self._entries.append(entry)
        return entry

    def get_all(self) -> list[HistoryEntry]:
        """Retrieve all history entries.

        Returns:
            A list of all HistoryEntry objects in chronological order.

        Examples:
            >>> history = CalculationHistory()
            >>> history.add("1 + 1", 2)
            >>> history.add("2 + 2", 4)
            >>> len(history.get_all())
            2
        """
        return list(self._entries)

    def get_last(self, n: int) -> list[HistoryEntry]:
        """Retrieve the last n history entries.

        Args:
            n: The number of recent entries to retrieve.

        Returns:
            A list of the last n HistoryEntry objects. If n is greater
            than the total number of entries, returns all entries.

        Examples:
            >>> history = CalculationHistory()
            >>> history.add("1 + 1", 2)
            >>> history.add("2 + 2", 4)
            >>> history.add("3 + 3", 6)
            >>> [e.result for e in history.get_last(2)]
            [4, 6]
        """
        if n <= 0:
            return []
        return list(self._entries[-n:])

    def clear(self) -> None:
        """Clear all history entries.

        Examples:
            >>> history = CalculationHistory()
            >>> history.add("1 + 1", 2)
            >>> history.clear()
            >>> len(history.get_all())
            0
        """
        self._entries.clear()

    def __len__(self) -> int:
        """Return the number of entries in history.

        Returns:
            The count of history entries.
        """
        return len(self._entries)
