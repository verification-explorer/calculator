"""Command-line interface for the calculator.

This module provides an interactive REPL (Read-Eval-Print Loop) for
performing calculations from the command line.
"""

import re
import sys
from typing import Optional

from calculator import core
from calculator.history import CalculationHistory

Number = int | float

HELP_TEXT = """
Calculator Commands:
  help     - Show this help message
  history  - Show calculation history
  clear    - Clear calculation history
  quit     - Exit the calculator

Supported Operations:
  Addition:       5 + 3
  Subtraction:    10 - 4
  Multiplication: 6 * 7
  Division:       15 / 3
  Power:          2 ^ 8
  Modulo:         17 % 5
  Square Root:    sqrt(16)

Type an expression and press Enter to calculate.
"""


def parse_number(s: str) -> Number:
    """Parse a string into a number.

    Args:
        s: The string to parse.

    Returns:
        An int if the string represents a whole number, otherwise a float.

    Raises:
        ValueError: If the string cannot be parsed as a number.
    """
    s = s.strip()
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        raise ValueError(f"Invalid number: {s}")


def evaluate_expression(expr: str) -> tuple[str, Number]:
    """Evaluate a mathematical expression.

    Args:
        expr: The expression string to evaluate.

    Returns:
        A tuple of (normalized_expression, result).

    Raises:
        ValueError: If the expression is invalid or cannot be evaluated.
    """
    expr = expr.strip()

    sqrt_match = re.match(r"sqrt\s*\(\s*([+-]?\d*\.?\d+)\s*\)", expr, re.IGNORECASE)
    if sqrt_match:
        n = parse_number(sqrt_match.group(1))
        result = core.square_root(n)
        return f"sqrt({n})", result

    binary_match = re.match(
        r"([+-]?\d*\.?\d+)\s*([+\-*/^%])\s*([+-]?\d*\.?\d+)", expr
    )
    if binary_match:
        a = parse_number(binary_match.group(1))
        op = binary_match.group(2)
        b = parse_number(binary_match.group(3))

        operations = {
            "+": (core.add, f"{a} + {b}"),
            "-": (core.subtract, f"{a} - {b}"),
            "*": (core.multiply, f"{a} * {b}"),
            "/": (core.divide, f"{a} / {b}"),
            "^": (core.power, f"{a} ^ {b}"),
            "%": (core.modulo, f"{a} % {b}"),
        }

        if op in operations:
            func, normalized = operations[op]
            result = func(a, b)
            return normalized, result

    raise ValueError(f"Invalid expression: {expr}")


def run_repl(history: Optional[CalculationHistory] = None) -> None:
    """Run the interactive calculator REPL.

    Args:
        history: Optional CalculationHistory instance. If not provided,
            a new instance will be created.

    This function runs an infinite loop until the user types 'quit'.
    It handles all exceptions gracefully and continues running.
    """
    if history is None:
        history = CalculationHistory()

    print("Calculator - Type 'help' for commands, 'quit' to exit")
    print()

    while True:
        try:
            user_input = input("calc> ").strip()
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        command = user_input.lower()

        if command == "quit":
            print("Goodbye!")
            break
        elif command == "help":
            print(HELP_TEXT)
        elif command == "history":
            entries = history.get_all()
            if not entries:
                print("No history yet.")
            else:
                print("Calculation History:")
                for i, entry in enumerate(entries, 1):
                    print(f"  {i}. {entry}")
        elif command == "clear":
            history.clear()
            print("History cleared.")
        else:
            try:
                normalized_expr, result = evaluate_expression(user_input)
                history.add(normalized_expr, result)
                print(f"  = {result}")
            except ValueError as e:
                print(f"Error: {e}")


def main() -> None:
    """Entry point for the calculator CLI.

    This function is called when running the calculator from the command line
    via the 'calc' command.
    """
    try:
        run_repl()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
