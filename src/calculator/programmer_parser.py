"""Expression parser for programmer mode.

This module provides expression parsing and evaluation for programmer mode,
supporting hex/octal/binary literals and bitwise operators with parentheses.
"""

import re
from typing import Union
from calculator import programmer
from calculator.programmer import Size


Number = Union[int, float]


def parse_base_literal(token: str) -> tuple[int, str]:
    """Parse a base-prefixed literal and return (value, base).

    Args:
        token: String token that may be a base literal (0xFF, 0o377, 0b1010, or decimal)

    Returns:
        Tuple of (integer_value, base_name) where base_name is "HEX", "DEC", "OCT", or "BIN"

    Raises:
        ValueError: If token is not a valid number literal

    Examples:
        >>> parse_base_literal("0xFF")
        (255, 'HEX')
        >>> parse_base_literal("255")
        (255, 'DEC')
        >>> parse_base_literal("0o377")
        (255, 'OCT')
        >>> parse_base_literal("0b11111111")
        (255, 'BIN')
    """
    token = token.strip().replace(" ", "")

    # Check for hex prefix
    if token.lower().startswith("0x"):
        try:
            value = int(token, 16)
            return value, "HEX"
        except ValueError:
            raise ValueError(f"Invalid hexadecimal literal: {token}")

    # Check for octal prefix
    if token.lower().startswith("0o"):
        try:
            value = int(token, 8)
            return value, "OCT"
        except ValueError:
            raise ValueError(f"Invalid octal literal: {token}")

    # Check for binary prefix
    if token.lower().startswith("0b"):
        try:
            value = int(token, 2)
            return value, "BIN"
        except ValueError:
            raise ValueError(f"Invalid binary literal: {token}")

    # Default to decimal
    try:
        value = int(token)
        return value, "DEC"
    except ValueError:
        raise ValueError(f"Invalid decimal literal: {token}")


def tokenize_expression(expr: str) -> list[str]:
    """Split expression into tokens: numbers, operators, parentheses.

    Args:
        expr: Expression string

    Returns:
        List of tokens

    Examples:
        >>> tokenize_expression("0xFF AND 0x0F")
        ['0xFF', 'AND', '0x0F']
        >>> tokenize_expression("(0xFF & 0x0F) | 0x10")
        ['(', '0xFF', '&', '0x0F', ')', '|', '0x10']
    """
    # Pattern: match hex/oct/bin/dec numbers, operators, parentheses
    # Support both word operators (AND, OR) and symbol operators (&, |)
    # Note: Use case-insensitive flag for hex/oct/bin prefixes
    pattern = r'(0[xX][0-9A-Fa-f]+|0[oO][0-7]+|0[bB][01\s]+|\d+|AND|OR|XOR|NOT|NAND|NOR|<<|>>|[&|^~+\-*/%()])'
    tokens = re.findall(pattern, expr, re.IGNORECASE)
    # Uppercase only the word operators, not the hex numbers
    result = []
    for token in tokens:
        token = token.strip()
        if token and not token.startswith('0'):  # Don't uppercase number literals
            result.append(token.upper())
        else:
            result.append(token)
    return [t for t in result if t]


def normalize_operator(op: str) -> str:
    """Normalize operator to word form for display.

    Args:
        op: Operator (can be word or symbol)

    Returns:
        Normalized word form

    Examples:
        >>> normalize_operator("&")
        'AND'
        >>> normalize_operator("AND")
        'AND'
    """
    operator_map = {
        "&": "AND",
        "|": "OR",
        "^": "XOR",
        "~": "NOT",
        "<<": "<<",
        ">>": ">>",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
        "%": "%",
    }
    return operator_map.get(op, op)


def evaluate_programmer_expression(
    expr: str, size: Size, carry: bool = False
) -> tuple[str, int, bool]:
    """Evaluate a programmer mode expression.

    Supports left-to-right evaluation (calculator style) with full parentheses support.
    Handles bitwise operators (AND, OR, XOR, NOT, NAND, NOR) and shift operators (<<, >>).

    Args:
        expr: Expression string (e.g., "0xFF AND 0x0F", "(0xFF & 0x0F) | 0x10")
        size: Integer size for operations
        carry: Current carry flag state

    Returns:
        Tuple of (normalized_expression, result, new_carry_flag)

    Raises:
        ValueError: If expression is invalid or contains errors

    Examples:
        >>> evaluate_programmer_expression("0xFF AND 0x0F", "Byte")
        ('0xFF AND 0x0F', 15, False)
        >>> evaluate_programmer_expression("0xFF << 1", "Byte")
        ('0xFF << 1', 254, False)
    """
    expr = expr.strip()

    # Handle empty expression
    if not expr:
        raise ValueError("Empty expression")

    tokens = tokenize_expression(expr)

    if not tokens:
        raise ValueError("Invalid expression: no tokens found")

    # Handle single number (no operation)
    if len(tokens) == 1:
        value, base = parse_base_literal(tokens[0])
        value = programmer.apply_size_mask(value, size)
        normalized = programmer.convert_to_base(value, base, size)
        return normalized, value, carry

    # Handle unary NOT operation
    if tokens[0].upper() in ["NOT", "~"] and len(tokens) == 2:
        value, base = parse_base_literal(tokens[1])
        result = programmer.bitwise_not(value, size)
        normalized = f"NOT {programmer.convert_to_base(value, base, size)}"
        return normalized, result, carry

    # Evaluate expression with parentheses support
    result, normalized_parts = _evaluate_with_parentheses(tokens, size, carry)

    # Build normalized expression
    normalized_expr = " ".join(normalized_parts)

    return normalized_expr, result, carry


def _evaluate_with_parentheses(
    tokens: list[str], size: Size, carry: bool
) -> tuple[int, list[str]]:
    """Evaluate expression with parentheses support (recursive).

    Args:
        tokens: List of tokens
        size: Integer size
        carry: Carry flag

    Returns:
        Tuple of (result, normalized_tokens)
    """
    # Find and evaluate innermost parentheses first
    while "(" in tokens:
        # Find innermost parentheses
        start_idx = -1
        for i, token in enumerate(tokens):
            if token == "(":
                start_idx = i
            elif token == ")":
                if start_idx == -1:
                    raise ValueError("Unmatched closing parenthesis")

                # Extract sub-expression
                sub_tokens = tokens[start_idx + 1 : i]
                sub_result, sub_normalized = _evaluate_left_to_right(sub_tokens, size, carry)

                # Replace parenthesized expression with just the result value
                # We'll track the normalized form separately
                result_token = str(sub_result)
                tokens = tokens[:start_idx] + [result_token] + tokens[i + 1 :]
                break
        else:
            if start_idx != -1:
                raise ValueError("Unmatched opening parenthesis")

    # Now evaluate without parentheses
    return _evaluate_left_to_right(tokens, size, carry)


def _evaluate_left_to_right(
    tokens: list[str], size: Size, carry: bool
) -> tuple[int, list[str]]:
    """Evaluate expression left-to-right (calculator style).

    Args:
        tokens: List of tokens without parentheses
        size: Integer size
        carry: Carry flag

    Returns:
        Tuple of (result, normalized_tokens)
    """
    if not tokens:
        raise ValueError("Empty token list")

    # Parse first operand
    value, base = parse_base_literal(tokens[0])
    result = programmer.apply_size_mask(value, size)
    normalized = [programmer.convert_to_base(value, base, size)]

    i = 1
    while i < len(tokens):
        if i >= len(tokens):
            break

        operator = tokens[i]
        normalized_op = normalize_operator(operator)

        # Check if we have a second operand
        if i + 1 >= len(tokens):
            raise ValueError(f"Missing operand after {operator}")

        # Parse second operand
        operand_token = tokens[i + 1]
        operand_value, operand_base = parse_base_literal(operand_token)
        operand_value = programmer.apply_size_mask(operand_value, size)
        normalized_operand = programmer.convert_to_base(operand_value, operand_base, size)

        # Apply operation
        result = _apply_operation(operator, result, operand_value, size, carry)

        # Add to normalized expression
        normalized.append(normalized_op)
        normalized.append(normalized_operand)

        i += 2

    return result, normalized


def _apply_operation(
    operator: str, a: int, b: int, size: Size, carry: bool
) -> int:
    """Apply a binary operation.

    Args:
        operator: Operator string
        a: First operand
        b: Second operand
        size: Integer size
        carry: Carry flag (used for rotate-through-carry)

    Returns:
        Result of operation
    """
    op_upper = operator.upper()

    # Bitwise operations
    if op_upper in ["AND", "&"]:
        return programmer.bitwise_and(a, b, size)
    elif op_upper in ["OR", "|"]:
        return programmer.bitwise_or(a, b, size)
    elif op_upper in ["XOR", "^"]:
        return programmer.bitwise_xor(a, b, size)
    elif op_upper == "NAND":
        return programmer.bitwise_nand(a, b, size)
    elif op_upper == "NOR":
        return programmer.bitwise_nor(a, b, size)

    # Shift operations
    elif op_upper == "<<":
        return programmer.left_shift(a, b, size)
    elif op_upper == ">>":
        # Default to logical shift (could be extended to support arithmetic)
        return programmer.right_shift_logical(a, b, size)

    # Arithmetic operations (from core.py)
    elif op_upper == "+":
        result = a + b
        return programmer.apply_size_mask(result, size)
    elif op_upper == "-":
        result = a - b
        return programmer.apply_size_mask(result, size)
    elif op_upper == "*":
        result = a * b
        return programmer.apply_size_mask(result, size)
    elif op_upper == "/":
        if b == 0:
            raise ValueError("Division by zero")
        result = int(a / b)
        return programmer.apply_size_mask(result, size)
    elif op_upper == "%":
        if b == 0:
            raise ValueError("Division by zero")
        result = a % b
        return programmer.apply_size_mask(result, size)

    else:
        raise ValueError(f"Unknown operator: {operator}")
