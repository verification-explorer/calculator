---
paths:
  - "src/calculator/core.py"
  - "src/calculator/programmer.py"
  - "src/calculator/programmer_parser.py"
---

# Core Logic Rules

- All functions must raise `ValueError` for invalid inputs (division by zero, negative square root, etc.)
- Use the `Number = Union[int, float]` type alias for numeric parameters — do not use raw `int | float`
- Pure functions only — no side effects, no state, no UI imports
- Programmer mode internal representation is a **64-bit integer** — all conversions go through it
- No chained conversions — always convert from the canonical value directly to the target base
