"""Tests for calculator.cli module."""

import pytest

from calculator.cli import evaluate_expression, parse_number
from calculator.history import CalculationHistory


class TestParseNumber:
    """Tests for the parse_number function."""

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("5", 5),
            ("0", 0),
            ("-10", -10),
            ("3.14", 3.14),
            ("-2.5", -2.5),
            ("  42  ", 42),
            ("100", 100),
        ],
    )
    def test_parse_number_valid(self, input_str: str, expected: float) -> None:
        """Test parsing valid number strings."""
        assert parse_number(input_str) == expected

    def test_parse_number_invalid(self) -> None:
        """Test that invalid strings raise ValueError."""
        with pytest.raises(ValueError, match="Invalid number"):
            parse_number("abc")

    def test_parse_number_empty(self) -> None:
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid number"):
            parse_number("")


class TestEvaluateExpression:
    """Tests for the evaluate_expression function."""

    @pytest.mark.parametrize(
        "expr,expected_normalized,expected_result",
        [
            ("2 + 3", "2 + 3", 5),
            ("10 - 4", "10 - 4", 6),
            ("6 * 7", "6 * 7", 42),
            ("15 / 3", "15 / 3", 5.0),
            ("2 ^ 8", "2 ^ 8", 256),
            ("17 % 5", "17 % 5", 2),
            ("sqrt(16)", "sqrt(16)", 4.0),
            ("SQRT(25)", "sqrt(25)", 5.0),
            ("  5  +  5  ", "5 + 5", 10),
        ],
    )
    def test_evaluate_expression_valid(
        self, expr: str, expected_normalized: str, expected_result: float
    ) -> None:
        """Test evaluating valid expressions."""
        normalized, result = evaluate_expression(expr)
        assert normalized == expected_normalized
        assert result == expected_result

    def test_evaluate_division_by_zero(self) -> None:
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            evaluate_expression("10 / 0")

    def test_evaluate_negative_sqrt(self) -> None:
        """Test that square root of negative raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root"):
            evaluate_expression("sqrt(-4)")

    def test_evaluate_modulo_by_zero(self) -> None:
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot perform modulo by zero"):
            evaluate_expression("10 % 0")

    def test_evaluate_invalid_expression(self) -> None:
        """Test that invalid expression raises ValueError."""
        with pytest.raises(ValueError, match="Invalid expression"):
            evaluate_expression("hello world")

    def test_evaluate_float_numbers(self) -> None:
        """Test expressions with float numbers."""
        normalized, result = evaluate_expression("2.5 + 3.5")
        assert normalized == "2.5 + 3.5"
        assert result == 6.0

    def test_evaluate_negative_numbers(self) -> None:
        """Test expressions with negative numbers."""
        normalized, result = evaluate_expression("-5 + 3")
        assert normalized == "-5 + 3"
        assert result == -2


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def test_history_integration(self) -> None:
        """Test that evaluated expressions are tracked in history."""
        history = CalculationHistory()

        expr1, result1 = evaluate_expression("5 + 5")
        history.add(expr1, result1)

        expr2, result2 = evaluate_expression("10 * 2")
        history.add(expr2, result2)

        entries = history.get_all()
        assert len(entries) == 2
        assert entries[0].expression == "5 + 5"
        assert entries[0].result == 10
        assert entries[1].expression == "10 * 2"
        assert entries[1].result == 20

    def test_history_clear_integration(self) -> None:
        """Test clearing history in CLI context."""
        history = CalculationHistory()

        expr, result = evaluate_expression("3 * 3")
        history.add(expr, result)
        assert len(history) == 1

        history.clear()
        assert len(history) == 0

    @pytest.mark.parametrize(
        "expr",
        [
            "2+3",
            "2 +3",
            "2+ 3",
            "  2 + 3  ",
        ],
    )
    def test_whitespace_handling(self, expr: str) -> None:
        """Test that expressions with various whitespace are handled."""
        normalized, result = evaluate_expression(expr)
        assert result == 5
