"""Tests for programmer mode expression parser."""

import pytest
from calculator import programmer_parser


class TestParseLiteral:
    """Tests for parse_base_literal function."""

    @pytest.mark.parametrize(
        "token,expected_value,expected_base",
        [
            ("0xFF", 255, "HEX"),
            ("0xff", 255, "HEX"),
            ("0XFF", 255, "HEX"),
            ("0x1234", 0x1234, "HEX"),
            ("0o377", 255, "OCT"),
            ("0O377", 255, "OCT"),
            ("0o777", 511, "OCT"),
            ("0b11111111", 255, "BIN"),
            ("0B11111111", 255, "BIN"),
            ("0b1010", 10, "BIN"),
            ("255", 255, "DEC"),
            ("1234", 1234, "DEC"),
            ("0", 0, "DEC"),
        ],
    )
    def test_parse_base_literal_valid(self, token, expected_value, expected_base):
        """Test parsing various base literals."""
        value, base = programmer_parser.parse_base_literal(token)
        assert value == expected_value
        assert base == expected_base

    @pytest.mark.parametrize(
        "token",
        [
            "0xGG",  # Invalid hex
            "0o999",  # Invalid octal
            "0b222",  # Invalid binary
            "GHI",  # Invalid - contains non-hex letters
        ],
    )
    def test_parse_base_literal_invalid(self, token):
        """Test that invalid literals raise ValueError."""
        with pytest.raises(ValueError):
            programmer_parser.parse_base_literal(token)


class TestTokenize:
    """Tests for tokenize_expression function."""

    @pytest.mark.parametrize(
        "expr,expected_tokens",
        [
            ("0xFF AND 0x0F", ["0xFF", "AND", "0x0F"]),
            ("0xFF & 0x0F", ["0xFF", "&", "0x0F"]),
            ("255 + 15", ["255", "+", "15"]),
            ("(0xFF & 0x0F) | 0x10", ["(", "0xFF", "&", "0x0F", ")", "|", "0x10"]),
            ("NOT 0xFF", ["NOT", "0xFF"]),
            ("0xFF << 2", ["0xFF", "<<", "2"]),
            ("0xFF >> 2", ["0xFF", ">>", "2"]),
            ("0b1010 XOR 0b0101", ["0b1010", "XOR", "0b0101"]),
        ],
    )
    def test_tokenize_expression(self, expr, expected_tokens):
        """Test expression tokenization."""
        tokens = programmer_parser.tokenize_expression(expr)
        assert tokens == expected_tokens


class TestNormalizeOperator:
    """Tests for normalize_operator function."""

    @pytest.mark.parametrize(
        "operator,expected",
        [
            ("&", "AND"),
            ("|", "OR"),
            ("^", "XOR"),
            ("~", "NOT"),
            ("AND", "AND"),
            ("OR", "OR"),
            ("XOR", "XOR"),
            ("<<", "<<"),
            (">>", ">>"),
            ("+", "+"),
            ("-", "-"),
            ("*", "*"),
            ("/", "/"),
            ("%", "%"),
        ],
    )
    def test_normalize_operator(self, operator, expected):
        """Test operator normalization."""
        assert programmer_parser.normalize_operator(operator) == expected


class TestEvaluateSimpleExpressions:
    """Tests for simple expression evaluation."""

    def test_single_hex_number(self):
        """Test that a single hex number returns itself."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression("0xFF", "Byte")
        assert result == 255
        assert carry is False

    def test_single_decimal_number(self):
        """Test that a single decimal number returns itself."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression("255", "Byte")
        assert result == 255
        assert carry is False

    def test_unary_not(self):
        """Test unary NOT operation."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression("NOT 0x0F", "Byte")
        assert result == 0xF0
        assert carry is False


class TestBitwiseExpressions:
    """Tests for bitwise operation expressions."""

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            ("0xFF AND 0x0F", "Byte", 0x0F),
            ("0xFF & 0x0F", "Byte", 0x0F),
            ("0xF0 OR 0x0F", "Byte", 0xFF),
            ("0xF0 | 0x0F", "Byte", 0xFF),
            ("0xFF XOR 0x0F", "Byte", 0xF0),
            ("0xFF ^ 0x0F", "Byte", 0xF0),
            ("0xFF NAND 0x0F", "Byte", 0xF0),
            ("0xF0 NOR 0x0F", "Byte", 0x00),
        ],
    )
    def test_bitwise_operations(self, expression, size, expected_result):
        """Test various bitwise operations."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    def test_mixed_bases(self):
        """Test expression with mixed number bases."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "0xFF AND 255", "Byte"
        )
        assert result == 255


class TestShiftExpressions:
    """Tests for shift operation expressions."""

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            ("0x0F << 4", "Byte", 0xF0),
            ("0xFF << 1", "Byte", 0xFE),
            ("0xFF >> 1", "Byte", 0x7F),
            ("0xF0 >> 4", "Byte", 0x0F),
            ("1 << 7", "Byte", 0x80),
        ],
    )
    def test_shift_operations(self, expression, size, expected_result):
        """Test shift operations."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result


class TestArithmeticExpressions:
    """Tests for arithmetic operation expressions."""

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            ("0x0F + 0x01", "Byte", 0x10),
            ("0x10 - 0x01", "Byte", 0x0F),
            ("0x10 * 2", "Byte", 0x20),
            ("0xFF / 2", "Byte", 0x7F),
            ("0xFF % 16", "Byte", 0x0F),
        ],
    )
    def test_arithmetic_operations(self, expression, size, expected_result):
        """Test arithmetic operations."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    def test_division_by_zero(self):
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Division by zero"):
            programmer_parser.evaluate_programmer_expression("0xFF / 0", "Byte")


class TestLeftToRightEvaluation:
    """Tests for left-to-right evaluation order."""

    def test_left_to_right_and_or(self):
        """Test that evaluation is left-to-right, not standard precedence."""
        # Left-to-right: (0x0F AND 0xFF) OR 0x10 = 0x0F OR 0x10 = 0x1F
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "0x0F AND 0xFF OR 0x10", "Byte"
        )
        assert result == 0x1F

    def test_left_to_right_arithmetic(self):
        """Test left-to-right with arithmetic."""
        # Left-to-right: (10 + 5) * 2 = 15 * 2 = 30
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "10 + 5 * 2", "Byte"
        )
        assert result == 30


class TestParentheses:
    """Tests for parentheses support."""

    def test_simple_parentheses(self):
        """Test simple parenthesized expression."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "(0xFF AND 0x0F)", "Byte"
        )
        assert result == 0x0F

    def test_nested_parentheses(self):
        """Test nested parentheses."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "((0xFF AND 0x0F) OR 0x10)", "Byte"
        )
        assert result == 0x1F

    def test_multiple_parenthesized_groups(self):
        """Test multiple parenthesized groups."""
        # (0xFF AND 0x0F) = 0x0F, (0x10 XOR 0x20) = 0x30
        # 0x0F OR 0x30 = 0x3F
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "(0xFF AND 0x0F) OR (0x10 XOR 0x20)", "Byte"
        )
        assert result == 0x3F

    def test_parentheses_override_left_to_right(self):
        """Test that parentheses override left-to-right evaluation."""
        # Without parens (left-to-right): (0x0F AND 0xFF) OR 0x10 = 0x1F
        # With parens: 0x0F AND (0xFF OR 0x10) = 0x0F AND 0xFF = 0x0F
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "0x0F AND (0xFF OR 0x10)", "Byte"
        )
        assert result == 0x0F

    def test_unmatched_opening_paren(self):
        """Test that unmatched opening parenthesis raises ValueError."""
        with pytest.raises(ValueError, match="Unmatched"):
            programmer_parser.evaluate_programmer_expression("(0xFF AND 0x0F", "Byte")

    def test_unmatched_closing_paren(self):
        """Test that unmatched closing parenthesis raises ValueError."""
        with pytest.raises(ValueError):
            programmer_parser.evaluate_programmer_expression("0xFF AND 0x0F)", "Byte")


class TestIntegerSizes:
    """Tests that operations respect integer size."""

    def test_byte_truncation(self):
        """Test that Byte size truncates to 8 bits."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "0xFFFF AND 0xFFFF", "Byte"
        )
        assert result == 0xFF

    def test_word_truncation(self):
        """Test that Word size truncates to 16 bits."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "0xFFFFFFFF AND 0xFFFFFFFF", "Word"
        )
        assert result == 0xFFFF

    def test_dword_no_truncation(self):
        """Test that DWord handles 32-bit values."""
        expr, result, carry = programmer_parser.evaluate_programmer_expression(
            "0xFFFFFFFF AND 0xFFFFFFFF", "DWord"
        )
        assert result == 0xFFFFFFFF


class TestNormalizedExpression:
    """Tests for normalized expression output."""

    def test_normalized_hex_format(self):
        """Test that normalized expression uses proper hex format."""
        normalized, result, carry = programmer_parser.evaluate_programmer_expression(
            "0xff and 0x0f", "Byte"
        )
        assert "0xFF" in normalized or "0xF" in normalized
        assert "AND" in normalized

    def test_normalized_preserves_structure(self):
        """Test that normalized expression preserves operation structure."""
        normalized, result, carry = programmer_parser.evaluate_programmer_expression(
            "0xFF AND 0x0F OR 0x10", "Byte"
        )
        # Should contain all three operands and two operators
        assert "0xFF" in normalized or "0xF" in normalized
        assert "AND" in normalized
        assert "OR" in normalized


class TestErrorHandling:
    """Tests for error handling."""

    def test_empty_expression(self):
        """Test that empty expression raises ValueError."""
        with pytest.raises(ValueError, match="Empty expression"):
            programmer_parser.evaluate_programmer_expression("", "Byte")

    def test_missing_operand(self):
        """Test that missing operand raises ValueError."""
        with pytest.raises(ValueError, match="Missing operand"):
            programmer_parser.evaluate_programmer_expression("0xFF AND", "Byte")

    def test_unknown_operator(self):
        """Test that unknown operator raises ValueError."""
        # The tokenizer will skip "UNKNOWN", so the expression becomes "0xFF 0x0F"
        # which will fail because there's no operator between them
        with pytest.raises(ValueError):
            programmer_parser.evaluate_programmer_expression("0xFF UNKNOWN 0x0F", "Byte")


class TestGUIButtonInput:
    """Tests for expressions built from GUI button clicks (no prefixes).

    These tests simulate actual user input patterns from the calculator GUI,
    where users click digit buttons and operators without typing prefixes.
    """

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # HEX mode: raw hex digits without 0x prefix
            ("A AND B", "Byte", 0x0A & 0x0B),
            ("A OR B", "Byte", 0x0A | 0x0B),
            ("A XOR B", "Byte", 0x0A ^ 0x0B),
            ("A NOR B", "Byte", (~(0x0A | 0x0B)) & 0xFF),
            ("A NAND B", "Byte", (~(0x0A & 0x0B)) & 0xFF),
            ("FF AND 0F", "Byte", 0x0F),
            ("FF OR 0F", "Byte", 0xFF),
            ("C0 XOR 3F", "Byte", 0xC0 ^ 0x3F),
            ("DEAD AND BEEF", "DWord", 0xDEAD & 0xBEEF),
        ],
    )
    def test_hex_mode_raw_input(self, expression, size, expected_result):
        """Test HEX mode expressions without 0x prefix (GUI button input)."""
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # DEC mode: decimal digits
            ("10 AND 15", "Byte", 10 & 15),
            ("255 OR 128", "Byte", 255 | 128),
            ("100 XOR 50", "Byte", 100 ^ 50),
            ("200 + 55", "Byte", 255),
            ("100 - 25", "Byte", 75),
        ],
    )
    def test_dec_mode_input(self, expression, size, expected_result):
        """Test DEC mode expressions (GUI button input)."""
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # BIN mode: binary digits (parsed as decimal, which is correct for raw input)
            # Note: In BIN mode GUI, "110" means binary 110 = 6 decimal
            # But the parser sees raw digits, so we test that parsing works
            ("110 AND 111", "Byte", 110 & 111),  # Parsed as decimal
            ("101 OR 010", "Byte", 101 | 10),    # Parsed as decimal
            ("111 XOR 101", "Byte", 111 ^ 101),
        ],
    )
    def test_bin_mode_raw_input(self, expression, size, expected_result):
        """Test expressions with binary-looking digits (GUI button input).

        Note: Without 0b prefix, these are parsed as decimal numbers.
        The GUI should add 0b prefix for proper binary interpretation.
        """
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # Shift operations from GUI
            ("F0 << 2", "Byte", (0xF0 << 2) & 0xFF),
            ("FF >> 4", "Byte", 0xFF >> 4),
            ("80 >> 1", "Byte", 80 >> 1),  # 80 without hex letters = decimal
            ("1 << 7", "Byte", 0x80),
            ("A0 >> 1", "Byte", 0xA0 >> 1),  # A0 has hex letter = hex
        ],
    )
    def test_shift_operations_raw_input(self, expression, size, expected_result):
        """Test shift operations with raw hex digits (GUI button input)."""
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # Unary NOT from GUI
            ("NOT F", "Byte", 0xF0),
            ("NOT 0", "Byte", 0xFF),
            ("NOT FF", "Byte", 0x00),
            ("NOT A5", "Byte", 0x5A),
        ],
    )
    def test_not_operation_raw_input(self, expression, size, expected_result):
        """Test NOT operation with raw hex digits (GUI button input)."""
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # Chained operations from GUI
            ("A AND B OR C", "Byte", (0x0A & 0x0B) | 0x0C),
            ("FF AND F0 AND 0F", "Byte", 0xFF & 0xF0 & 0x0F),
            ("10 + 20 + 30", "Byte", 60),
            ("A XOR B XOR C", "Byte", 0x0A ^ 0x0B ^ 0x0C),
        ],
    )
    def test_chained_operations_raw_input(self, expression, size, expected_result):
        """Test chained operations with raw hex digits (GUI button input)."""
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result

    @pytest.mark.parametrize(
        "expression,size,expected_result",
        [
            # Parentheses with raw hex input
            ("(A AND B) OR C", "Byte", (0x0A & 0x0B) | 0x0C),
            ("A AND (B OR C)", "Byte", 0x0A & (0x0B | 0x0C)),
            ("(FF AND F0) XOR 0F", "Byte", (0xFF & 0xF0) ^ 0x0F),
            ("((A OR B) AND C)", "Byte", (0x0A | 0x0B) & 0x0C),
        ],
    )
    def test_parentheses_raw_input(self, expression, size, expected_result):
        """Test parentheses with raw hex digits (GUI button input)."""
        _, result, _ = programmer_parser.evaluate_programmer_expression(expression, size)
        assert result == expected_result


class TestTokenizerEdgeCases:
    """Tests for tokenizer edge cases discovered during integration."""

    def test_operator_not_split_as_hex(self):
        """Ensure AND/OR/etc are not split into hex digits A, D, etc."""
        tokens = programmer_parser.tokenize_expression("FF AND 0F")
        assert tokens == ["FF", "AND", "0F"]
        assert "A" not in tokens
        assert "D" not in tokens

    def test_nand_not_split(self):
        """Ensure NAND is not split (contains A and D)."""
        tokens = programmer_parser.tokenize_expression("FF NAND 0F")
        assert tokens == ["FF", "NAND", "0F"]

    def test_nor_not_split(self):
        """Ensure NOR is not split."""
        tokens = programmer_parser.tokenize_expression("A NOR B")
        assert tokens == ["A", "NOR", "B"]

    def test_single_hex_digit(self):
        """Test single hex digit tokenization."""
        for digit in "0123456789ABCDEF":
            tokens = programmer_parser.tokenize_expression(digit)
            assert tokens == [digit], f"Failed for digit {digit}"

    def test_mixed_case_operators(self):
        """Test that operators work in any case."""
        for op in ["and", "AND", "And", "aNd"]:
            tokens = programmer_parser.tokenize_expression(f"A {op} B")
            assert tokens[1] == "AND", f"Failed for operator {op}"
