"""Unit conversion logic for the calculator converter mode.

This module provides pure conversion functions for 8 measurement categories:
Length, Weight, Temperature, Volume, Area, Speed, Time, and Data Storage.
All conversions go through a base unit (no chained conversions).
"""

import math
from typing import Literal, Union

Number = Union[int, float]
Category = Literal[
    "Length", "Weight", "Temperature", "Volume", "Area", "Speed", "Time", "Data"
]

CATEGORIES: list[str] = [
    "Length",
    "Weight",
    "Temperature",
    "Volume",
    "Area",
    "Speed",
    "Time",
    "Data",
]

# Conversion factors: multiply value by factor to get base unit
# Base units: meter, kilogram, kelvin (special), liter, sq meter, m/s, second, byte
CONVERSION_FACTORS: dict[str, dict[str, float]] = {
    "Length": {
        "meter": 1.0,
        "kilometer": 1000.0,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.344,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
        "nautical mile": 1852.0,
    },
    "Weight": {
        "kilogram": 1.0,
        "gram": 0.001,
        "milligram": 0.000001,
        "metric ton": 1000.0,
        "pound": 0.45359237,
        "ounce": 0.028349523125,
        "stone": 6.35029318,
    },
    "Volume": {
        "liter": 1.0,
        "milliliter": 0.001,
        "cubic meter": 1000.0,
        "gallon (US)": 3.785411784,
        "gallon (UK)": 4.54609,
        "quart": 0.946352946,
        "pint": 0.473176473,
        "cup": 0.2365882365,
        "fluid ounce": 0.0295735295625,
    },
    "Area": {
        "sq meter": 1.0,
        "sq kilometer": 1000000.0,
        "sq centimeter": 0.0001,
        "sq foot": 0.09290304,
        "sq yard": 0.83612736,
        "acre": 4046.8564224,
        "hectare": 10000.0,
        "sq mile": 2589988.110336,
    },
    "Speed": {
        "m/s": 1.0,
        "km/h": 0.277777778,
        "mph": 0.44704,
        "knots": 0.514444444,
        "ft/s": 0.3048,
        "Mach": 343.0,
    },
    "Time": {
        "second": 1.0,
        "millisecond": 0.001,
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400.0,
        "week": 604800.0,
        "year": 31536000.0,
    },
    "Data": {
        "byte": 1.0,
        "kilobyte": 1000.0,
        "megabyte": 1000000.0,
        "gigabyte": 1000000000.0,
        "terabyte": 1000000000000.0,
        "kibibyte": 1024.0,
        "mebibyte": 1048576.0,
        "gibibyte": 1073741824.0,
        "tebibyte": 1099511627776.0,
    },
}

# Unit metadata: abbreviation and full name for each unit
UNIT_METADATA: dict[str, dict[str, str]] = {
    # Length
    "meter": {"abbrev": "m", "full_name": "meter"},
    "kilometer": {"abbrev": "km", "full_name": "kilometer"},
    "centimeter": {"abbrev": "cm", "full_name": "centimeter"},
    "millimeter": {"abbrev": "mm", "full_name": "millimeter"},
    "mile": {"abbrev": "mi", "full_name": "mile"},
    "yard": {"abbrev": "yd", "full_name": "yard"},
    "foot": {"abbrev": "ft", "full_name": "foot"},
    "inch": {"abbrev": "in", "full_name": "inch"},
    "nautical mile": {"abbrev": "nmi", "full_name": "nautical mile"},
    # Weight
    "kilogram": {"abbrev": "kg", "full_name": "kilogram"},
    "gram": {"abbrev": "g", "full_name": "gram"},
    "milligram": {"abbrev": "mg", "full_name": "milligram"},
    "metric ton": {"abbrev": "t", "full_name": "metric ton"},
    "pound": {"abbrev": "lb", "full_name": "pound"},
    "ounce": {"abbrev": "oz", "full_name": "ounce"},
    "stone": {"abbrev": "st", "full_name": "stone"},
    # Temperature
    "Celsius": {"abbrev": "C", "full_name": "Celsius"},
    "Fahrenheit": {"abbrev": "F", "full_name": "Fahrenheit"},
    "Kelvin": {"abbrev": "K", "full_name": "Kelvin"},
    # Volume
    "liter": {"abbrev": "L", "full_name": "liter"},
    "milliliter": {"abbrev": "mL", "full_name": "milliliter"},
    "cubic meter": {"abbrev": "m³", "full_name": "cubic meter"},
    "gallon (US)": {"abbrev": "gal", "full_name": "US gallon"},
    "gallon (UK)": {"abbrev": "gal UK", "full_name": "UK gallon"},
    "quart": {"abbrev": "qt", "full_name": "quart"},
    "pint": {"abbrev": "pt", "full_name": "pint"},
    "cup": {"abbrev": "cup", "full_name": "cup"},
    "fluid ounce": {"abbrev": "fl oz", "full_name": "fluid ounce"},
    # Area
    "sq meter": {"abbrev": "m²", "full_name": "square meter"},
    "sq kilometer": {"abbrev": "km²", "full_name": "square kilometer"},
    "sq centimeter": {"abbrev": "cm²", "full_name": "square centimeter"},
    "sq foot": {"abbrev": "ft²", "full_name": "square foot"},
    "sq yard": {"abbrev": "yd²", "full_name": "square yard"},
    "acre": {"abbrev": "ac", "full_name": "acre"},
    "hectare": {"abbrev": "ha", "full_name": "hectare"},
    "sq mile": {"abbrev": "mi²", "full_name": "square mile"},
    # Speed
    "m/s": {"abbrev": "m/s", "full_name": "meters per second"},
    "km/h": {"abbrev": "km/h", "full_name": "kilometers per hour"},
    "mph": {"abbrev": "mph", "full_name": "miles per hour"},
    "knots": {"abbrev": "kn", "full_name": "knots"},
    "ft/s": {"abbrev": "ft/s", "full_name": "feet per second"},
    "Mach": {"abbrev": "Mach", "full_name": "Mach number"},
    # Time
    "second": {"abbrev": "s", "full_name": "second"},
    "millisecond": {"abbrev": "ms", "full_name": "millisecond"},
    "minute": {"abbrev": "min", "full_name": "minute"},
    "hour": {"abbrev": "hr", "full_name": "hour"},
    "day": {"abbrev": "d", "full_name": "day"},
    "week": {"abbrev": "wk", "full_name": "week"},
    "year": {"abbrev": "yr", "full_name": "year"},
    # Data
    "byte": {"abbrev": "B", "full_name": "byte"},
    "kilobyte": {"abbrev": "KB", "full_name": "kilobyte"},
    "megabyte": {"abbrev": "MB", "full_name": "megabyte"},
    "gigabyte": {"abbrev": "GB", "full_name": "gigabyte"},
    "terabyte": {"abbrev": "TB", "full_name": "terabyte"},
    "kibibyte": {"abbrev": "KiB", "full_name": "kibibyte"},
    "mebibyte": {"abbrev": "MiB", "full_name": "mebibyte"},
    "gibibyte": {"abbrev": "GiB", "full_name": "gibibyte"},
    "tebibyte": {"abbrev": "TiB", "full_name": "tebibyte"},
}

# Quick unit buttons per category (abbreviations)
QUICK_UNITS: dict[str, list[str]] = {
    "Length": ["m", "km", "cm", "mm", "mi", "yd", "ft", "in"],
    "Weight": ["kg", "g", "mg", "t", "lb", "oz", "st"],
    "Temperature": ["C", "F", "K"],
    "Volume": ["L", "mL", "m³", "gal", "qt", "pt", "cup"],
    "Area": ["m²", "km²", "ft²", "yd²", "ac", "ha", "mi²"],
    "Speed": ["m/s", "km/h", "mph", "kn", "ft/s", "Mach"],
    "Time": ["s", "ms", "min", "hr", "d", "wk", "yr"],
    "Data": ["B", "KB", "MB", "GB", "TB", "KiB", "MiB", "GiB"],
}

# Default FROM and TO units per category
DEFAULT_UNITS: dict[str, tuple[str, str]] = {
    "Length": ("meter", "foot"),
    "Weight": ("kilogram", "pound"),
    "Temperature": ("Celsius", "Fahrenheit"),
    "Volume": ("liter", "gallon (US)"),
    "Area": ("sq meter", "sq foot"),
    "Speed": ("km/h", "mph"),
    "Time": ("minute", "second"),
    "Data": ("megabyte", "gigabyte"),
}

# Temperature units (handled specially - non-linear conversions)
TEMPERATURE_UNITS: list[str] = ["Celsius", "Fahrenheit", "Kelvin"]


def _celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin."""
    return c + 273.15


def _kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius."""
    return k - 273.15


def _fahrenheit_to_kelvin(f: float) -> float:
    """Convert Fahrenheit to Kelvin."""
    return (f - 32) * 5 / 9 + 273.15


def _kelvin_to_fahrenheit(k: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return (k - 273.15) * 9 / 5 + 32


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin.

    Uses Kelvin as the intermediate (base) unit. Silently clamps to
    absolute zero (0 K) if the result would be negative Kelvin.
    """
    # Convert to Kelvin first
    if from_unit == "Celsius":
        kelvin = _celsius_to_kelvin(value)
    elif from_unit == "Fahrenheit":
        kelvin = _fahrenheit_to_kelvin(value)
    else:  # Kelvin
        kelvin = value

    # Clamp to absolute zero (silent clamp per spec)
    kelvin = max(0.0, kelvin)

    # Convert from Kelvin to target
    if to_unit == "Celsius":
        return _kelvin_to_celsius(kelvin)
    elif to_unit == "Fahrenheit":
        return _kelvin_to_fahrenheit(kelvin)
    else:  # Kelvin
        return kelvin


def convert(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """Convert a value from one unit to another.

    Args:
        value: The numeric value to convert.
        from_unit: Source unit name (e.g., "meter", "Celsius").
        to_unit: Target unit name (e.g., "foot", "Fahrenheit").
        category: Category name (e.g., "Length", "Temperature").

    Returns:
        Converted value as float.

    Raises:
        ValueError: If unit not found in category or category unknown.

    Examples:
        >>> convert(100, "meter", "foot", "Length")
        328.0839895013123
        >>> convert(0, "Celsius", "Fahrenheit", "Temperature")
        32.0
        >>> convert(1024, "mebibyte", "gibibyte", "Data")
        1.0
    """
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")

    # Same unit conversion - return unchanged
    if from_unit == to_unit:
        return value

    # Temperature is special (non-linear)
    if category == "Temperature":
        if from_unit not in TEMPERATURE_UNITS:
            raise ValueError(f"Unknown temperature unit: {from_unit}")
        if to_unit not in TEMPERATURE_UNITS:
            raise ValueError(f"Unknown temperature unit: {to_unit}")
        return _convert_temperature(value, from_unit, to_unit)

    # Linear conversion: value * from_factor / to_factor
    factors = CONVERSION_FACTORS.get(category)
    if factors is None:
        raise ValueError(f"No conversion factors for category: {category}")

    if from_unit not in factors:
        raise ValueError(f"Unknown unit '{from_unit}' in category '{category}'")
    if to_unit not in factors:
        raise ValueError(f"Unknown unit '{to_unit}' in category '{category}'")

    # Convert: FROM -> base unit -> TO
    base_value = value * factors[from_unit]
    return base_value / factors[to_unit]


def get_units_for_category(category: str) -> list[str]:
    """Get list of all unit names for a category.

    Args:
        category: Category name.

    Returns:
        List of unit names.

    Raises:
        ValueError: If category is unknown.
    """
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")

    if category == "Temperature":
        return TEMPERATURE_UNITS.copy()

    return list(CONVERSION_FACTORS[category].keys())


def get_unit_abbreviation(unit: str) -> str:
    """Get display abbreviation for a unit.

    Args:
        unit: Full unit name.

    Returns:
        Abbreviation (e.g., "m" for "meter", "m²" for "sq meter").

    Raises:
        ValueError: If unit is unknown.
    """
    if unit not in UNIT_METADATA:
        raise ValueError(f"Unknown unit: {unit}")
    return UNIT_METADATA[unit]["abbrev"]


def get_unit_from_abbreviation(abbrev: str, category: str) -> str:
    """Look up full unit name from abbreviation.

    Args:
        abbrev: Unit abbreviation.
        category: Category to search in.

    Returns:
        Full unit name.

    Raises:
        ValueError: If abbreviation not found in category.
    """
    units = get_units_for_category(category)
    for unit in units:
        if UNIT_METADATA[unit]["abbrev"] == abbrev:
            return unit
    raise ValueError(f"Unknown abbreviation '{abbrev}' in category '{category}'")


def get_categories() -> list[str]:
    """Get list of all category names in display order.

    Returns:
        List of category names.
    """
    return CATEGORIES.copy()


def get_quick_units(category: str) -> list[str]:
    """Get abbreviations for quick unit buttons.

    Args:
        category: Category name.

    Returns:
        List of unit abbreviations for quick buttons.

    Raises:
        ValueError: If category is unknown.
    """
    if category not in QUICK_UNITS:
        raise ValueError(f"Unknown category: {category}")
    return QUICK_UNITS[category].copy()


def get_default_units(category: str) -> tuple[str, str]:
    """Get default FROM and TO units for a category.

    Args:
        category: Category name.

    Returns:
        Tuple of (from_unit, to_unit) names.

    Raises:
        ValueError: If category is unknown.
    """
    if category not in DEFAULT_UNITS:
        raise ValueError(f"Unknown category: {category}")
    return DEFAULT_UNITS[category]


def format_result(value: float, precision: int = 10) -> str:
    """Format a conversion result for display.

    Args:
        value: Numeric result.
        precision: Maximum significant digits (default 10).

    Returns:
        Formatted string with thousand separators, trailing zeros removed.
        Uses scientific notation for very large/small values.
        Rounds using half-even (banker's rounding).

    Examples:
        >>> format_result(32.0)
        '32'
        >>> format_result(3.14159265358979)
        '3.141592654'
        >>> format_result(1234567.89)
        '1,234,567.89'
        >>> format_result(1500000000000)
        '1.5e+12'
    """
    # Handle non-finite values
    if not math.isfinite(value):
        return "Error"

    # Handle zero
    if value == 0:
        return "0"

    # Use scientific notation for very large or very small values
    abs_value = abs(value)
    if abs_value >= 1e12 or (abs_value < 1e-10 and abs_value != 0):
        return f"{value:.{precision}g}"

    # Format with proper precision
    formatted = f"{value:.{precision}g}"

    # Add thousand separators to integer part
    if "e" in formatted.lower():
        return formatted

    if "." in formatted:
        int_part, dec_part = formatted.split(".")
        try:
            int_formatted = f"{int(int_part):,}"
        except ValueError:
            int_formatted = int_part
        return f"{int_formatted}.{dec_part}"
    else:
        try:
            return f"{int(float(formatted)):,}"
        except ValueError:
            return formatted
