# GUI Layer — PyQt6 Instructions

Applies when working with files in `src/calculator/`.

## Framework

- **PyQt6 version 6.4.0+** — do not use PyQt5 or PySide2/6 APIs
- Entry point: `calc-gui` (defined in pyproject.toml)

## Key Classes

- `CalculatorButton` — reuse for all buttons; accepts `text` and `color` parameters
- `CalculationHistory` — shared history model between Standard and Programmer modes

## Color Constants (dark theme)

| Role | Hex |
|---|---|
| Default button | `#4a4a4a` |
| Operator button | `#ff9500` (orange) |
| Clear/error button | `#ff3b30` (red) |
| Function button | `#5856d6` (purple) |
| Active base accent | `#ff9500` (orange) |
| Background | `#1c1c1e` |
| Display background | `#2c2c2e` |

## Rules

- Always reuse `CalculatorButton` — never create raw `QPushButton` in calculator views
- Match the existing dark theme; do not introduce new colors without a strong reason
- Mode switching changes window content via `QStackedWidget` — do not open new windows
- Histories clear on mode switch
- The sidebar (mode switcher) overlays the layout — it does not push content
