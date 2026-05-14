"""Tests for calculator.core module."""

import math

import pytest

from calculator import core


class TestAdd:
    """Tests for the add function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (1.5, 2.5, 4.0),
            (-5, -3, -8),
            (100, 200, 300),
            (0.1, 0.2, pytest.approx(0.3)),
        ],
    )
    def test_add_happy_path(self, a: float, b: float, expected: float) -> None:
        """Test addition with various valid inputs."""
        assert core.add(a, b) == expected


class TestSubtract:
    """Tests for the subtract function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (5, 3, 2),
            (0, 0, 0),
            (1, 1, 0),
            (10, 15, -5),
            (-5, -3, -2),
            (2.5, 1.5, 1.0),
        ],
    )
    def test_subtract_happy_path(self, a: float, b: float, expected: float) -> None:
        """Test subtraction with various valid inputs."""
        assert core.subtract(a, b) == expected


class TestMultiply:
    """Tests for the multiply function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (4, 3, 12),
            (0, 100, 0),
            (-2, 3, -6),
            (-2, -3, 6),
            (2.5, 4, 10.0),
            (1, 1, 1),
        ],
    )
    def test_multiply_happy_path(self, a: float, b: float, expected: float) -> None:
        """Test multiplication with various valid inputs."""
        assert core.multiply(a, b) == expected


class TestDivide:
    """Tests for the divide function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (10, 2, 5.0),
            (7, 2, 3.5),
            (0, 5, 0.0),
            (-10, 2, -5.0),
            (10, -2, -5.0),
            (-10, -2, 5.0),
            (1, 3, pytest.approx(0.333333, rel=1e-4)),
        ],
    )
    def test_divide_happy_path(self, a: float, b: float, expected: float) -> None:
        """Test division with various valid inputs."""
        assert core.divide(a, b) == expected

    def test_divide_by_zero_raises_value_error(self) -> None:
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            core.divide(10, 0)

    def test_divide_zero_by_zero_raises_value_error(self) -> None:
        """Test that 0/0 raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            core.divide(0, 0)


class TestPower:
    """Tests for the power function."""

    @pytest.mark.parametrize(
        "base,exp,expected",
        [
            (2, 3, 8),
            (2, 0, 1),
            (2, -1, 0.5),
            (4, 0.5, 2.0),
            (10, 2, 100),
            (-2, 2, 4),
            (-2, 3, -8),
            (0, 5, 0),
        ],
    )
    def test_power_happy_path(self, base: float, exp: float, expected: float) -> None:
        """Test power function with various valid inputs."""
        assert core.power(base, exp) == expected


class TestSquareRoot:
    """Tests for the square_root function."""

    @pytest.mark.parametrize(
        "n,expected",
        [
            (16, 4.0),
            (2, math.sqrt(2)),
            (0, 0.0),
            (1, 1.0),
            (100, 10.0),
            (0.25, 0.5),
        ],
    )
    def test_square_root_happy_path(self, n: float, expected: float) -> None:
        """Test square root with various valid inputs."""
        assert core.square_root(n) == pytest.approx(expected)

    def test_square_root_negative_raises_value_error(self) -> None:
        """Test that square root of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of a negative"):
            core.square_root(-1)

    def test_square_root_negative_large_raises_value_error(self) -> None:
        """Test that square root of large negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of a negative"):
            core.square_root(-100)


class TestModulo:
    """Tests for the modulo function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (10, 3, 1),
            (15, 5, 0),
            (17, 5, 2),
            (-10, 3, 2),
            (10, -3, -2),
            (0, 5, 0),
            (7.5, 2.5, pytest.approx(0.0)),
        ],
    )
    def test_modulo_happy_path(self, a: float, b: float, expected: float) -> None:
        """Test modulo with various valid inputs."""
        assert core.modulo(a, b) == expected

    def test_modulo_by_zero_raises_value_error(self) -> None:
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot perform modulo by zero"):
            core.modulo(10, 0)

    def test_modulo_zero_by_zero_raises_value_error(self) -> None:
        """Test that 0 % 0 raises ValueError."""
        with pytest.raises(ValueError, match="Cannot perform modulo by zero"):
            core.modulo(0, 0)
