"""Calculator package - a simple calculator with history tracking."""

from calculator.core import (
    add,
    subtract,
    multiply,
    divide,
    power,
    square_root,
    modulo,
)
from calculator.history import CalculationHistory, HistoryEntry

__version__ = "1.0.0"
__all__ = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "square_root",
    "modulo",
    "CalculationHistory",
    "HistoryEntry",
]
