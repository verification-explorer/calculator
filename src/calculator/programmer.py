"""Programmer mode bitwise operations and utilities.

This module provides bitwise operations, shift operations, and base conversion
utilities for the calculator's Programmer mode.
"""

from typing import Literal, Union

# Type definitions
Size = Literal["Byte", "Word", "DWord", "QWord"]
Base = Literal["HEX", "DEC", "OCT", "BIN"]
Number = Union[int, float]


def get_size_bits(size: Size) -> int:
    """Get bit width for integer size.

    Args:
        size: Integer size (Byte, Word, DWord, QWord)

    Returns:
        Number of bits (8, 16, 32, or 64)

    Examples:
        >>> get_size_bits("Byte")
        8
        >>> get_size_bits("QWord")
        64
    """
    size_map = {"Byte": 8, "Word": 16, "DWord": 32, "QWord": 64}
    return size_map[size]


def get_size_mask(size: Size) -> int:
    """Get bitmask for integer size.

    Args:
        size: Integer size (Byte, Word, DWord, QWord)

    Returns:
        Bitmask for truncation (e.g., 0xFF for Byte)

    Examples:
        >>> hex(get_size_mask("Byte"))
        '0xff'
        >>> hex(get_size_mask("Word"))
        '0xffff'
    """
    bits = get_size_bits(size)
    return (1 << bits) - 1


def apply_size_mask(value: int, size: Size) -> int:
    """Apply integer size truncation using two's complement.

    Args:
        value: Integer value to truncate
        size: Target integer size

    Returns:
        Value truncated to size

    Examples:
        >>> hex(apply_size_mask(0x1234, "Byte"))
        '0x34'
        >>> apply_size_mask(-1, "Byte")
        255
    """
    mask = get_size_mask(size)
    return value & mask


def convert_to_base(value: int, base: Base, size: Size) -> str:
    """Convert integer to specified base with prefix.

    Args:
        value: Integer to convert
        base: Target base (HEX, DEC, OCT, BIN)
        size: Integer size for proper formatting

    Returns:
        Formatted string with prefix (0x, 0o, 0b) or plain decimal

    Examples:
        >>> convert_to_base(255, "HEX", "Byte")
        '0xFF'
        >>> convert_to_base(255, "DEC", "Byte")
        '255'
        >>> convert_to_base(255, "BIN", "Byte")
        '0b1111 1111'
    """
    # Apply size mask to ensure value is in range
    value = apply_size_mask(value, size)

    if base == "HEX":
        # Remove '0x' prefix from hex(), uppercase, add back with '0x'
        hex_str = format(value, 'X')
        return f"0x{hex_str}"
    elif base == "DEC":
        return str(value)
    elif base == "OCT":
        # Remove '0o' prefix from oct(), add back
        oct_str = format(value, 'o')
        return f"0o{oct_str}"
    elif base == "BIN":
        # Remove '0b' prefix from bin(), add nibble grouping
        bits = get_size_bits(size)
        bin_str = format(value, f'0{bits}b')
        # Group by 4 bits (nibbles) with spaces
        grouped = ' '.join([bin_str[i:i+4] for i in range(0, len(bin_str), 4)])
        return f"0b{grouped}"
    else:
        raise ValueError(f"Unknown base: {base}")


def parse_base_input(value_str: str, base: Base) -> int:
    """Parse a string in a specific base to integer.

    Args:
        value_str: String to parse (may include prefix like 0x, 0o, 0b)
        base: Expected base (HEX, DEC, OCT, BIN)

    Returns:
        Integer value

    Raises:
        ValueError: If string is invalid for the specified base

    Examples:
        >>> parse_base_input("0xFF", "HEX")
        255
        >>> parse_base_input("255", "DEC")
        255
        >>> parse_base_input("0b11111111", "BIN")
        255
    """
    # Remove whitespace and prefixes
    value_str = value_str.strip().replace(" ", "")

    if base == "HEX":
        # Accept with or without 0x prefix
        if value_str.lower().startswith("0x"):
            value_str = value_str[2:]
        return int(value_str, 16)
    elif base == "DEC":
        return int(value_str, 10)
    elif base == "OCT":
        # Accept with or without 0o prefix
        if value_str.lower().startswith("0o"):
            value_str = value_str[2:]
        return int(value_str, 8)
    elif base == "BIN":
        # Accept with or without 0b prefix
        if value_str.lower().startswith("0b"):
            value_str = value_str[2:]
        return int(value_str, 2)
    else:
        raise ValueError(f"Unknown base: {base}")


def check_overflow(value: int, new_digit: str, base: Base, size: Size) -> bool:
    """Check if adding a digit would overflow the current integer size.

    Args:
        value: Current value
        new_digit: Digit to potentially add
        base: Current base mode
        size: Current integer size

    Returns:
        True if adding the digit would overflow, False otherwise

    Examples:
        >>> check_overflow(0xFF, "F", "HEX", "Byte")
        True
        >>> check_overflow(0xF, "F", "HEX", "Byte")
        False
    """
    base_radix = {"HEX": 16, "DEC": 10, "OCT": 8, "BIN": 2}[base]
    try:
        new_digit_val = int(new_digit, base_radix)
    except ValueError:
        return True  # Invalid digit for this base

    new_value = value * base_radix + new_digit_val
    max_value = get_size_mask(size)
    return new_value > max_value


def bitwise_and(a: int, b: int, size: Size) -> int:
    """Bitwise AND operation.

    Args:
        a: First operand
        b: Second operand
        size: Integer size for truncation

    Returns:
        a AND b, truncated to size

    Examples:
        >>> hex(bitwise_and(0xFF, 0x0F, "Byte"))
        '0xf'
        >>> bitwise_and(255, 15, "Byte")
        15
    """
    result = a & b
    return apply_size_mask(result, size)


def bitwise_or(a: int, b: int, size: Size) -> int:
    """Bitwise OR operation.

    Args:
        a: First operand
        b: Second operand
        size: Integer size for truncation

    Returns:
        a OR b, truncated to size

    Examples:
        >>> hex(bitwise_or(0xF0, 0x0F, "Byte"))
        '0xff'
        >>> bitwise_or(240, 15, "Byte")
        255
    """
    result = a | b
    return apply_size_mask(result, size)


def bitwise_xor(a: int, b: int, size: Size) -> int:
    """Bitwise XOR operation.

    Args:
        a: First operand
        b: Second operand
        size: Integer size for truncation

    Returns:
        a XOR b, truncated to size

    Examples:
        >>> hex(bitwise_xor(0xFF, 0x0F, "Byte"))
        '0xf0'
        >>> bitwise_xor(255, 15, "Byte")
        240
    """
    result = a ^ b
    return apply_size_mask(result, size)


def bitwise_nand(a: int, b: int, size: Size) -> int:
    """Bitwise NAND operation.

    Args:
        a: First operand
        b: Second operand
        size: Integer size for truncation

    Returns:
        NOT (a AND b), truncated to size

    Examples:
        >>> hex(bitwise_nand(0xFF, 0x0F, "Byte"))
        '0xf0'
        >>> bitwise_nand(255, 15, "Byte")
        240
    """
    result = ~(a & b)
    return apply_size_mask(result, size)


def bitwise_nor(a: int, b: int, size: Size) -> int:
    """Bitwise NOR operation.

    Args:
        a: First operand
        b: Second operand
        size: Integer size for truncation

    Returns:
        NOT (a OR b), truncated to size

    Examples:
        >>> hex(bitwise_nor(0xF0, 0x0F, "Byte"))
        '0x0'
        >>> bitwise_nor(240, 15, "Byte")
        0
    """
    result = ~(a | b)
    return apply_size_mask(result, size)


def bitwise_not(a: int, size: Size) -> int:
    """Bitwise NOT (unary) operation.

    Args:
        a: Operand
        size: Integer size

    Returns:
        Bitwise NOT of a, truncated to size

    Examples:
        >>> hex(bitwise_not(0x0F, "Byte"))
        '0xf0'
        >>> hex(bitwise_not(0x0F, "Word"))
        '0xfff0'
    """
    result = ~a
    return apply_size_mask(result, size)


def left_shift(a: int, shift_amount: int, size: Size) -> int:
    """Logical left shift.

    Args:
        a: Value to shift
        shift_amount: Number of positions to shift
        size: Integer size

    Returns:
        a << shift_amount, truncated to size

    Examples:
        >>> hex(left_shift(0x0F, 4, "Byte"))
        '0xf0'
        >>> hex(left_shift(0xFF, 1, "Byte"))
        '0xfe'
    """
    bits = get_size_bits(size)
    # Wrap shift amount (modulo bit width)
    shift_amount = shift_amount % bits
    result = a << shift_amount
    return apply_size_mask(result, size)


def right_shift_logical(a: int, shift_amount: int, size: Size) -> int:
    """Logical right shift (zero-fill).

    Args:
        a: Value to shift
        shift_amount: Number of positions to shift
        size: Integer size

    Returns:
        a >> shift_amount (logical), zero-filled

    Examples:
        >>> hex(right_shift_logical(0xFF, 1, "Byte"))
        '0x7f'
        >>> hex(right_shift_logical(0xF0, 4, "Byte"))
        '0xf'
    """
    bits = get_size_bits(size)
    # Wrap shift amount
    shift_amount = shift_amount % bits
    # Ensure value is positive (treat as unsigned)
    a = apply_size_mask(a, size)
    result = a >> shift_amount
    return result


def right_shift_arithmetic(a: int, shift_amount: int, size: Size) -> int:
    """Arithmetic right shift (sign-extend).

    Args:
        a: Value to shift
        shift_amount: Number of positions to shift
        size: Integer size

    Returns:
        a >> shift_amount (arithmetic), sign-extended

    Examples:
        >>> hex(right_shift_arithmetic(0xFF, 1, "Byte"))
        '0xff'
        >>> hex(right_shift_arithmetic(0x7F, 1, "Byte"))
        '0x3f'
    """
    bits = get_size_bits(size)
    shift_amount = shift_amount % bits
    a = apply_size_mask(a, size)

    # Check sign bit
    sign_bit = 1 << (bits - 1)
    is_negative = (a & sign_bit) != 0

    # Perform logical shift
    result = a >> shift_amount

    # If negative, fill with 1s from the left
    if is_negative:
        # Create mask of 1s for the shifted positions
        mask = ((1 << shift_amount) - 1) << (bits - shift_amount)
        result |= mask

    return apply_size_mask(result, size)


def rotate_left(a: int, shift_amount: int, size: Size) -> int:
    """Circular left rotate.

    Args:
        a: Value to rotate
        shift_amount: Number of positions to rotate
        size: Integer size

    Returns:
        Value rotated left (bits wrap around)

    Examples:
        >>> hex(rotate_left(0x81, 1, "Byte"))
        '0x3'
        >>> hex(rotate_left(0xFF, 4, "Byte"))
        '0xff'
    """
    bits = get_size_bits(size)
    shift_amount = shift_amount % bits
    a = apply_size_mask(a, size)

    # Rotate: shift left and bring wrapped bits to right
    result = ((a << shift_amount) | (a >> (bits - shift_amount)))
    return apply_size_mask(result, size)


def rotate_right(a: int, shift_amount: int, size: Size) -> int:
    """Circular right rotate.

    Args:
        a: Value to rotate
        shift_amount: Number of positions to rotate
        size: Integer size

    Returns:
        Value rotated right (bits wrap around)

    Examples:
        >>> hex(rotate_right(0x81, 1, "Byte"))
        '0xc0'
        >>> hex(rotate_right(0xFF, 4, "Byte"))
        '0xff'
    """
    bits = get_size_bits(size)
    shift_amount = shift_amount % bits
    a = apply_size_mask(a, size)

    # Rotate: shift right and bring wrapped bits to left
    result = ((a >> shift_amount) | (a << (bits - shift_amount)))
    return apply_size_mask(result, size)


def rotate_through_carry_left(a: int, shift_amount: int, carry: bool, size: Size) -> tuple[int, bool]:
    """Rotate left through carry.

    Args:
        a: Value to rotate
        shift_amount: Number of positions to rotate
        carry: Current carry flag state
        size: Integer size

    Returns:
        Tuple of (result, new_carry_flag)

    Examples:
        >>> hex(rotate_through_carry_left(0x81, 1, False, "Byte")[0])
        '0x2'
        >>> rotate_through_carry_left(0x81, 1, False, "Byte")[1]
        True
    """
    bits = get_size_bits(size)
    shift_amount = shift_amount % (bits + 1)  # +1 because carry is part of rotation
    a = apply_size_mask(a, size)

    # For simplicity, rotate one bit at a time
    for _ in range(shift_amount):
        # Get bit that will be shifted out
        msb = (a >> (bits - 1)) & 1
        # Shift left
        a = (a << 1) & get_size_mask(size)
        # Insert carry at LSB
        if carry:
            a |= 1
        # Update carry with shifted-out bit
        carry = bool(msb)

    return a, carry


def rotate_through_carry_right(a: int, shift_amount: int, carry: bool, size: Size) -> tuple[int, bool]:
    """Rotate right through carry.

    Args:
        a: Value to rotate
        shift_amount: Number of positions to rotate
        carry: Current carry flag state
        size: Integer size

    Returns:
        Tuple of (result, new_carry_flag)

    Examples:
        >>> hex(rotate_through_carry_right(0x81, 1, False, "Byte")[0])
        '0x40'
        >>> rotate_through_carry_right(0x81, 1, False, "Byte")[1]
        True
    """
    bits = get_size_bits(size)
    shift_amount = shift_amount % (bits + 1)
    a = apply_size_mask(a, size)

    # Rotate one bit at a time
    for _ in range(shift_amount):
        # Get bit that will be shifted out
        lsb = a & 1
        # Shift right
        a = a >> 1
        # Insert carry at MSB
        if carry:
            a |= (1 << (bits - 1))
        # Update carry with shifted-out bit
        carry = bool(lsb)

    return a, carry


def get_bit_at(value: int, position: int) -> bool:
    """Read a single bit at the specified position.

    Args:
        value: Integer value
        position: Bit position (0 = LSB)

    Returns:
        True if bit is 1, False if bit is 0

    Examples:
        >>> get_bit_at(0xFF, 0)
        True
        >>> get_bit_at(0xFF, 8)
        False
    """
    return bool((value >> position) & 1)


def set_bit_at(value: int, position: int, bit_value: bool, size: Size) -> int:
    """Set a single bit at the specified position.

    Args:
        value: Integer value
        position: Bit position (0 = LSB)
        bit_value: True to set bit to 1, False to set to 0
        size: Integer size

    Returns:
        Value with modified bit, truncated to size

    Examples:
        >>> hex(set_bit_at(0x00, 0, True, "Byte"))
        '0x1'
        >>> hex(set_bit_at(0xFF, 0, False, "Byte"))
        '0xfe'
    """
    if bit_value:
        # Set bit to 1
        result = value | (1 << position)
    else:
        # Set bit to 0
        result = value & ~(1 << position)
    return apply_size_mask(result, size)


def get_changed_bits(old_value: int, new_value: int, size: Size) -> list[int]:
    """Get list of bit positions that changed between two values.

    Args:
        old_value: Previous value
        new_value: New value
        size: Integer size

    Returns:
        List of bit positions that changed (0 = LSB)

    Examples:
        >>> get_changed_bits(0x00, 0xFF, "Byte")
        [0, 1, 2, 3, 4, 5, 6, 7]
        >>> get_changed_bits(0x0F, 0xF0, "Byte")
        [0, 1, 2, 3, 4, 5, 6, 7]
    """
    old_value = apply_size_mask(old_value, size)
    new_value = apply_size_mask(new_value, size)
    xor_result = old_value ^ new_value

    changed = []
    bits = get_size_bits(size)
    for i in range(bits):
        if (xor_result >> i) & 1:
            changed.append(i)
    return changed
