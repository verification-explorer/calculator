"""Tests for calculator.history module."""

from datetime import datetime

import pytest

from calculator.history import CalculationHistory, HistoryEntry


class TestHistoryEntry:
    """Tests for the HistoryEntry dataclass."""

    def test_history_entry_creation(self) -> None:
        """Test creating a HistoryEntry with all fields."""
        timestamp = datetime(2024, 1, 1, 12, 0, 0)
        entry = HistoryEntry("2 + 3", 5, timestamp)

        assert entry.expression == "2 + 3"
        assert entry.result == 5
        assert entry.timestamp == timestamp

    def test_history_entry_default_timestamp(self) -> None:
        """Test that HistoryEntry gets a default timestamp."""
        before = datetime.now()
        entry = HistoryEntry("5 * 5", 25)
        after = datetime.now()

        assert before <= entry.timestamp <= after

    def test_history_entry_str(self) -> None:
        """Test the string representation of HistoryEntry."""
        entry = HistoryEntry("10 / 2", 5.0)
        assert str(entry) == "10 / 2 = 5.0"

    def test_history_entry_with_float_result(self) -> None:
        """Test HistoryEntry with a float result."""
        entry = HistoryEntry("7 / 3", 2.333333)
        assert entry.result == 2.333333


class TestCalculationHistory:
    """Tests for the CalculationHistory class."""

    def test_init_empty(self, empty_history: CalculationHistory) -> None:
        """Test that a new history is empty."""
        assert len(empty_history) == 0
        assert empty_history.get_all() == []

    def test_add_single_entry(self, empty_history: CalculationHistory) -> None:
        """Test adding a single entry to history."""
        entry = empty_history.add("3 + 4", 7)

        assert len(empty_history) == 1
        assert entry.expression == "3 + 4"
        assert entry.result == 7

    def test_add_multiple_entries(self, empty_history: CalculationHistory) -> None:
        """Test adding multiple entries to history."""
        empty_history.add("1 + 1", 2)
        empty_history.add("2 + 2", 4)
        empty_history.add("3 + 3", 6)

        assert len(empty_history) == 3

    def test_get_all_returns_copy(self, populated_history: CalculationHistory) -> None:
        """Test that get_all returns a copy, not the internal list."""
        entries1 = populated_history.get_all()
        entries2 = populated_history.get_all()

        assert entries1 == entries2
        assert entries1 is not entries2

    def test_get_all_order(self, empty_history: CalculationHistory) -> None:
        """Test that entries are returned in chronological order."""
        empty_history.add("first", 1)
        empty_history.add("second", 2)
        empty_history.add("third", 3)

        entries = empty_history.get_all()
        assert entries[0].expression == "first"
        assert entries[1].expression == "second"
        assert entries[2].expression == "third"

    @pytest.mark.parametrize(
        "n,expected_count",
        [
            (1, 1),
            (2, 2),
            (3, 3),
            (5, 3),
            (100, 3),
        ],
    )
    def test_get_last_n(
        self,
        populated_history: CalculationHistory,
        n: int,
        expected_count: int,
    ) -> None:
        """Test getting the last n entries."""
        entries = populated_history.get_last(n)
        assert len(entries) == expected_count

    def test_get_last_returns_correct_entries(
        self, populated_history: CalculationHistory
    ) -> None:
        """Test that get_last returns the most recent entries."""
        entries = populated_history.get_last(2)
        assert entries[0].expression == "10 / 2"
        assert entries[1].expression == "4 * 5"

    def test_get_last_zero(self, populated_history: CalculationHistory) -> None:
        """Test that get_last(0) returns empty list."""
        assert populated_history.get_last(0) == []

    def test_get_last_negative(self, populated_history: CalculationHistory) -> None:
        """Test that get_last with negative number returns empty list."""
        assert populated_history.get_last(-1) == []

    def test_clear(self, populated_history: CalculationHistory) -> None:
        """Test clearing the history."""
        assert len(populated_history) > 0
        populated_history.clear()
        assert len(populated_history) == 0
        assert populated_history.get_all() == []

    def test_clear_empty_history(self, empty_history: CalculationHistory) -> None:
        """Test clearing an already empty history."""
        empty_history.clear()
        assert len(empty_history) == 0

    def test_len(self, empty_history: CalculationHistory) -> None:
        """Test the __len__ method."""
        assert len(empty_history) == 0
        empty_history.add("1", 1)
        assert len(empty_history) == 1
        empty_history.add("2", 2)
        assert len(empty_history) == 2

    def test_history_with_fixture(
        self, sample_history_entries: list[HistoryEntry]
    ) -> None:
        """Test using the sample_history_entries fixture directly."""
        assert len(sample_history_entries) == 3
        assert sample_history_entries[0].expression == "2 + 3"
        assert sample_history_entries[1].result == 5.0
        assert sample_history_entries[2].expression == "4 * 5"
