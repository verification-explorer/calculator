# Specification for Calculator Unit Conversion Mode

## Context
A planned mode for converting between measurement units across common physical categories. It coexists with Standard and Programmer modes via the existing mode-switcher sidebar, using the same dark theme and UI patterns.

## Core Features

### Supported Categories
**Initial scope:** 8 categories covering the most common conversion needs

| Category | Base Unit | Display Units |
|----------|-----------|---------------|
| Length | meter | meter, kilometer, centimeter, millimeter, mile, yard, foot, inch, nautical mile |
| Weight/Mass | kilogram | kilogram, gram, milligram, metric ton, pound, ounce, stone |
| Temperature | kelvin (internal) | Celsius, Fahrenheit, Kelvin |
| Volume | liter | liter, milliliter, cubic meter, gallon (US), gallon (UK), quart, pint, cup, fluid ounce |
| Area | square meter | sq meter, sq kilometer, sq centimeter, sq foot, sq yard, acre, hectare, sq mile |
| Speed | meters/second | m/s, km/h, mph, knots, ft/s, Mach |
| Time | second | second, millisecond, minute, hour, day, week, year |
| Data Storage | byte | byte, kilobyte (KB), megabyte (MB), gigabyte (GB), terabyte (TB), kibibyte (KiB), mebibyte (MiB), gibibyte (GiB), tebibyte (TiB) |

**Default state on startup:** Length category, meter-to-foot conversion

---

## UI Layout (Top to Bottom)

### ASCII Layout Diagram

```
+------------------------------------------------------------------------+
| [hamburger]  Calculator                                                 |
+------------------------------------------------------------------------+
|                                                                          |
| [Length] [Weight] [Temp] [Volume] [Area] [Speed] [Time] [Data]          |  <- Category Selector
|                                                                          |
+------------------------------------------------------------------------+
|                                                                          |
|  FROM                                                                    |
|  +------------------+  +------------------------------------------+     |
|  | m - meter      v |  |                         1,234.56789      |     |  <- From Unit + Input
|  +------------------+  +------------------------------------------+     |
|                                                                          |
|                       [ Swap Units ⇄ ]                                   |  <- Swap Button
|                                                                          |
|  TO                                                                      |
|  +------------------+  +------------------------------------------+     |
|  | ft - foot      v |  |                         4,050.52493      |     |  <- To Unit + Input
|  +------------------+  +------------------------------------------+     |
|                                                                          |
+------------------------------------------------------------------------+
|                                                                          |
|  [m] [km] [cm] [mm] [mi] [yd] [ft] [in]                                 |  <- Quick Unit Buttons (left-aligned)
|                                                                          |
+------------------------------------------------------------------------+
|                                                                          |
|  7   8   9   C                                                           |
|  4   5   6   CE                                                          |  <- Numeric Keypad (4x4, shrinks with window)
|  1   2   3   ⌫                                                           |
|  +/- 0   .   =                                                           |
|                                                                          |
+------------------------------------------------------------------------+
|                          HISTORY                                         |
|  1,234.56789 m = 4,050.52493 ft [Length]                                |
|  100 km = 62.1371 mi [Length]                                           |
|  0 C = 32 F [Temperature]                                               |
|  ...                                                                     |
+------------------------------------------------------------------------+
```

---

### 1. Category Selector
**Position:** Top of the mode UI, below the toolbar  
**Style:** Horizontal row of `CalculatorButton` widgets  
**Options:** Length | Weight | Temp | Volume | Area | Speed | Time | Data  

**Button specifications:**
- Default color: `#3a3a3a` (inactive)
- Active color: `#ff9500` (orange accent)
- Size: Minimum width 70px, height 40px
- Font: Segoe UI, 11pt

**Behavior:**
- Only one category active at a time (mutual exclusion)
- Clicking a category:
  1. Highlights that button with accent color
  2. Updates quick unit buttons to show units for that category
  3. Resets FROM and TO unit selectors to category defaults
  4. Clears current input values (both fields reset to "0")
  5. Does NOT clear history

**Default units per category:**

| Category | Default FROM | Default TO |
|----------|--------------|------------|
| Length | meter | foot |
| Weight | kilogram | pound |
| Temperature | Celsius | Fahrenheit |
| Volume | liter | gallon (US) |
| Area | sq meter | sq foot |
| Speed | km/h | mph |
| Time | minute | second |
| Data | megabyte (MB) | gigabyte (GB) |

**Keyboard shortcuts (F6-F13):**
| Key | Category |
|-----|----------|
| F6 | Length |
| F7 | Weight |
| F8 | Temperature |
| F9 | Volume |
| F10 | Area |
| F11 | Speed |
| F12 | Time |
| F13 | Data |

---

### 2. FROM Panel
**Position:** Below category selector  
**Layout:** Label ("FROM") + Unit dropdown + Editable input field

**Unit Dropdown:**
- Type: `QComboBox` styled as button
- Width: Fixed 150px
- Background: `#3a3a3a`
- Font: Segoe UI, 12pt
- Shows current unit with dropdown arrow
- Dropdown list shows all units for current category
- Each unit displays: **abbreviation + full name** (e.g., "m - meter")

**Input Field:**
- Type: `QLineEdit`
- Alignment: Right-aligned
- Font: Segoe UI, 20pt (monospace for digits)
- Background: `#1c1c1c`
- Text color: white
- Minimum height: 50px
- Accepts: digits, decimal point (minus via +/− button only)
- Maximum precision: 15 significant digits
- Editable: Yes (user can type directly)
- On every keystroke: updates TO field in real-time
- **Thousand separators:** Enabled (e.g., 1,234,567)

---

### 3. Swap Button
**Position:** Centered between FROM and TO panels  
**Type:** `CalculatorButton`  
**Label:** "Swap Units ⇄" or icon  
**Color:** `#5856d6` (purple, same as trig/function buttons)  
**Size:** Width 120px, height 40px

**Behavior:**
- Swaps FROM unit with TO unit
- **Swaps FROM value with TO value**
- Example: "100 meters → 328.084 feet" becomes "328.084 feet → 100 meters"
- Does NOT add to history (it's a UI convenience, not a calculation)

---

### 4. TO Panel
**Position:** Below swap button  
**Layout:** Identical to FROM panel

**Bidirectional editing:**
- Both fields are editable
- Typing in TO field updates FROM field in real-time
- **Last-edited field becomes the source of truth**
- Subsequent unit changes recalculate the non-edited field from the last-edited field's value

---

### 5. Quick Unit Buttons
**Position:** Below TO panel  
**Layout:** Horizontal wrap row of `CalculatorButton` widgets, **left-aligned**
**Purpose:** One-click unit selection for common units

**Behavior:**
- Shows abbreviations for units in current category
- Clicking a quick unit button sets it as the FROM unit
- Shift+click sets it as the TO unit (keyboard/mouse only; touch users use dropdowns)
- Active FROM unit: highlighted with orange border
- Active TO unit: highlighted with purple border
- If same unit selected for both FROM and TO: **show "1" in both fields**

**Button specifications:**
- Size: 50x50 minimum
- Color: `#4a4a4a` (default digit button color)
- Font: Segoe UI, 12pt
- **Unicode superscripts** for area/volume: m², km², m³

**Quick units per category:**
```
Length:      [m] [km] [cm] [mm] [mi] [yd] [ft] [in]
Weight:      [kg] [g] [mg] [t] [lb] [oz] [st]
Temperature: [C] [F] [K]                              <- left-aligned, 3 buttons
Volume:      [L] [mL] [m³] [gal] [qt] [pt] [cup]
Area:        [m²] [km²] [ft²] [yd²] [ac] [ha] [mi²]
Speed:       [m/s] [km/h] [mph] [kn] [ft/s] [Mach]
Time:        [s] [ms] [min] [hr] [d] [wk] [yr]
Data:        [B] [KB] [MB] [GB] [TB] [KiB] [MiB] [GiB]
```

---

### 6. Numeric Keypad
**Position:** Below quick unit buttons  
**Layout:** 4 rows x 4 columns grid
**Responsive:** Buttons shrink proportionally with window size (maintain 4x4 grid)

**Button layout:**
```
Row 1: [7] [8] [9] [C]
Row 2: [4] [5] [6] [CE]
Row 3: [1] [2] [3] [⌫]
Row 4: [+/−] [0] [.] [=]
```

**Button functions:**
- `0-9`: Append digit to currently focused input field
- `.`: Append decimal point (only one allowed)
- `+/−`: Toggle sign (for negative values, primarily temperature) — **only way to enter negative**
- `C`: Clear both input fields, reset to "0"
- `CE`: Clear only the currently focused input field
- `⌫`: Delete last character from focused field
- `=`: Record current conversion to history

**Focus behavior:**
- Keypad operates on the last-clicked input field (FROM or TO)
- Default focus: FROM field
- Visual indicator: focused field has brighter border (`#ff9500`)

**Button colors:**
- Digits `0-9` and `.`: `#4a4a4a`
- `+/−`: `#4a4a4a`
- `C` and `CE`: `#ff3b30` (red)
- `⌫`: `#ff3b30` (red)
- `=`: `#ff9500` (orange)

---

### 7. History Panel
**Position:** Right side of layout (same as Standard/Programmer modes)  
**Style:** Reuse existing `QListWidget` styling

**Entry format:**
```
{from_value} {from_unit_abbr} = {to_value} {to_unit_abbr} [{category}]
```

**Examples:**
```
1,234.56789 m = 4,050.52493 ft [Length]
100 km = 62.1371 mi [Length]
0 C = 32 F [Temperature]
1,024 MiB = 1 GiB [Data]
1.5e+12 B = 1.5 TB [Data]       <- scientific notation matches display
```

**Behavior:**
- History recorded **only on explicit = or Enter press** (not auto-recorded on pause)
- **Duplicate entries allowed** (pressing = multiple times adds multiple entries)
- Double-clicking an entry:
  1. **Auto-switches to the entry's category** if different
  2. Populates FROM field with that value
  3. Sets FROM and TO units from the entry
- History persists within session but clears on mode switch (per existing behavior)
- "Clear History" button at bottom (reuse existing implementation)

---

## Data Model and Core Logic

### Canonical Value Architecture
**Internal representation:** All values stored as floating-point in the category's base unit

**Source of truth:** **Whichever field was last edited becomes canonical.** When a unit dropdown changes, the system recalculates the non-edited field from the last-edited field's value.

**Base units per category:**
| Category | Base Unit | Rationale |
|----------|-----------|-----------|
| Length | meter | SI standard |
| Weight | kilogram | SI standard |
| Temperature | kelvin | Absolute scale, no negative values |
| Volume | liter | Common practical unit |
| Area | square meter | SI standard |
| Speed | meters/second | SI standard |
| Time | second | SI standard |
| Data | byte | Fundamental unit |

**Conversion flow:**
1. User enters value in FROM field (e.g., "100 km")
2. Convert to base unit: `100 km × 1000 = 100000 m`
3. Store canonical value: `100000.0`
4. Convert to TO unit: `100000 m × 3.28084 = 328084 ft`
5. Display in TO field: `328,084`

**No chained conversions:** Always convert FROM → base unit → TO. Never convert FROM → TO directly (except when both are the same unit).

---

### Conversion Factor Data Structure

```python
# In converter.py
from typing import Literal, Callable

Category = Literal["Length", "Weight", "Temperature", "Volume", "Area", "Speed", "Time", "Data"]

# Simple linear conversions: multiply by factor to get base unit
# Factor = how many base units equal 1 of this unit
CONVERSION_FACTORS: dict[Category, dict[str, float]] = {
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
        "Mach": 343.0,  # Speed of sound at sea level (approx)
    },
    "Time": {
        "second": 1.0,
        "millisecond": 0.001,
        "minute": 60.0,
        "hour": 3600.0,
        "day": 86400.0,
        "week": 604800.0,
        "year": 31536000.0,  # 365 days (simple, not Gregorian average)
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

# Temperature requires special handling (non-linear conversions)
def celsius_to_kelvin(c: float) -> float:
    return c + 273.15

def kelvin_to_celsius(k: float) -> float:
    return k - 273.15

def fahrenheit_to_kelvin(f: float) -> float:
    return (f - 32) * 5/9 + 273.15

def kelvin_to_fahrenheit(k: float) -> float:
    return (k - 273.15) * 9/5 + 32

def kelvin_to_kelvin(k: float) -> float:
    return k

TEMPERATURE_TO_KELVIN: dict[str, Callable[[float], float]] = {
    "Celsius": celsius_to_kelvin,
    "Fahrenheit": fahrenheit_to_kelvin,
    "Kelvin": kelvin_to_kelvin,
}

KELVIN_TO_TEMPERATURE: dict[str, Callable[[float], float]] = {
    "Celsius": kelvin_to_celsius,
    "Fahrenheit": kelvin_to_fahrenheit,
    "Kelvin": kelvin_to_kelvin,
}
```

---

### Unit Metadata

```python
# Unit display information - uses Unicode superscripts for area/volume
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
    
    # Volume - uses Unicode superscript for m³
    "liter": {"abbrev": "L", "full_name": "liter"},
    "milliliter": {"abbrev": "mL", "full_name": "milliliter"},
    "cubic meter": {"abbrev": "m³", "full_name": "cubic meter"},
    "gallon (US)": {"abbrev": "gal", "full_name": "US gallon"},
    "gallon (UK)": {"abbrev": "gal UK", "full_name": "UK gallon"},
    "quart": {"abbrev": "qt", "full_name": "quart"},
    "pint": {"abbrev": "pt", "full_name": "pint"},
    "cup": {"abbrev": "cup", "full_name": "cup"},
    "fluid ounce": {"abbrev": "fl oz", "full_name": "fluid ounce"},
    
    # Area - uses Unicode superscripts
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

# Quick unit buttons per category (subset for UI, using abbreviations)
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
```

---

## Core Module: `converter.py`

Located at `src/calculator/converter.py`

### Public Functions

```python
def convert(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """Convert a value from one unit to another.
    
    Args:
        value: The numeric value to convert
        from_unit: Source unit name (e.g., "meter", "Celsius")
        to_unit: Target unit name (e.g., "foot", "Fahrenheit")
        category: Category name (e.g., "Length", "Temperature")
    
    Returns:
        Converted value as float
    
    Raises:
        ValueError: If unit not found in category or category unknown
    
    Examples:
        >>> convert(100, "meter", "foot", "Length")
        328.084
        >>> convert(0, "Celsius", "Fahrenheit", "Temperature")
        32.0
        >>> convert(1024, "mebibyte", "gibibyte", "Data")
        1.0
    """

def get_units_for_category(category: str) -> list[str]:
    """Get list of all unit names for a category.
    
    Args:
        category: Category name
    
    Returns:
        List of unit names
    
    Examples:
        >>> get_units_for_category("Temperature")
        ['Celsius', 'Fahrenheit', 'Kelvin']
    """

def get_unit_abbreviation(unit: str) -> str:
    """Get display abbreviation for a unit.
    
    Args:
        unit: Full unit name
    
    Returns:
        Abbreviation (e.g., "m" for "meter", "m²" for "sq meter")
    """

def get_unit_from_abbreviation(abbrev: str, category: str) -> str:
    """Look up full unit name from abbreviation.
    
    Args:
        abbrev: Unit abbreviation
        category: Category to search in
    
    Returns:
        Full unit name
    
    Raises:
        ValueError: If abbreviation not found in category
    """

def get_categories() -> list[str]:
    """Get list of all category names.
    
    Returns:
        List of category names in display order
    """

def get_quick_units(category: str) -> list[str]:
    """Get abbreviations for quick unit buttons.
    
    Args:
        category: Category name
    
    Returns:
        List of unit abbreviations for quick buttons
    """

def get_default_units(category: str) -> tuple[str, str]:
    """Get default FROM and TO units for a category.
    
    Args:
        category: Category name
    
    Returns:
        Tuple of (from_unit, to_unit) names
    """

def format_result(value: float, precision: int = 10) -> str:
    """Format a conversion result for display.
    
    Args:
        value: Numeric result
        precision: Maximum significant digits (default 10)
    
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
```

---

## GUI Widget: `ConverterModeWidget`

Located in `src/calculator/gui.py` as a new class

### Class Structure

```python
class ConverterModeWidget(QWidget):
    """Widget containing the unit converter mode UI."""
    
    def __init__(self, parent: CalculatorWindow):
        super().__init__()
        self.parent = parent
        
        # State variables
        self.current_category: str = "Length"
        self.from_unit: str = "meter"
        self.to_unit: str = "foot"
        self.from_value: float = 0.0
        self.to_value: float = 0.0
        self.focused_field: str = "from"  # "from" or "to"
        self.last_edited_field: str = "from"  # tracks source of truth
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the converter mode user interface."""
        # Main horizontal layout (calc + history)
        # Category selector row
        # FROM panel (label + dropdown + input)
        # Swap button
        # TO panel (label + dropdown + input)
        # Quick unit buttons (left-aligned)
        # Numeric keypad (4x4, proportionally shrinking)
        pass
    
    # Category handling
    def _on_category_changed(self, category: str): ...
    def _update_category_buttons(self): ...
    
    # Unit handling
    def _on_from_unit_changed(self, unit: str): ...
    def _on_to_unit_changed(self, unit: str): ...
    def _on_quick_unit_clicked(self, abbrev: str): ...
    def _swap_units(self): ...
    
    # Input handling
    def _on_from_input_changed(self, text: str): ...
    def _on_to_input_changed(self, text: str): ...
    def _on_keypad_click(self, key: str): ...
    def _append_digit(self, digit: str): ...
    def _clear_all(self): ...
    def _clear_entry(self): ...
    def _backspace(self): ...
    def _toggle_sign(self): ...
    def _record_to_history(self): ...
    
    # Conversion
    def _perform_conversion(self, source: str): ...
    def _update_display(self): ...
    
    # Utility
    def set_initial_state(self): ...
```

---

## Integration Points

### 1. Mode Switching (CalculatorWindow)

**Modifications to `_switch_mode` method:**

```python
def _switch_mode(self, mode: str):
    """Switch between calculator modes."""
    if mode == self.current_mode:
        return
    
    self.current_mode = mode
    self.history.clear()
    self.current_input = ""
    self.last_result = None
    
    if mode == "standard":
        self.mode_stack.setCurrentIndex(0)
        # ... existing standard mode switch code ...
    elif mode == "programmer":
        self.mode_stack.setCurrentIndex(1)
        # ... existing programmer mode switch code ...
    elif mode == "converter":
        self.mode_stack.setCurrentIndex(2)
        self.history_list.clear()
        converter_widget = self.mode_stack.widget(2)
        converter_widget.set_initial_state()
```

### 2. Sidebar Menu (ModeSidebar)

**Add converter mode button:**

```python
def _setup_ui(self):
    # ... existing code ...
    
    self.standard_btn = QPushButton("Standard")
    # ...
    
    self.programmer_btn = QPushButton("Programmer")
    # ...
    
    self.converter_btn = QPushButton("Unit Converter")
    self.converter_btn.setFont(QFont("Segoe UI", 14))
    self.converter_btn.clicked.connect(lambda: self.mode_selected.emit("converter"))
    layout.addWidget(self.converter_btn)
    
    layout.addStretch()
    
    self.set_active_mode("standard")
```

**Update `set_active_mode`:**

```python
def set_active_mode(self, mode: str):
    self.current_mode = mode
    
    # Apply styles to all three buttons
    for btn, btn_mode in [
        (self.standard_btn, "standard"),
        (self.programmer_btn, "programmer"),
        (self.converter_btn, "converter"),
    ]:
        btn.setStyleSheet(active_style if mode == btn_mode else normal_style)
```

### 3. Main Window Setup

**Add converter widget to stack:**

```python
def _setup_ui(self):
    # ... existing code ...
    
    self.mode_stack = QStackedWidget()
    self.standard_widget = StandardModeWidget(self)
    self.programmer_widget = ProgrammerModeWidget(self)
    self.converter_widget = ConverterModeWidget(self)
    
    self.mode_stack.addWidget(self.standard_widget)      # index 0
    self.mode_stack.addWidget(self.programmer_widget)    # index 1
    self.mode_stack.addWidget(self.converter_widget)     # index 2
```

### 4. History Integration

**Extend `HistoryEntry` for converter mode:**

```python
@dataclass
class ConverterHistoryEntry(HistoryEntry):
    """A unit converter history entry.
    
    Attributes:
        expression: The conversion expression (e.g., "100 m")
        result: The converted value
        timestamp: When the conversion was performed
        category: The category (e.g., "Length")
        from_unit: Source unit name
        to_unit: Target unit name
    """
    
    category: Optional[str] = None
    from_unit: Optional[str] = None
    to_unit: Optional[str] = None
    
    def __str__(self) -> str:
        if self.category and self.from_unit and self.to_unit:
            from calculator import converter
            from_abbr = converter.get_unit_abbreviation(self.from_unit)
            to_abbr = converter.get_unit_abbreviation(self.to_unit)
            return f"{self.expression} {from_abbr} = {self.result} {to_abbr} [{self.category}]"
        return f"{self.expression} = {self.result}"
```

---

## Keyboard Shortcuts

**Full keyboard support:**

| Key | Action |
|-----|--------|
| `0-9` | Digit input to focused field |
| `.` | Decimal point |
| `Backspace` | Delete last character |
| `Delete` | Clear entry (CE) |
| `Escape` | Clear all (C) — always clears, even if sidebar open |
| `Enter` or `=` | Record to history |
| `Tab` | Cycle through all interactive elements (full widget cycle) |
| `Ctrl+Shift+S` | Swap units |
| `F6` | Switch to Length |
| `F7` | Switch to Weight |
| `F8` | Switch to Temperature |
| `F9` | Switch to Volume |
| `F10` | Switch to Area |
| `F11` | Switch to Speed |
| `F12` | Switch to Time |
| `F13` | Switch to Data |

**Note:** Minus key (`-`) does NOT toggle sign. Use the `+/−` button only for negative values.

**Keyboard input in main window:**

```python
def keyPressEvent(self, event):
    if self.current_mode == "converter":
        converter_widget = self.mode_stack.widget(2)
        
        # Category shortcuts (F6-F13)
        category_keys = {
            Qt.Key.Key_F6: "Length",
            Qt.Key.Key_F7: "Weight",
            Qt.Key.Key_F8: "Temperature",
            Qt.Key.Key_F9: "Volume",
            Qt.Key.Key_F10: "Area",
            Qt.Key.Key_F11: "Speed",
            Qt.Key.Key_F12: "Time",
            Qt.Key.Key_F13: "Data",
        }
        if event.key() in category_keys:
            converter_widget._on_category_changed(category_keys[event.key()])
            return
        
        # Numeric input (minus key intentionally NOT handled)
        key = event.text()
        if key.isdigit() or key == '.':
            converter_widget._append_digit(key)
            return
        # ... etc ...
```

---

## Behavioral Specifications

### Real-Time Conversion
**Update frequency:** On every keystroke (same as Programmer Mode)

**Debouncing:** Not required (conversions are simple arithmetic)

**Update flow:**
1. User types in FROM field
2. Parse input to float
3. Mark FROM as `last_edited_field`
4. Call `converter.convert(value, from_unit, to_unit, category)`
5. Format result and display in TO field
6. (Reverse if user types in TO field)

### Input Validation

**Valid characters:** `0-9`, `.`

**Negative input:** +/− button only (minus key ignored)

**Invalid input handling:**
- Silently ignore invalid characters (do not add to field)
- Multiple decimal points: ignore second `.`

**Paste handling (Ctrl+V):**
- **Strip non-numeric characters:** Paste '123abc456' → '123456'
- Keep only digits, `.`, and leading `-`

**Empty field handling:**
- Empty string treated as 0
- Display "0" when field is cleared

**Overflow handling:**
- Very large numbers displayed in scientific notation (e.g., 1.5e+12)
- Very small numbers: show up to 15 significant digits
- Infinity/NaN: display "Error" and clear on next input

### Precision and Rounding

**Display precision:** 10 significant digits maximum

**Internal precision:** Full Python float precision (~15 significant digits)

**Rounding:** **Round half-even (banker's rounding)** — Python default
- 3.141592653589793 → "3.141592654"

**Trailing zeros:** Remove trailing zeros after decimal point
- `32.0` displays as `32`
- `32.10` displays as `32.1`
- `0.00001` displays as `0.00001`

**Thousand separators:** Enabled for all displayed values
- `1234567.89` displays as `1,234,567.89`
- `1099511627776` displays as `1,099,511,627,776`

### Temperature Special Cases

**Negative values:** Allowed for Celsius and Fahrenheit (via +/− button)

**Absolute zero handling:**
- Kelvin cannot be negative
- If user enters negative Kelvin, **silently clamp to 0** (no visual feedback)
- -273.15°C = 0 K (clamped)
- -459.67°F = 0 K (clamped)

**Display format:**
- Celsius: "25 C" (no degree symbol for simplicity)
- Fahrenheit: "77 F"
- Kelvin: "298.15 K"

### Data Storage Special Cases

**Binary vs Decimal:**
- KB/MB/GB/TB: Decimal (powers of 1000)
- KiB/MiB/GiB/TiB: Binary (powers of 1024)
- Both available in same category

**Display:** Always show full precision for data sizes (developers need exact values)

### Same-Unit Conversion

When FROM and TO are the same unit (e.g., meter → meter):
- **Display "1" in both fields**
- Clears any previous user input

---

## Visual Theme and Styling

### Color Scheme (Consistent with Dark Theme)

| Element | Hex Code | Usage |
|---------|----------|-------|
| Background | `#2d2d2d` | Main window background |
| Panel background | `#1c1c1c` | Input fields, history |
| Default button | `#4a4a4a` | Digits, unit buttons |
| Active category | `#ff9500` | Selected category button |
| Inactive category | `#3a3a3a` | Unselected category buttons |
| Swap button | `#5856d6` | Purple function color |
| Clear buttons | `#ff3b30` | C, CE, backspace |
| Equals button | `#ff9500` | Orange operator color |
| Text color | `#ffffff` | All text |
| Secondary text | `#888888` | Labels ("FROM", "TO") |
| Focus border | `#ff9500` | Focused input field |
| Border | `#3a3a3a` | Default borders |

### Font Specifications

| Element | Font | Size |
|---------|------|------|
| Category buttons | Segoe UI | 11pt |
| Unit dropdowns | Segoe UI | 12pt |
| Input fields | Segoe UI | 20pt |
| Labels | Segoe UI | 12pt |
| Quick unit buttons | Segoe UI | 12pt |
| Keypad buttons | Segoe UI | 16pt |
| History items | Segoe UI | 11pt |

### Widget Styling

**Input field styling:**
```python
self.from_input.setStyleSheet("""
    QLineEdit {
        background-color: #1c1c1c;
        color: white;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 10px;
        font-size: 20pt;
    }
    QLineEdit:focus {
        border-color: #ff9500;
    }
""")
```

**Dropdown (QComboBox) styling:**
```python
self.from_dropdown.setStyleSheet("""
    QComboBox {
        background-color: #3a3a3a;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px;
        font-size: 12pt;
    }
    QComboBox:hover {
        background-color: #4a4a4a;
    }
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);  /* or use text: ▼ */
    }
    QComboBox QAbstractItemView {
        background-color: #2d2d2d;
        color: white;
        selection-background-color: #ff9500;
    }
""")
```

**Context menu:** Enabled on input fields (standard Copy, Paste, Select All)

**Copy behavior:** Copies number only (e.g., "328.084", not "328.084 ft")

---

## Error Handling

### Conversion Errors

| Error | Cause | Display | Recovery |
|-------|-------|---------|----------|
| Unknown unit | Unit not in category | "Error" in result field | Clear on next input |
| Unknown category | Invalid category name | Should not occur (UI controlled) | N/A |
| Parse error | Invalid number format | Keep previous value | User corrects input |
| Overflow | Result exceeds float range | "Overflow" or scientific notation | Clear on next input |

### Input Errors

| Input | Behavior |
|-------|----------|
| Multiple decimal points | Ignore second `.` |
| Letters | Ignore (no effect) |
| Minus key | Ignore (use +/− button) |
| Leading zeros | Allow (treated as 0.xxx) |
| Empty after backspace | Display "0" |

---

## Accessibility

### Screen Reader Support
- All buttons have descriptive ARIA labels
- Category changes announced: "Switched to Length category"
- Unit changes announced: "From unit changed to meter"
- Results announced: "Result: 328.084 feet"

### Keyboard Navigation
- **Full keyboard control without mouse**
- **Tab cycles through all interactive elements** (category buttons → FROM dropdown → FROM input → Swap → TO dropdown → TO input → Quick units → Keypad → History)
- Enter/Space activates buttons
- Arrow keys navigate within category row and quick unit row

### High Contrast
- Respect system high contrast settings
- Ensure all text meets WCAG 2.1 AA contrast ratio (4.5:1)

---

## State Persistence

### Remember Between Sessions
- Last used category
- Last used FROM unit per category
- Last used TO unit per category

### Within Session (Category Switch)
- **Reset to default units** when switching categories
- Do NOT remember per-category units within session

### On Startup
- Restore last category and units from previous session
- If no prior session, default to Length (meter → foot)
- History does NOT persist between sessions (same as other modes)

### Storage Location
- Use same mechanism as Programmer Mode state persistence
- Store in user preferences/settings file

---

## File Structure

### New Files to Create

1. **`src/calculator/converter.py`**
   - Pure conversion functions
   - Unit data (factors, metadata)
   - Category definitions
   - No UI imports

2. **`tests/test_converter.py`**
   - Unit tests for all conversion functions
   - Edge case tests (temperature, overflow)
   - Parameterized tests for each category

### Existing Files to Modify

1. **`src/calculator/gui.py`**
   - Add `ConverterModeWidget` class
   - Modify `CalculatorWindow._setup_ui()` to add converter widget to stack
   - Modify `ModeSidebar` to add converter button
   - Modify `_switch_mode()` to handle "converter" mode
   - Add keyboard shortcut handling for converter mode

2. **`src/calculator/history.py`**
   - Add `ConverterHistoryEntry` dataclass

3. **`CLAUDE.md`**
   - Add converter mode section to GUI Rules
   - Document converter.py patterns in Architecture section

---

## Summary of Key Decisions

| Aspect | Decision |
|--------|----------|
| Internal representation | Float in base unit (no integer limitation) |
| Source of truth | **Last-edited field** — whichever field was edited most recently |
| Conversion architecture | Always FROM → base → TO (no chained conversions) |
| Temperature handling | Special functions (non-linear), kelvin as internal base |
| Absolute zero | **Silent clamp** to 0 K (no visual feedback) |
| Data storage | Support both decimal (KB) and binary (KiB) units |
| Bidirectional editing | Both FROM and TO fields are editable |
| Real-time updates | Convert on every keystroke |
| Precision | 10 significant digits display, full float internally |
| Rounding | **Round half-even** (banker's rounding) |
| Thousand separators | **Enabled** (e.g., 1,234,567) |
| Negative values | **+/− button only** (minus key ignored) |
| Overflow | Scientific notation for very large/small values |
| History format | `{value} {abbr} = {result} {abbr} [{category}]` |
| History trigger | **Explicit = only** (no auto-record on pause) |
| Duplicate history | **Allowed** (pressing = multiple times adds entries) |
| History recall | **Auto-switches category** when double-clicking entry |
| Quick unit behavior | Click = FROM, Shift+click = TO (touch users use dropdowns) |
| Quick unit layout | **Left-aligned** (sparse rows like Temperature stay left) |
| Category switch | Clears input values, **resets to default units**, preserves history |
| Mode switch | Clears history (same as existing modes) |
| Swap button | **Swaps units AND values** |
| Same-unit conversion | **Show "1" in both fields** |
| Default focus | FROM field |
| Keyboard shortcuts | **F6-F13** for all 8 categories |
| Tab behavior | **Full widget cycle** through all interactive elements |
| Escape behavior | **Always clears** (like C button) |
| State persistence | Remember last category and units across sessions |
| Unit dropdown format | **Abbreviation + name** (e.g., "m - meter") |
| Unicode superscripts | **Enabled** (m², km², m³) |
| Keypad layout | 4x4 grid, **shrinks proportionally** with window |
| UI component | `CalculatorButton` for all buttons (per GUI rules) |
| Dropdown component | `QComboBox` for unit selection |
| Layout pattern | Match Programmer Mode (calc on left, history on right) |
| Context menu | **Enabled** on input fields |
| Copy format | **Number only** (no unit) |
| Paste behavior | **Strip non-numeric** characters |
| Year definition | **365 days** (simple, not Gregorian average) |
| Gallon abbreviations | **gal / gal UK** (asymmetric, US gallon more common) |
| Speed units | Include **Mach** |
| Time precision | **Millisecond** as smallest (no μs/ns) |

---

## Future Enhancements (Post-MVP)

**Potential additions not in initial scope:**
- Currency conversion (requires API integration)
- Custom unit definitions
- Conversion formula display ("1 m = 3.28084 ft")
- Favorites/pinned conversions
- Copy result to clipboard button
- Unit converter widget for embedding in other modes
- Conversion chains (e.g., "100 km/h in ft/min")
- Angle conversions (degrees, radians, gradians)
- Pressure conversions (bar, psi, atm, pascal)
- Energy conversions (joule, calorie, BTU, kWh)
- Microsecond and nanosecond time units

---

## End of Specification

This specification is comprehensive and ready for implementation. All major questions about behavior, UI layout, interactions, data model, and edge cases have been addressed. The design follows existing patterns from Programmer Mode and integrates cleanly with the current codebase.
