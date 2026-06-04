"""Tests for calculator.converter module.

Comprehensive test coverage for the unit conversion functionality,
covering all 8 categories, edge cases, and error conditions.
"""

import math

import pytest

from calculator import converter


class TestConvertLength:
    """Tests for length unit conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Basic conversions
            (1, "meter", "foot", pytest.approx(3.28084, rel=1e-5)),
            (1, "foot", "meter", pytest.approx(0.3048, rel=1e-5)),
            (1, "kilometer", "mile", pytest.approx(0.621371, rel=1e-5)),
            (1, "mile", "kilometer", pytest.approx(1.609344, rel=1e-6)),
            (1, "inch", "centimeter", pytest.approx(2.54, rel=1e-5)),
            (1, "yard", "meter", pytest.approx(0.9144, rel=1e-5)),
            (1, "nautical mile", "kilometer", pytest.approx(1.852, rel=1e-5)),
            # Multi-step conversions (always through base unit)
            (12, "inch", "foot", pytest.approx(1.0, rel=1e-5)),
            (3, "foot", "yard", pytest.approx(1.0, rel=1e-5)),
            (1000, "meter", "kilometer", pytest.approx(1.0, rel=1e-5)),
            (100, "centimeter", "meter", pytest.approx(1.0, rel=1e-5)),
            (1000, "millimeter", "meter", pytest.approx(1.0, rel=1e-5)),
            # Large values
            (1000000, "meter", "kilometer", pytest.approx(1000.0, rel=1e-5)),
            # Small values
            (0.001, "meter", "millimeter", pytest.approx(1.0, rel=1e-5)),
            # Zero
            (0, "meter", "foot", 0.0),
            # Negative values
            (-1, "meter", "foot", pytest.approx(-3.28084, rel=1e-5)),
        ],
    )
    def test_length_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test length conversions with various unit combinations."""
        result = converter.convert(value, from_unit, to_unit, "Length")
        assert result == expected


class TestConvertWeight:
    """Tests for weight/mass unit conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Basic conversions
            (1, "kilogram", "pound", pytest.approx(2.20462, rel=1e-5)),
            (1, "pound", "kilogram", pytest.approx(0.45359237, rel=1e-6)),
            (1, "kilogram", "gram", pytest.approx(1000.0, rel=1e-5)),
            (1, "gram", "milligram", pytest.approx(1000.0, rel=1e-5)),
            (1, "metric ton", "kilogram", pytest.approx(1000.0, rel=1e-5)),
            (1, "ounce", "gram", pytest.approx(28.3495, rel=1e-4)),
            (1, "stone", "pound", pytest.approx(14.0, rel=1e-4)),
            # Multi-step conversions
            (16, "ounce", "pound", pytest.approx(1.0, rel=1e-4)),
            (14, "pound", "stone", pytest.approx(1.0, rel=1e-4)),
            (1000, "gram", "kilogram", pytest.approx(1.0, rel=1e-5)),
            # Zero and negative
            (0, "kilogram", "pound", 0.0),
            (-1, "kilogram", "pound", pytest.approx(-2.20462, rel=1e-5)),
        ],
    )
    def test_weight_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test weight/mass conversions with various unit combinations."""
        result = converter.convert(value, from_unit, to_unit, "Weight")
        assert result == expected


class TestConvertTemperature:
    """Tests for temperature conversions (non-linear)."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Celsius to Fahrenheit
            (0, "Celsius", "Fahrenheit", pytest.approx(32.0, abs=0.01)),
            (100, "Celsius", "Fahrenheit", pytest.approx(212.0, abs=0.01)),
            (-40, "Celsius", "Fahrenheit", pytest.approx(-40.0, abs=0.01)),
            (37, "Celsius", "Fahrenheit", pytest.approx(98.6, abs=0.1)),
            # Fahrenheit to Celsius
            (32, "Fahrenheit", "Celsius", pytest.approx(0.0, abs=0.01)),
            (212, "Fahrenheit", "Celsius", pytest.approx(100.0, abs=0.01)),
            (-40, "Fahrenheit", "Celsius", pytest.approx(-40.0, abs=0.01)),
            (98.6, "Fahrenheit", "Celsius", pytest.approx(37.0, abs=0.1)),
            # Celsius to Kelvin
            (0, "Celsius", "Kelvin", pytest.approx(273.15, abs=0.01)),
            (100, "Celsius", "Kelvin", pytest.approx(373.15, abs=0.01)),
            (-273.15, "Celsius", "Kelvin", pytest.approx(0.0, abs=0.01)),
            # Kelvin to Celsius
            (273.15, "Kelvin", "Celsius", pytest.approx(0.0, abs=0.01)),
            (373.15, "Kelvin", "Celsius", pytest.approx(100.0, abs=0.01)),
            (0, "Kelvin", "Celsius", pytest.approx(-273.15, abs=0.01)),
            # Fahrenheit to Kelvin
            (32, "Fahrenheit", "Kelvin", pytest.approx(273.15, abs=0.01)),
            (-459.67, "Fahrenheit", "Kelvin", pytest.approx(0.0, abs=0.01)),
            # Kelvin to Fahrenheit
            (273.15, "Kelvin", "Fahrenheit", pytest.approx(32.0, abs=0.01)),
            (0, "Kelvin", "Fahrenheit", pytest.approx(-459.67, abs=0.01)),
        ],
    )
    def test_temperature_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test non-linear temperature conversions."""
        result = converter.convert(value, from_unit, to_unit, "Temperature")
        assert result == expected


class TestTemperatureAbsoluteZeroClamping:
    """Tests for absolute zero clamping behavior per spec."""

    def test_celsius_below_absolute_zero_clamped_to_zero_kelvin(self) -> None:
        """Celsius below -273.15 should clamp to 0 K."""
        result = converter.convert(-300, "Celsius", "Kelvin", "Temperature")
        assert result == 0.0

    def test_fahrenheit_below_absolute_zero_clamped_to_zero_kelvin(self) -> None:
        """Fahrenheit below -459.67 should clamp to 0 K."""
        result = converter.convert(-500, "Fahrenheit", "Kelvin", "Temperature")
        assert result == 0.0

    def test_negative_kelvin_clamped_to_zero(self) -> None:
        """Negative Kelvin input should clamp to 0 K."""
        result = converter.convert(-100, "Kelvin", "Kelvin", "Temperature")
        # Same unit returns same value, but if going through conversion:
        # Actually per implementation, same unit returns value unchanged
        # Let's test conversion to different unit
        result = converter.convert(-100, "Kelvin", "Celsius", "Temperature")
        assert result == pytest.approx(-273.15, abs=0.01)  # 0 K in Celsius

    def test_negative_kelvin_to_fahrenheit_clamped(self) -> None:
        """Negative Kelvin to Fahrenheit should give absolute zero F."""
        result = converter.convert(-100, "Kelvin", "Fahrenheit", "Temperature")
        assert result == pytest.approx(-459.67, abs=0.01)  # 0 K in Fahrenheit

    def test_celsius_exactly_at_absolute_zero(self) -> None:
        """Exactly -273.15 C should convert to 0 K."""
        result = converter.convert(-273.15, "Celsius", "Kelvin", "Temperature")
        assert result == pytest.approx(0.0, abs=0.01)


class TestTemperatureSameUnitConversion:
    """Tests for temperature same-unit conversions."""

    @pytest.mark.parametrize(
        "value,unit",
        [
            (25, "Celsius"),
            (77, "Fahrenheit"),
            (300, "Kelvin"),
            (0, "Celsius"),
            (-40, "Fahrenheit"),
        ],
    )
    def test_same_unit_returns_same_value(self, value: float, unit: str) -> None:
        """Same unit conversion should return the original value."""
        result = converter.convert(value, unit, unit, "Temperature")
        assert result == value


class TestConvertVolume:
    """Tests for volume unit conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Basic conversions
            (1, "liter", "milliliter", pytest.approx(1000.0, rel=1e-5)),
            (1, "milliliter", "liter", pytest.approx(0.001, rel=1e-5)),
            (1, "cubic meter", "liter", pytest.approx(1000.0, rel=1e-5)),
            (1, "gallon (US)", "liter", pytest.approx(3.785411784, rel=1e-6)),
            (1, "gallon (UK)", "liter", pytest.approx(4.54609, rel=1e-5)),
            (1, "quart", "pint", pytest.approx(2.0, rel=1e-4)),
            (1, "pint", "cup", pytest.approx(2.0, rel=1e-4)),
            (1, "cup", "fluid ounce", pytest.approx(8.0, rel=1e-3)),
            # Multi-step conversions
            (4, "quart", "gallon (US)", pytest.approx(1.0, rel=1e-3)),
            (2, "pint", "quart", pytest.approx(1.0, rel=1e-3)),
            # Zero
            (0, "liter", "gallon (US)", 0.0),
        ],
    )
    def test_volume_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test volume conversions with various unit combinations."""
        result = converter.convert(value, from_unit, to_unit, "Volume")
        assert result == expected


class TestConvertArea:
    """Tests for area unit conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Basic conversions
            (1, "sq meter", "sq foot", pytest.approx(10.7639, rel=1e-4)),
            (1, "sq foot", "sq meter", pytest.approx(0.09290304, rel=1e-6)),
            (1, "sq kilometer", "sq meter", pytest.approx(1000000.0, rel=1e-5)),
            (1, "hectare", "sq meter", pytest.approx(10000.0, rel=1e-5)),
            (1, "acre", "sq meter", pytest.approx(4046.8564224, rel=1e-6)),
            (1, "sq mile", "acre", pytest.approx(640.0, rel=1e-4)),
            (1, "sq yard", "sq foot", pytest.approx(9.0, rel=1e-4)),
            (1, "sq centimeter", "sq meter", pytest.approx(0.0001, rel=1e-6)),
            # Multi-step conversions
            (640, "acre", "sq mile", pytest.approx(1.0, rel=1e-4)),
            # Zero
            (0, "sq meter", "acre", 0.0),
        ],
    )
    def test_area_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test area conversions with various unit combinations."""
        result = converter.convert(value, from_unit, to_unit, "Area")
        assert result == expected


class TestConvertSpeed:
    """Tests for speed unit conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Basic conversions
            (1, "m/s", "km/h", pytest.approx(3.6, rel=1e-4)),
            (1, "km/h", "m/s", pytest.approx(0.277778, rel=1e-4)),
            (100, "km/h", "mph", pytest.approx(62.1371, rel=1e-4)),
            (60, "mph", "km/h", pytest.approx(96.5606, rel=1e-4)),
            (1, "Mach", "m/s", pytest.approx(343.0, rel=1e-4)),
            (1, "knots", "km/h", pytest.approx(1.852, rel=1e-4)),
            (1, "ft/s", "m/s", pytest.approx(0.3048, rel=1e-5)),
            # Multi-step
            (1, "knots", "mph", pytest.approx(1.15078, rel=1e-4)),
            # Zero
            (0, "km/h", "mph", 0.0),
        ],
    )
    def test_speed_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test speed conversions with various unit combinations."""
        result = converter.convert(value, from_unit, to_unit, "Speed")
        assert result == expected


class TestConvertTime:
    """Tests for time unit conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Basic conversions
            (1, "minute", "second", pytest.approx(60.0, rel=1e-5)),
            (1, "hour", "minute", pytest.approx(60.0, rel=1e-5)),
            (1, "hour", "second", pytest.approx(3600.0, rel=1e-5)),
            (1, "day", "hour", pytest.approx(24.0, rel=1e-5)),
            (1, "week", "day", pytest.approx(7.0, rel=1e-5)),
            (1, "year", "day", pytest.approx(365.0, rel=1e-5)),
            (1000, "millisecond", "second", pytest.approx(1.0, rel=1e-5)),
            (1, "second", "millisecond", pytest.approx(1000.0, rel=1e-5)),
            # Multi-step
            (1, "week", "hour", pytest.approx(168.0, rel=1e-5)),
            (1, "year", "week", pytest.approx(52.1429, rel=1e-4)),
            # Zero
            (0, "hour", "minute", 0.0),
        ],
    )
    def test_time_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test time conversions with various unit combinations."""
        result = converter.convert(value, from_unit, to_unit, "Time")
        assert result == expected


class TestConvertDataDecimal:
    """Tests for decimal (SI) data storage conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Decimal units (powers of 1000)
            (1, "kilobyte", "byte", 1000.0),
            (1, "megabyte", "kilobyte", 1000.0),
            (1, "gigabyte", "megabyte", 1000.0),
            (1, "terabyte", "gigabyte", 1000.0),
            (1, "byte", "kilobyte", 0.001),
            (1, "kilobyte", "megabyte", 0.001),
            (1, "megabyte", "gigabyte", 0.001),
            (1, "gigabyte", "terabyte", 0.001),
            # Multi-step
            (1, "gigabyte", "byte", 1e9),
            (1, "terabyte", "byte", 1e12),
        ],
    )
    def test_decimal_data_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test decimal (SI) data unit conversions."""
        result = converter.convert(value, from_unit, to_unit, "Data")
        assert result == pytest.approx(expected, rel=1e-10)


class TestConvertDataBinary:
    """Tests for binary (IEC) data storage conversions."""

    @pytest.mark.parametrize(
        "value,from_unit,to_unit,expected",
        [
            # Binary units (powers of 1024)
            (1, "kibibyte", "byte", 1024.0),
            (1, "mebibyte", "kibibyte", 1024.0),
            (1, "gibibyte", "mebibyte", 1024.0),
            (1, "tebibyte", "gibibyte", 1024.0),
            (1, "byte", "kibibyte", 1 / 1024),
            (1, "kibibyte", "mebibyte", 1 / 1024),
            (1, "mebibyte", "gibibyte", 1 / 1024),
            (1, "gibibyte", "tebibyte", 1 / 1024),
            # Multi-step
            (1, "gibibyte", "byte", 1024**3),
            (1, "tebibyte", "byte", 1024**4),
        ],
    )
    def test_binary_data_conversions(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ) -> None:
        """Test binary (IEC) data unit conversions."""
        result = converter.convert(value, from_unit, to_unit, "Data")
        assert result == pytest.approx(expected, rel=1e-10)


class TestConvertDataCrossDecimalBinary:
    """Tests for conversions between decimal and binary data units."""

    def test_gigabyte_not_equal_gibibyte(self) -> None:
        """1 GB != 1 GiB in bytes."""
        gb_bytes = converter.convert(1, "gigabyte", "byte", "Data")
        gib_bytes = converter.convert(1, "gibibyte", "byte", "Data")
        assert gb_bytes == 1e9
        assert gib_bytes == 1024**3
        assert gb_bytes != gib_bytes

    def test_megabyte_to_mebibyte(self) -> None:
        """1 MB = 1000000 bytes, 1 MiB = 1048576 bytes."""
        result = converter.convert(1, "megabyte", "mebibyte", "Data")
        expected = 1000000 / 1048576
        assert result == pytest.approx(expected, rel=1e-10)

    def test_terabyte_to_tebibyte(self) -> None:
        """1 TB != 1 TiB."""
        result = converter.convert(1, "terabyte", "tebibyte", "Data")
        expected = 1e12 / (1024**4)
        assert result == pytest.approx(expected, rel=1e-10)


class TestConvertSameUnit:
    """Tests for same-unit conversions per spec."""

    @pytest.mark.parametrize(
        "category,unit,value",
        [
            ("Length", "meter", 42.5),
            ("Length", "foot", 100),
            ("Weight", "kilogram", 75),
            ("Weight", "pound", 165),
            ("Volume", "liter", 2.5),
            ("Area", "sq meter", 100),
            ("Speed", "km/h", 120),
            ("Time", "second", 3600),
            ("Data", "byte", 1024),
            ("Data", "gigabyte", 500),
        ],
    )
    def test_same_unit_returns_unchanged_value(
        self, category: str, unit: str, value: float
    ) -> None:
        """Converting to the same unit should return the original value."""
        result = converter.convert(value, unit, unit, category)
        assert result == value


class TestConvertRoundTrip:
    """Tests for round-trip conversion accuracy."""

    @pytest.mark.parametrize(
        "category,unit1,unit2",
        [
            ("Length", "meter", "foot"),
            ("Length", "kilometer", "mile"),
            ("Length", "inch", "centimeter"),
            ("Weight", "kilogram", "pound"),
            ("Weight", "gram", "ounce"),
            ("Volume", "liter", "gallon (US)"),
            ("Volume", "milliliter", "fluid ounce"),
            ("Area", "sq meter", "sq foot"),
            ("Area", "hectare", "acre"),
            ("Speed", "km/h", "mph"),
            ("Speed", "m/s", "knots"),
            ("Time", "hour", "minute"),
            ("Time", "day", "second"),
            ("Data", "megabyte", "kilobyte"),
            ("Data", "gibibyte", "mebibyte"),
        ],
    )
    def test_round_trip_linear_conversions(
        self, category: str, unit1: str, unit2: str
    ) -> None:
        """Converting A->B->A should return the original value."""
        original = 42.5
        converted = converter.convert(original, unit1, unit2, category)
        back = converter.convert(converted, unit2, unit1, category)
        assert back == pytest.approx(original, rel=1e-10)

    @pytest.mark.parametrize(
        "unit1,unit2",
        [
            ("Celsius", "Fahrenheit"),
            ("Celsius", "Kelvin"),
            ("Fahrenheit", "Kelvin"),
        ],
    )
    def test_round_trip_temperature_conversions(
        self, unit1: str, unit2: str
    ) -> None:
        """Temperature round-trip should preserve value (above absolute zero)."""
        original = 25.0  # Safe value above absolute zero
        converted = converter.convert(original, unit1, unit2, "Temperature")
        back = converter.convert(converted, unit2, unit1, "Temperature")
        assert back == pytest.approx(original, rel=1e-10)


class TestGetCategories:
    """Tests for get_categories function."""

    def test_returns_eight_categories(self) -> None:
        """Should return exactly 8 categories."""
        categories = converter.get_categories()
        assert len(categories) == 8

    def test_categories_in_correct_order(self) -> None:
        """Categories should be in the specified order."""
        categories = converter.get_categories()
        assert categories[0] == "Length"
        assert categories[1] == "Weight"
        assert categories[2] == "Temperature"
        assert categories[3] == "Volume"
        assert categories[4] == "Area"
        assert categories[5] == "Speed"
        assert categories[6] == "Time"
        assert categories[7] == "Data"

    def test_returns_copy_not_reference(self) -> None:
        """Should return a copy, not the original list."""
        categories1 = converter.get_categories()
        categories2 = converter.get_categories()
        assert categories1 is not categories2


class TestGetUnitsForCategory:
    """Tests for get_units_for_category function."""

    @pytest.mark.parametrize(
        "category,expected_units",
        [
            ("Length", ["meter", "kilometer", "centimeter", "millimeter", "mile",
                        "yard", "foot", "inch", "nautical mile"]),
            ("Temperature", ["Celsius", "Fahrenheit", "Kelvin"]),
        ],
    )
    def test_returns_correct_units(
        self, category: str, expected_units: list[str]
    ) -> None:
        """Should return all units for the specified category."""
        units = converter.get_units_for_category(category)
        for expected in expected_units:
            assert expected in units

    def test_temperature_has_exactly_three_units(self) -> None:
        """Temperature category should have exactly 3 units."""
        units = converter.get_units_for_category("Temperature")
        assert len(units) == 3

    def test_unknown_category_raises_value_error(self) -> None:
        """Unknown category should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown category"):
            converter.get_units_for_category("InvalidCategory")


class TestGetUnitAbbreviation:
    """Tests for get_unit_abbreviation function."""

    @pytest.mark.parametrize(
        "unit,expected_abbrev",
        [
            # Length
            ("meter", "m"),
            ("kilometer", "km"),
            ("foot", "ft"),
            ("inch", "in"),
            ("nautical mile", "nmi"),
            # Weight
            ("kilogram", "kg"),
            ("pound", "lb"),
            # Temperature
            ("Celsius", "C"),
            ("Fahrenheit", "F"),
            ("Kelvin", "K"),
            # Volume with unicode
            ("cubic meter", "m³"),
            # Area with unicode superscripts
            ("sq meter", "m²"),
            ("sq kilometer", "km²"),
            ("sq foot", "ft²"),
            # Speed
            ("m/s", "m/s"),
            ("km/h", "km/h"),
            ("Mach", "Mach"),
            # Time
            ("second", "s"),
            ("millisecond", "ms"),
            ("minute", "min"),
            # Data
            ("byte", "B"),
            ("kilobyte", "KB"),
            ("kibibyte", "KiB"),
            ("mebibyte", "MiB"),
        ],
    )
    def test_returns_correct_abbreviation(
        self, unit: str, expected_abbrev: str
    ) -> None:
        """Should return correct abbreviation for each unit."""
        result = converter.get_unit_abbreviation(unit)
        assert result == expected_abbrev

    def test_unknown_unit_raises_value_error(self) -> None:
        """Unknown unit should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown unit"):
            converter.get_unit_abbreviation("lightyear")


class TestGetUnitFromAbbreviation:
    """Tests for get_unit_from_abbreviation function."""

    @pytest.mark.parametrize(
        "abbrev,category,expected_unit",
        [
            ("m", "Length", "meter"),
            ("km", "Length", "kilometer"),
            ("ft", "Length", "foot"),
            ("kg", "Weight", "kilogram"),
            ("lb", "Weight", "pound"),
            ("C", "Temperature", "Celsius"),
            ("F", "Temperature", "Fahrenheit"),
            ("K", "Temperature", "Kelvin"),
            ("m²", "Area", "sq meter"),
            ("m³", "Volume", "cubic meter"),
            ("m/s", "Speed", "m/s"),
            ("s", "Time", "second"),
            ("B", "Data", "byte"),
            ("KB", "Data", "kilobyte"),
            ("KiB", "Data", "kibibyte"),
        ],
    )
    def test_returns_correct_unit_name(
        self, abbrev: str, category: str, expected_unit: str
    ) -> None:
        """Should return correct full unit name from abbreviation."""
        result = converter.get_unit_from_abbreviation(abbrev, category)
        assert result == expected_unit

    def test_unknown_abbreviation_raises_value_error(self) -> None:
        """Unknown abbreviation should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown abbreviation"):
            converter.get_unit_from_abbreviation("xyz", "Length")

    def test_abbreviation_in_wrong_category_raises_value_error(self) -> None:
        """Abbreviation valid in one category but used in another should raise."""
        with pytest.raises(ValueError, match="Unknown abbreviation"):
            converter.get_unit_from_abbreviation("kg", "Length")


class TestGetQuickUnits:
    """Tests for get_quick_units function."""

    @pytest.mark.parametrize(
        "category,expected_count,expected_contains",
        [
            ("Length", 8, ["m", "km", "cm", "mm", "mi", "yd", "ft", "in"]),
            ("Weight", 7, ["kg", "g", "mg", "t", "lb", "oz", "st"]),
            ("Temperature", 3, ["C", "F", "K"]),
            ("Volume", 7, ["L", "mL", "m³", "gal", "qt", "pt", "cup"]),
            ("Area", 7, ["m²", "km²", "ft²", "yd²", "ac", "ha", "mi²"]),
            ("Speed", 6, ["m/s", "km/h", "mph", "kn", "ft/s", "Mach"]),
            ("Time", 7, ["s", "ms", "min", "hr", "d", "wk", "yr"]),
            ("Data", 8, ["B", "KB", "MB", "GB", "TB", "KiB", "MiB", "GiB"]),
        ],
    )
    def test_returns_correct_quick_units(
        self, category: str, expected_count: int, expected_contains: list[str]
    ) -> None:
        """Should return correct quick unit abbreviations for each category."""
        quick_units = converter.get_quick_units(category)
        assert len(quick_units) == expected_count
        for abbrev in expected_contains:
            assert abbrev in quick_units

    def test_unknown_category_raises_value_error(self) -> None:
        """Unknown category should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown category"):
            converter.get_quick_units("InvalidCategory")

    def test_returns_copy_not_reference(self) -> None:
        """Should return a copy, not the original list."""
        quick1 = converter.get_quick_units("Length")
        quick2 = converter.get_quick_units("Length")
        assert quick1 is not quick2


class TestGetDefaultUnits:
    """Tests for get_default_units function."""

    @pytest.mark.parametrize(
        "category,expected_from,expected_to",
        [
            ("Length", "meter", "foot"),
            ("Weight", "kilogram", "pound"),
            ("Temperature", "Celsius", "Fahrenheit"),
            ("Volume", "liter", "gallon (US)"),
            ("Area", "sq meter", "sq foot"),
            ("Speed", "km/h", "mph"),
            ("Time", "minute", "second"),
            ("Data", "megabyte", "gigabyte"),
        ],
    )
    def test_returns_correct_default_units(
        self, category: str, expected_from: str, expected_to: str
    ) -> None:
        """Should return correct default FROM and TO units per spec."""
        from_unit, to_unit = converter.get_default_units(category)
        assert from_unit == expected_from
        assert to_unit == expected_to

    def test_unknown_category_raises_value_error(self) -> None:
        """Unknown category should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown category"):
            converter.get_default_units("InvalidCategory")


class TestFormatResultBasic:
    """Tests for basic format_result functionality."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, "0"),
            (1, "1"),
            (42, "42"),
            (100, "100"),
            (-1, "-1"),
            (-42, "-42"),
        ],
    )
    def test_integer_formatting(self, value: float, expected: str) -> None:
        """Integer values should format without decimal point."""
        result = converter.format_result(float(value))
        assert result == expected


class TestFormatResultTrailingZeros:
    """Tests for trailing zero removal in format_result."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            (32.0, "32"),
            (32.10, "32.1"),
            (32.100, "32.1"),
            (1.0, "1"),
            (0.0, "0"),
            (100.0, "100"),
            (3.50, "3.5"),
        ],
    )
    def test_trailing_zeros_removed(self, value: float, expected: str) -> None:
        """Trailing zeros after decimal point should be removed."""
        result = converter.format_result(value)
        assert result == expected


class TestFormatResultThousandSeparators:
    """Tests for thousand separator formatting."""

    @pytest.mark.parametrize(
        "value,expected_contains",
        [
            (1234, "1,234"),
            (1234567, "1,234,567"),
            (1000000, "1,000,000"),
            (123456789, "123,456,789"),
        ],
    )
    def test_thousand_separators_present(
        self, value: float, expected_contains: str
    ) -> None:
        """Large integers should have thousand separators."""
        result = converter.format_result(float(value))
        assert expected_contains in result

    def test_thousand_separators_with_decimal(self) -> None:
        """Numbers with decimals should have thousand separators in integer part."""
        result = converter.format_result(1234567.89)
        assert "1,234,567" in result


class TestFormatResultScientificNotation:
    """Tests for scientific notation in format_result."""

    def test_very_large_value_uses_scientific(self) -> None:
        """Values >= 1e12 should use scientific notation."""
        result = converter.format_result(1.5e12)
        assert "e" in result.lower()

    def test_very_small_value_uses_scientific(self) -> None:
        """Very small values should use scientific notation."""
        result = converter.format_result(1e-15)
        assert "e" in result.lower()

    def test_large_value_below_threshold(self) -> None:
        """Values with <= 10 digits should not use scientific notation."""
        # 10-digit value stays within precision=10 limit, so no scientific notation
        result = converter.format_result(1234567890)
        # Should have thousand separators, not scientific
        assert "," in result and "e" not in result.lower()


class TestFormatResultPrecision:
    """Tests for precision limiting in format_result."""

    def test_precision_limited_to_ten_significant_digits(self) -> None:
        """Result should have at most 10 significant digits."""
        result = converter.format_result(3.14159265358979323846)
        # Remove formatting characters to count significant digits
        digits_only = result.replace(",", "").replace(".", "").replace("-", "")
        assert len(digits_only) <= 11  # Allow for rounding

    def test_custom_precision(self) -> None:
        """Custom precision parameter should be respected."""
        result = converter.format_result(3.14159265358979, precision=5)
        # Should have fewer digits
        digits_only = result.replace(",", "").replace(".", "").replace("-", "")
        assert len(digits_only) <= 6


class TestFormatResultErrorValues:
    """Tests for error value handling in format_result."""

    def test_infinity_returns_error(self) -> None:
        """Infinity should return 'Error'."""
        assert converter.format_result(float("inf")) == "Error"

    def test_negative_infinity_returns_error(self) -> None:
        """Negative infinity should return 'Error'."""
        assert converter.format_result(float("-inf")) == "Error"

    def test_nan_returns_error(self) -> None:
        """NaN should return 'Error'."""
        assert converter.format_result(float("nan")) == "Error"


class TestFormatResultNegativeValues:
    """Tests for negative value formatting."""

    def test_negative_integer(self) -> None:
        """Negative integer should format with minus sign."""
        result = converter.format_result(-273)
        assert result.startswith("-")
        assert "273" in result

    def test_negative_decimal(self) -> None:
        """Negative decimal should format with minus sign."""
        result = converter.format_result(-273.15)
        assert result.startswith("-")
        assert "273" in result


class TestConvertErrorHandling:
    """Tests for error handling in convert function."""

    def test_unknown_category_raises_value_error(self) -> None:
        """Unknown category should raise ValueError with descriptive message."""
        with pytest.raises(ValueError, match="Unknown category"):
            converter.convert(1, "meter", "foot", "InvalidCategory")

    def test_unknown_from_unit_raises_value_error(self) -> None:
        """Unknown from_unit should raise ValueError with descriptive message."""
        with pytest.raises(ValueError, match="Unknown unit"):
            converter.convert(1, "lightyear", "foot", "Length")

    def test_unknown_to_unit_raises_value_error(self) -> None:
        """Unknown to_unit should raise ValueError with descriptive message."""
        with pytest.raises(ValueError, match="Unknown unit"):
            converter.convert(1, "meter", "lightyear", "Length")

    def test_unknown_temperature_from_unit_raises_value_error(self) -> None:
        """Unknown temperature from_unit should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown temperature unit"):
            converter.convert(1, "Rankine", "Celsius", "Temperature")

    def test_unknown_temperature_to_unit_raises_value_error(self) -> None:
        """Unknown temperature to_unit should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown temperature unit"):
            converter.convert(1, "Celsius", "Rankine", "Temperature")

    def test_unit_from_wrong_category_raises_value_error(self) -> None:
        """Unit valid in one category but used in another should raise."""
        with pytest.raises(ValueError, match="Unknown unit"):
            converter.convert(1, "kilogram", "foot", "Length")


class TestConversionFactorsIntegrity:
    """Tests to verify conversion factors are correctly defined."""

    @pytest.mark.parametrize(
        "category",
        ["Length", "Weight", "Volume", "Area", "Speed", "Time", "Data"],
    )
    def test_base_unit_has_factor_one(self, category: str) -> None:
        """Each category's base unit should have factor 1.0."""
        base_units = {
            "Length": "meter",
            "Weight": "kilogram",
            "Volume": "liter",
            "Area": "sq meter",
            "Speed": "m/s",
            "Time": "second",
            "Data": "byte",
        }
        base_unit = base_units[category]
        factor = converter.CONVERSION_FACTORS[category][base_unit]
        assert factor == 1.0

    def test_all_units_have_metadata(self) -> None:
        """Every unit in conversion factors should have metadata."""
        for category, units in converter.CONVERSION_FACTORS.items():
            for unit in units:
                assert unit in converter.UNIT_METADATA, f"Missing metadata for {unit}"

    def test_temperature_units_have_metadata(self) -> None:
        """All temperature units should have metadata."""
        for unit in converter.TEMPERATURE_UNITS:
            assert unit in converter.UNIT_METADATA, f"Missing metadata for {unit}"


class TestEdgeCases:
    """Tests for various edge cases."""

    def test_very_large_conversion(self) -> None:
        """Test conversion with very large values."""
        # 1 trillion bytes to terabytes
        result = converter.convert(1e12, "byte", "terabyte", "Data")
        assert result == pytest.approx(1.0, rel=1e-10)

    def test_very_small_conversion(self) -> None:
        """Test conversion with very small values."""
        result = converter.convert(0.000001, "meter", "millimeter", "Length")
        assert result == pytest.approx(0.001, rel=1e-10)

    def test_floating_point_precision(self) -> None:
        """Test that floating point precision is maintained."""
        # 0.1 + 0.2 floating point issue shouldn't affect conversions
        original = 0.3
        converted = converter.convert(original, "meter", "foot", "Length")
        back = converter.convert(converted, "foot", "meter", "Length")
        assert back == pytest.approx(original, rel=1e-10)

    def test_zero_conversion_all_categories(self) -> None:
        """Zero should convert to zero in all categories."""
        categories_units = [
            ("Length", "meter", "foot"),
            ("Weight", "kilogram", "pound"),
            ("Temperature", "Celsius", "Fahrenheit"),
            ("Volume", "liter", "gallon (US)"),
            ("Area", "sq meter", "acre"),
            ("Speed", "km/h", "mph"),
            ("Time", "hour", "second"),
            ("Data", "gigabyte", "megabyte"),
        ]
        for category, from_unit, to_unit in categories_units:
            result = converter.convert(0, from_unit, to_unit, category)
            # Temperature 0C = 32F, so skip assertion for temperature
            if category != "Temperature":
                assert result == 0.0
