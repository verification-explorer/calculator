"""Calculation history management.

This module provides classes for tracking and managing calculation history,
including storage of expressions, results, and timestamps.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Union, Literal, Optional

Number = Union[int, float]
Size = Literal["Byte", "Word", "DWord", "QWord"]
Base = Literal["HEX", "DEC", "OCT", "BIN"]


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


@dataclass
class ProgrammerHistoryEntry(HistoryEntry):
    """A programmer mode calculation history entry.

    Extends HistoryEntry with base and integer size information.

    Attributes:
        expression: The mathematical expression that was evaluated.
        result: The result of the calculation.
        timestamp: When the calculation was performed.
        base: The number base used (HEX, DEC, OCT, BIN).
        integer_size: The integer size used (Byte, Word, DWord, QWord).
    """

    base: Optional[Base] = None
    integer_size: Optional[Size] = None

    def __str__(self) -> str:
        """Return a human-readable string representation with base and size.

        Returns:
            A formatted string showing the expression, result, base, and size.
        """
        if self.base and self.integer_size:
            return f"{self.expression} = {self.result} [{self.base}, {self.integer_size}]"
        return f"{self.expression} = {self.result}"


@dataclass
class ConverterHistoryEntry(HistoryEntry):
    """A unit converter mode history entry.

    Extends HistoryEntry with category and unit information.

    Attributes:
        expression: The formatted from value string (e.g., "1,234.56789").
        result: The converted result value.
        timestamp: When the conversion was performed.
        category: The category (e.g., "Length", "Temperature").
        from_unit: Source unit name (e.g., "meter").
        to_unit: Target unit name (e.g., "foot").
    """

    category: Optional[str] = None
    from_unit: Optional[str] = None
    to_unit: Optional[str] = None

    def __str__(self) -> str:
        """Return a human-readable string representation with units.

        Returns:
            A formatted string showing the conversion, e.g.,
            "1,234.56789 m = 4,050.52493 ft [Length]"
        """
        if self.category and self.from_unit and self.to_unit:
            from calculator import converter

            from_abbr = converter.get_unit_abbreviation(self.from_unit)
            to_abbr = converter.get_unit_abbreviation(self.to_unit)
            result_str = converter.format_result(float(self.result))
            return f"{self.expression} {from_abbr} = {result_str} {to_abbr} [{self.category}]"
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

    def add_converter(
        self,
        from_value: str,
        to_value: Number,
        category: str,
        from_unit: str,
        to_unit: str,
    ) -> ConverterHistoryEntry:
        """Add a converter mode entry to the history.

        Args:
            from_value: The formatted from value string.
            to_value: The numeric result.
            category: Category name (e.g., "Length").
            from_unit: Source unit name (e.g., "meter").
            to_unit: Target unit name (e.g., "foot").

        Returns:
            The newly created ConverterHistoryEntry.

        Examples:
            >>> history = CalculationHistory()
            >>> entry = history.add_converter("100", 328.084, "Length", "meter", "foot")
            >>> str(entry)
            '100 m = 328.084 ft [Length]'
        """
        entry = ConverterHistoryEntry(
            expression=from_value,
            result=to_value,
            category=category,
            from_unit=from_unit,
            to_unit=to_unit,
        )
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
