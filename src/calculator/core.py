"""Core calculation functions for the calculator.

This module provides pure mathematical operations with proper error handling
and type hints. All functions raise ValueError for invalid inputs.
"""

import math
from typing import Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Add two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.

    Examples:
        >>> add(2, 3)
        5
        >>> add(1.5, 2.5)
        4.0
    """
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Subtract the second number from the first.

    Args:
        a: The number to subtract from.
        b: The number to subtract.

    Returns:
        The difference of a minus b.

    Examples:
        >>> subtract(5, 3)
        2
        >>> subtract(1.0, 2.5)
        -1.5
    """
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Multiply two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The product of a and b.

    Examples:
        >>> multiply(4, 3)
        12
        >>> multiply(2.5, 4)
        10.0
    """
    return a * b


def divide(a: Number, b: Number) -> float:
    """Divide the first number by the second.

    Args:
        a: The dividend (number to be divided).
        b: The divisor (number to divide by).

    Returns:
        The quotient of a divided by b.

    Raises:
        ValueError: If b is zero (division by zero).

    Examples:
        >>> divide(10, 2)
        5.0
        >>> divide(7, 2)
        3.5
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: Number, exp: Number) -> Number:
    """Raise a base number to an exponent.

    Args:
        base: The base number.
        exp: The exponent to raise the base to.

    Returns:
        The result of base raised to the power of exp.

    Examples:
        >>> power(2, 3)
        8
        >>> power(4, 0.5)
        2.0
    """
    return base ** exp


def square_root(n: Number) -> float:
    """Calculate the square root of a number.

    Args:
        n: The number to find the square root of.

    Returns:
        The square root of n.

    Raises:
        ValueError: If n is negative (square root of negative number).

    Examples:
        >>> square_root(16)
        4.0
        >>> square_root(2)
        1.4142135623730951
    """
    if n < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    return math.sqrt(n)


def modulo(a: Number, b: Number) -> Number:
    """Calculate the remainder of division.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The remainder when a is divided by b.

    Raises:
        ValueError: If b is zero (modulo by zero).

    Examples:
        >>> modulo(10, 3)
        1
        >>> modulo(15, 5)
        0
    """
    if b == 0:
        raise ValueError("Cannot perform modulo by zero")
    return a % b
