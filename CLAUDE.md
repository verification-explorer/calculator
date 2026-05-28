# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install for development
pip install -e ".[dev]"

# Install with GUI support
pip install -e ".[dev,gui]"

# Run tests
pytest tests/ -v

# Run specific test class or method
pytest tests/test_core.py::TestDivide -v
pytest tests/test_core.py::TestDivide::test_divide_by_zero_raises_value_error -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run CLI
calc

# Build docs
cd docs && make html
```

## Architecture

Python 3.10+ calculator with three layers in `src/calculator/`:

- **core.py** - Pure mathematical functions (add, subtract, multiply, divide, power, square_root, modulo). All raise `ValueError` for invalid inputs (division by zero, negative square root).
- **history.py** - `CalculationHistory` class with `HistoryEntry` dataclass for tracking calculations with timestamps.
- **cli.py** - REPL interface that parses expressions via regex, delegates to core functions, and stores results in history.

Entry points defined in pyproject.toml: `calc` (CLI) and `calc-gui` (GUI).

Type alias `Number = Union[int, float]` is used throughout for numeric parameters.

## GUI

The GUI is built with **PyQt6 (6.4.0+)** and launched via the `calc-gui` entry point.

### Standard Mode
The existing calculator mode featuring:
- Dark theme with red/orange/purple/gray color scheme
- Arithmetic operations, trig functions (sin, cos, tan, inv, rad)
- Calculation history panel with clear history support

### Programmer Mode
A planned mode for software developers, embedded engineers, and anyone working with binary or hexadecimal numbers. It coexists with Standard mode via a mode-switcher UI element that feels native to the existing dark theme.

**Number system conversions:** DEC, HEX, OCT, BIN

**Bitwise operations:** AND, OR, XOR, NOT, left shift `<<`, right shift `>>`

**Integer size selection:** Byte (8-bit), Word (16-bit), DWord (32-bit), QWord (64-bit)

## Programmer Mode Specification

Full specification available in `specs/programmer_mode.md`. Key implementation details:

### UI Layout (Top to Bottom)
1. **Integer Size Selector** - Radio buttons (Byte/Word/DWord/QWord)
2. **Carry Flag Indicator** - Checkbox/LED next to bit display, manual and automatic control
3. **Bit Display Panel** - Interactive LED-style boxes showing individual bits, grouped by nibbles (4 bits)
   - Click to toggle individual bits
   - Changed bits flash orange on operations
   - Full ARIA accessibility with keyboard navigation
4. **Base Panels (HEX/DEC/OCT/BIN)** - Button + editable text field for each base
   - Active base highlighted with accent color
   - All fields update in real-time on every keystroke
   - Invalid characters silently ignored
   - Base switching preserves value via internal canonical representation
5. **Bit Manipulation Panel** - Bitwise/Bitshift buttons open floating overlays
   - Bitwise: AND, OR, NOT, NAND, NOR, XOR (2×3 grid)
   - Bitshift: Arithmetic, Logical, Rotate, Rotate-through-carry (vertical stack)
   - Auto-close after selection
6. **Main Display** - Full expression with horizontal scroll (show rightmost)
7. **Keyboard Panel** - 6×5 grid with hex digits (A-F), numbers (0-9), operators, parentheses, swap (⇄)

### Core Behaviors
- **Base switching**: Converts and displays value in new base, preserves precision via internal 64-bit canonical value
- **Overflow handling**: Block digit entry when exceeding integer size; truncate silently on size change
- **Negative numbers**: Two's complement representation (e.g., -1 in Byte = 0xFF)
- **Operation precedence**: Left-to-right evaluation (calculator style), full recursive parentheses support
- **NOT operation**: Unary, operates immediately on display value
- **Shift operations**: Amount respects current base mode, overflow wraps (modulo bit width)
  - Arithmetic shift: sign-extends
  - Logical shift: zero-fills
  - Rotate: bits wrap around
  - Rotate through carry: uses carry flag in rotation
- **Mode transition**: Preserve value, clear operation when switching Standard ↔ Programmer
- **History**: Stores base and size with each entry: `0xFF AND 0x0F = 0x0F [HEX, Byte]`
- **State persistence**: Restore last mode/base/size/carry flag on startup

### Keyboard Shortcuts
- **F2/F3/F4/F5**: Switch to HEX/DEC/OCT/BIN
- **0-9, A-F**: Direct input
- **+, -, *, /, %, (, )**: Operators and grouping
- **Enter/=**: Execute, **Backspace**: Delete, **Escape**: Clear entry
- **Ctrl+Shift+X**: Swap operands

### Technical Implementation
- Internal canonical value: 64-bit integer
- Display base separate from internal representation
- No chained conversions (all convert from canonical value)
- Expression parser with full parentheses support (recursive descent or shunting-yard)
- Invalid input silently ignored, overflow blocked during typing
- Division by zero shows error, clears on next input

## Testing

Tests use pytest with shared fixtures in `conftest.py` (`sample_history_entries`, `populated_history`, `empty_history`). Core tests use `@pytest.mark.parametrize` extensively for input variations.