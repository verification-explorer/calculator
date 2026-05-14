"""Pytest configuration and shared fixtures."""

from datetime import datetime

import pytest

from calculator.history import CalculationHistory, HistoryEntry


@pytest.fixture
def sample_history_entries() -> list[HistoryEntry]:
    """Provide a list of sample HistoryEntry objects for testing.

    Returns:
        A list of three pre-populated HistoryEntry objects.
    """
    return [
        HistoryEntry("2 + 3", 5, datetime(2024, 1, 1, 10, 0, 0)),
        HistoryEntry("10 / 2", 5.0, datetime(2024, 1, 1, 10, 1, 0)),
        HistoryEntry("4 * 5", 20, datetime(2024, 1, 1, 10, 2, 0)),
    ]


@pytest.fixture
def populated_history(sample_history_entries: list[HistoryEntry]) -> CalculationHistory:
    """Provide a CalculationHistory pre-populated with sample entries.

    Args:
        sample_history_entries: The sample entries fixture.

    Returns:
        A CalculationHistory instance with three entries.
    """
    history = CalculationHistory()
    for entry in sample_history_entries:
        history.add(entry.expression, entry.result)
    return history


@pytest.fixture
def empty_history() -> CalculationHistory:
    """Provide an empty CalculationHistory instance.

    Returns:
        A fresh, empty CalculationHistory.
    """
    return CalculationHistory()
