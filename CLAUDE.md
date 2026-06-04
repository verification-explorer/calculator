# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Identity

Python 3.10+ calculator application with a CLI and a PyQt6 GUI. Source lives in `src/calculator/`. Entry points: `calc` (CLI) and `calc-gui` (GUI).

## Architecture

Three core layers:

- **core.py** - Pure mathematical functions. All raise `ValueError` for invalid inputs. Type alias `Number = Union[int, float]` used throughout.
- **history.py** - `CalculationHistory` class with `HistoryEntry` dataclass for tracking calculations with timestamps.
- **cli.py** - REPL interface that parses expressions via regex, delegates to core functions, stores results in history.
- **gui.py** - PyQt6 GUI with Standard and Programmer modes via `QStackedWidget`.
- **programmer.py** / **programmer_parser.py** - Programmer mode logic and expression parser.

## Commands

```bash
# Install for development
pip install -e ".[dev]"

# Install with GUI support
pip install -e ".[dev,gui]"

# Run CLI
calc

# Run GUI
calc-gui

# Build docs
cd docs && make html
```

<important if="you are writing, running, or modifying tests">
## Testing
During implementation, Claude Code may write tests to verify its own work.
After implementation is complete, run @test-writer to produce the final
spec-driven test suite, which replaces any temporary implementation tests.

```bash
# Run all tests
pytest tests/ -v

# Run specific test class or method
pytest tests/test_core.py::TestDivide -v
pytest tests/test_core.py::TestDivide::test_divide_by_zero_raises_value_error -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

- Use **pytest** — not unittest
- Use `@pytest.mark.parametrize` for input variations — do not write repetitive test functions
- Shared fixtures are in `conftest.py`: `empty_history`, `populated_history`, `sample_history_entries`
- Every new function in `core.py` needs a corresponding test class in `test_core.py`
- Every new public method in `programmer.py` needs coverage in `test_programmer.py`
- Tests must not depend on execution order
- GUI tests require a `QApplication` instance — use the existing `qt_app` fixture pattern
</important>

<important if="you are working on the GUI, modifying gui.py, or adding new UI components">
## GUI Rules

- PyQt6 version 6.4.0+ — do not use PyQt5 or PySide2/6 APIs
- Always reuse `CalculatorButton` — never create a raw `QPushButton` in calculator views
- Match the existing dark theme; do not introduce new colors without a strong reason
- Mode switching uses `QStackedWidget` — do not open new windows
- The sidebar overlays the layout — it does not push content
- Histories clear on mode switch

### Color Constants

| Role | Hex |
|---|---|
| Default button | `#4a4a4a` |
| Operator button | `#ff9500` (orange) |
| Clear/error button | `#ff3b30` (red) |
| Function button | `#5856d6` (purple) |
| Active base accent | `#ff9500` (orange) |
| Background | `#1c1c1e` |
| Display background | `#2c2c2e` |
</important>

<important if="you are implementing or modifying Programmer Mode">
## Programmer Mode Specification

Full specification available in `specs/programmer_mode.md`. Key implementation details:

### UI Layout (Top to Bottom)
1. **Integer Size Selector** - Radio buttons (Byte/Word/DWord/QWord)
2. **Carry Flag Indicator** - Checkbox/LED next to bit display, manual and automatic control
3. **Bit Display Panel** - Interactive LED-style boxes showing individual bits, grouped by nibbles
   - Click to toggle individual bits
   - Changed bits flash orange on operations
4. **Base Panels (HEX/DEC/OCT/BIN)** - Button + editable text field for each base
   - Active base highlighted with accent color
   - All fields update in real-time on every keystroke
   - Invalid characters silently ignored
   - Base switching preserves value via internal canonical representation
5. **Bit Manipulation Panel** - Bitwise/Bitshift buttons open floating overlays
   - Bitwise: AND, OR, NOT, NAND, NOR, XOR (2×3 grid)
   - Bitshift: Arithmetic, Logical, Rotate, Rotate-through-carry (vertical stack)
6. **Main Display** - Full expression with horizontal scroll
7. **Keyboard Panel** - 6×5 grid with hex digits (A-F), numbers (0-9), operators, parentheses, swap (⇄)

### Core Behaviors
- Internal canonical value is a **64-bit integer** — all conversions go through it, no chained conversions
- Overflow: block digit entry when exceeding integer size; truncate silently on size change
- Negative numbers use two's complement (e.g., -1 in Byte = 0xFF)
- NOT operation is unary, operates immediately on display value
- History stores base and size with each entry: `0xFF AND 0x0F = 0x0F [HEX, Byte]`
- State persistence: restore last mode/base/size/carry flag on startup

### Keyboard Shortcuts
- **F2/F3/F4/F5**: Switch to HEX/DEC/OCT/BIN
- **0-9, A-F**: Direct input
- **Enter/=**: Execute, **Backspace**: Delete, **Escape**: Clear entry
- **Ctrl+Shift+X**: Swap operands
</important>


