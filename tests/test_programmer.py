"""Tests for programmer mode operations."""

import pytest
from calculator import programmer


class TestUtilityFunctions:
    """Tests for utility functions."""

    @pytest.mark.parametrize(
        "size,expected_bits",
        [
            ("Byte", 8),
            ("Word", 16),
            ("DWord", 32),
            ("QWord", 64),
        ],
    )
    def test_get_size_bits(self, size, expected_bits):
        """Test that get_size_bits returns correct bit widths."""
        assert programmer.get_size_bits(size) == expected_bits

    @pytest.mark.parametrize(
        "size,expected_mask",
        [
            ("Byte", 0xFF),
            ("Word", 0xFFFF),
            ("DWord", 0xFFFFFFFF),
            ("QWord", 0xFFFFFFFFFFFFFFFF),
        ],
    )
    def test_get_size_mask(self, size, expected_mask):
        """Test that get_size_mask returns correct masks."""
        assert programmer.get_size_mask(size) == expected_mask

    @pytest.mark.parametrize(
        "value,size,expected",
        [
            (0x1234, "Byte", 0x34),
            (0x12345678, "Word", 0x5678),
            (0x123456789ABCDEF0, "DWord", 0x9ABCDEF0),
            (-1, "Byte", 0xFF),
            (-1, "Word", 0xFFFF),
        ],
    )
    def test_apply_size_mask(self, value, size, expected):
        """Test size truncation with two's complement."""
        assert programmer.apply_size_mask(value, size) == expected


class TestBaseConversion:
    """Tests for base conversion functions."""

    @pytest.mark.parametrize(
        "value,base,size,expected",
        [
            (255, "HEX", "Byte", "0xFF"),
            (255, "DEC", "Byte", "255"),
            (255, "OCT", "Byte", "0o377"),
            (255, "BIN", "Byte", "0b1111 1111"),
            (0x1234, "HEX", "Word", "0x1234"),
            (15, "BIN", "Byte", "0b0000 1111"),
        ],
    )
    def test_convert_to_base(self, value, base, size, expected):
        """Test conversion to various bases with proper formatting."""
        assert programmer.convert_to_base(value, base, size) == expected

    @pytest.mark.parametrize(
        "value_str,base,expected",
        [
            ("0xFF", "HEX", 255),
            ("FF", "HEX", 255),
            ("255", "DEC", 255),
            ("0o377", "OCT", 255),
            ("377", "OCT", 255),
            ("0b11111111", "BIN", 255),
            ("11111111", "BIN", 255),
            ("0b1111 1111", "BIN", 255),  # With spaces
        ],
    )
    def test_parse_base_input(self, value_str, base, expected):
        """Test parsing strings in various bases."""
        assert programmer.parse_base_input(value_str, base) == expected

    def test_parse_base_input_invalid(self):
        """Test that invalid base input raises ValueError."""
        with pytest.raises(ValueError):
            programmer.parse_base_input("GG", "HEX")
        with pytest.raises(ValueError):
            programmer.parse_base_input("999", "OCT")

    @pytest.mark.parametrize(
        "value,new_digit,base,size,expected_overflow",
        [
            (0xFF, "F", "HEX", "Byte", True),  # Would overflow
            (0xF, "F", "HEX", "Byte", False),  # OK
            (255, "9", "DEC", "Byte", True),  # Would overflow
            (25, "5", "DEC", "Byte", False),  # OK
        ],
    )
    def test_check_overflow(self, value, new_digit, base, size, expected_overflow):
        """Test overflow detection during digit entry."""
        assert programmer.check_overflow(value, new_digit, base, size) == expected_overflow


class TestBitwiseAnd:
    """Tests for bitwise AND operation."""

    @pytest.mark.parametrize(
        "a,b,size,expected",
        [
            (0xFF, 0x0F, "Byte", 0x0F),
            (0xFFFF, 0x00FF, "Word", 0x00FF),
            (0xF0F0F0F0, 0x0F0F0F0F, "DWord", 0x00000000),
            (255, 15, "Byte", 15),
        ],
    )
    def test_and_operations(self, a, b, size, expected):
        """Test AND with various inputs and sizes."""
        assert programmer.bitwise_and(a, b, size) == expected

    def test_and_size_truncation(self):
        """Test that AND result is truncated to size."""
        # 0xFFFF AND 0xFFFF should truncate to 0xFF in Byte mode
        assert programmer.bitwise_and(0xFFFF, 0xFFFF, "Byte") == 0xFF


class TestBitwiseOr:
    """Tests for bitwise OR operation."""

    @pytest.mark.parametrize(
        "a,b,size,expected",
        [
            (0xF0, 0x0F, "Byte", 0xFF),
            (0xFF00, 0x00FF, "Word", 0xFFFF),
            (0, 0, "Byte", 0),
            (240, 15, "Byte", 255),
        ],
    )
    def test_or_operations(self, a, b, size, expected):
        """Test OR with various inputs and sizes."""
        assert programmer.bitwise_or(a, b, size) == expected


class TestBitwiseXor:
    """Tests for bitwise XOR operation."""

    @pytest.mark.parametrize(
        "a,b,size,expected",
        [
            (0xFF, 0x0F, "Byte", 0xF0),
            (0xFF, 0xFF, "Byte", 0x00),
            (0xAAAA, 0x5555, "Word", 0xFFFF),
            (255, 15, "Byte", 240),
        ],
    )
    def test_xor_operations(self, a, b, size, expected):
        """Test XOR with various inputs and sizes."""
        assert programmer.bitwise_xor(a, b, size) == expected


class TestBitwiseNand:
    """Tests for bitwise NAND operation."""

    @pytest.mark.parametrize(
        "a,b,size,expected",
        [
            (0xFF, 0x0F, "Byte", 0xF0),
            (0xFF, 0xFF, "Byte", 0x00),
            (0x00, 0x00, "Byte", 0xFF),
            (255, 15, "Byte", 240),
        ],
    )
    def test_nand_operations(self, a, b, size, expected):
        """Test NAND with various inputs and sizes."""
        assert programmer.bitwise_nand(a, b, size) == expected


class TestBitwiseNor:
    """Tests for bitwise NOR operation."""

    @pytest.mark.parametrize(
        "a,b,size,expected",
        [
            (0xF0, 0x0F, "Byte", 0x00),
            (0x00, 0x00, "Byte", 0xFF),
            (0xFF, 0xFF, "Byte", 0x00),
            (240, 15, "Byte", 0),
        ],
    )
    def test_nor_operations(self, a, b, size, expected):
        """Test NOR with various inputs and sizes."""
        assert programmer.bitwise_nor(a, b, size) == expected


class TestBitwiseNot:
    """Tests for bitwise NOT (unary) operation."""

    @pytest.mark.parametrize(
        "a,size,expected",
        [
            (0x0F, "Byte", 0xF0),
            (0x0F, "Word", 0xFFF0),
            (0x0F, "DWord", 0xFFFFFFF0),
            (0, "Byte", 0xFF),
            (0xFF, "Byte", 0x00),
        ],
    )
    def test_not_operations(self, a, size, expected):
        """Test NOT with various sizes showing size-dependent results."""
        assert programmer.bitwise_not(a, size) == expected


class TestLeftShift:
    """Tests for left shift operation."""

    @pytest.mark.parametrize(
        "a,shift,size,expected",
        [
            (0x0F, 4, "Byte", 0xF0),
            (0xFF, 1, "Byte", 0xFE),
            (0x01, 7, "Byte", 0x80),
            (1, 0, "Byte", 1),  # No shift
            (0xFF, 8, "Byte", 0xFF),  # Wrap around (8 % 8 = 0)
        ],
    )
    def test_left_shift_operations(self, a, shift, size, expected):
        """Test left shift with various shift amounts."""
        assert programmer.left_shift(a, shift, size) == expected

    def test_left_shift_overflow(self):
        """Test that left shift overflow is truncated."""
        # 0xFF << 1 = 0x1FE, truncated to 0xFE in Byte mode
        assert programmer.left_shift(0xFF, 1, "Byte") == 0xFE


class TestRightShiftLogical:
    """Tests for logical right shift."""

    @pytest.mark.parametrize(
        "a,shift,size,expected",
        [
            (0xFF, 1, "Byte", 0x7F),
            (0xF0, 4, "Byte", 0x0F),
            (0x80, 1, "Byte", 0x40),  # No sign extension
            (0xFF, 8, "Byte", 0xFF),  # Wrap around (8 % 8 = 0)
        ],
    )
    def test_right_shift_logical_operations(self, a, shift, size, expected):
        """Test logical right shift (zero-fill)."""
        assert programmer.right_shift_logical(a, shift, size) == expected


class TestRightShiftArithmetic:
    """Tests for arithmetic right shift."""

    @pytest.mark.parametrize(
        "a,shift,size,expected",
        [
            (0xFF, 1, "Byte", 0xFF),  # Sign bit extends
            (0x7F, 1, "Byte", 0x3F),  # Positive, no extension
            (0x80, 1, "Byte", 0xC0),  # Negative (sign bit set)
            (0xF0, 4, "Byte", 0xFF),  # Sign extends
        ],
    )
    def test_right_shift_arithmetic_operations(self, a, shift, size, expected):
        """Test arithmetic right shift (sign-extend)."""
        assert programmer.right_shift_arithmetic(a, shift, size) == expected


class TestRotateLeft:
    """Tests for circular left rotate."""

    @pytest.mark.parametrize(
        "a,shift,size,expected",
        [
            (0x81, 1, "Byte", 0x03),
            (0xFF, 4, "Byte", 0xFF),
            (0x01, 1, "Byte", 0x02),
            (0x80, 1, "Byte", 0x01),  # Wrap around
        ],
    )
    def test_rotate_left_operations(self, a, shift, size, expected):
        """Test circular left rotate."""
        assert programmer.rotate_left(a, shift, size) == expected


class TestRotateRight:
    """Tests for circular right rotate."""

    @pytest.mark.parametrize(
        "a,shift,size,expected",
        [
            (0x81, 1, "Byte", 0xC0),
            (0xFF, 4, "Byte", 0xFF),
            (0x01, 1, "Byte", 0x80),  # Wrap around
        ],
    )
    def test_rotate_right_operations(self, a, shift, size, expected):
        """Test circular right rotate."""
        assert programmer.rotate_right(a, shift, size) == expected


class TestRotateThroughCarryLeft:
    """Tests for rotate through carry left."""

    def test_rotate_through_carry_left_no_carry(self):
        """Test RCL with carry=False."""
        result, new_carry = programmer.rotate_through_carry_left(0x81, 1, False, "Byte")
        assert result == 0x02
        assert new_carry is True

    def test_rotate_through_carry_left_with_carry(self):
        """Test RCL with carry=True."""
        result, new_carry = programmer.rotate_through_carry_left(0x80, 1, True, "Byte")
        assert result == 0x01
        assert new_carry is True

    def test_rotate_through_carry_left_no_msb(self):
        """Test RCL when MSB is 0."""
        result, new_carry = programmer.rotate_through_carry_left(0x01, 1, False, "Byte")
        assert result == 0x02
        assert new_carry is False


class TestRotateThroughCarryRight:
    """Tests for rotate through carry right."""

    def test_rotate_through_carry_right_no_carry(self):
        """Test RCR with carry=False."""
        result, new_carry = programmer.rotate_through_carry_right(0x81, 1, False, "Byte")
        assert result == 0x40
        assert new_carry is True

    def test_rotate_through_carry_right_with_carry(self):
        """Test RCR with carry=True."""
        result, new_carry = programmer.rotate_through_carry_right(0x01, 1, True, "Byte")
        assert result == 0x80
        assert new_carry is True

    def test_rotate_through_carry_right_no_lsb(self):
        """Test RCR when LSB is 0."""
        result, new_carry = programmer.rotate_through_carry_right(0x02, 1, False, "Byte")
        assert result == 0x01
        assert new_carry is False


class TestBitManipulation:
    """Tests for bit manipulation utilities."""

    @pytest.mark.parametrize(
        "value,position,expected",
        [
            (0xFF, 0, True),
            (0xFF, 7, True),
            (0xFF, 8, False),
            (0x00, 0, False),
            (0x01, 0, True),
            (0x01, 1, False),
        ],
    )
    def test_get_bit_at(self, value, position, expected):
        """Test reading individual bits."""
        assert programmer.get_bit_at(value, position) == expected

    @pytest.mark.parametrize(
        "value,position,bit_value,size,expected",
        [
            (0x00, 0, True, "Byte", 0x01),
            (0xFF, 0, False, "Byte", 0xFE),
            (0x00, 7, True, "Byte", 0x80),
            (0xFF, 7, False, "Byte", 0x7F),
        ],
    )
    def test_set_bit_at(self, value, position, bit_value, size, expected):
        """Test setting individual bits."""
        assert programmer.set_bit_at(value, position, bit_value, size) == expected

    @pytest.mark.parametrize(
        "old_value,new_value,size,expected_changes",
        [
            (0x00, 0xFF, "Byte", [0, 1, 2, 3, 4, 5, 6, 7]),
            (0x0F, 0xF0, "Byte", [0, 1, 2, 3, 4, 5, 6, 7]),
            (0xFF, 0xFF, "Byte", []),
            (0x00, 0x01, "Byte", [0]),
            (0x01, 0x00, "Byte", [0]),
        ],
    )
    def test_get_changed_bits(self, old_value, new_value, size, expected_changes):
        """Test detecting changed bits between values."""
        assert programmer.get_changed_bits(old_value, new_value, size) == expected_changes
