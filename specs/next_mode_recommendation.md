# Next Mode Recommendation: Date Calculation Mode

## Executive Summary

The app now has three modes: Standard (arithmetic + trig), Programmer (bitwise + base conversion), and Unit Converter (physical measurements). After researching the full landscape of calculator app modes — Windows Calculator, macOS Calculator, Android/iOS scientific apps, and financial calculators — the recommended next mode is **Date Calculation Mode**.

It is the single most prominent calculator feature that this app is still missing, it requires no external APIs or network access, and PyQt6 ships with native date widgets (`QDateEdit`, `QCalendarWidget`) that make the implementation straightforward.

---

## Mode Name

**Date Calculator**

---

## What It Does

Date Calculator Mode provides two distinct sub-modes, selectable via toggle buttons at the top of the panel:

### Sub-mode 1: Date Difference

The user enters two dates (Start and End). The mode calculates and displays the span between them in multiple units simultaneously:

- Total days
- Weeks and remaining days
- Months and remaining days (approximate, using calendar months)
- Years, months, and remaining days (human-readable form)
- Business days only (excluding Saturdays and Sundays)

Example output for Jan 1, 2024 to Jun 4, 2026:
```
885 days total
126 weeks, 3 days
29 months, 3 days
2 years, 5 months, 3 days
633 business days
```

### Sub-mode 2: Add / Subtract Duration

The user enters a starting date and a duration (years, months, weeks, days), then chooses to add or subtract. The result is the new calendar date.

Example: Jan 1, 2024 + 90 days = March 31, 2024.

Optional: a "business days only" toggle that skips weekends when counting forward or backward.

---

## Why It Fits This App

### 1. Closes the Last Major Gap vs. Windows Calculator

Windows Calculator ships with four main modes: Standard, Scientific, Programmer, and Date Calculation. This app has covered the equivalent of the first three. Date Calculation is the obvious remaining entry in that list, and it is the one users most frequently ask about.

### 2. No External Dependencies

Unlike currency conversion (requires live exchange rates) or graphing (requires a plotting engine), date math is entirely self-contained in Python's `datetime` standard library and PyQt6's `QDate`. No new packages need to be added to the project.

### 3. PyQt6 Provides First-Class Date Widgets

PyQt6 includes `QDateEdit` (a spinner-style date input with up/down arrows) and `QCalendarWidget` (a full month-view calendar picker). Both are mature, keyboard-navigable, and work cleanly in the existing dark theme with a stylesheet override. No custom widget needs to be built from scratch.

### 4. Broad and Concrete Use Cases

Date difference calculations are used daily in project management, legal deadlines, HR (tenure calculations), healthcare (age, gestational weeks), finance (bond maturity), and everyday planning (days until an event). The business-days feature alone makes this mode useful for anyone managing deliverables.

### 5. Consistent Architecture

Date Calculation Mode requires a new `date_calc.py` core module (pure functions, no UI, raises `ValueError` for invalid inputs) following the same pattern as `core.py`, `programmer.py`, and `converter.py`. The UI widget follows the same `QWidget` subclass pattern as `StandardModeWidget`, `ProgrammerModeWidget`, and `ConverterModeWidget`. The sidebar gets a fourth entry. Nothing architectural needs to change.

### 6. History Integration is Trivial

The existing `CalculationHistory` class stores string expressions and results. A date calculation entry can be rendered as a plain string and stored the same way: `"Jan 1, 2024 to Jun 4, 2026 = 885 days"`.

---

## Key Buttons and Inputs

### Sub-mode Toggle

Two `CalculatorButton` widgets at the top, styled like Programmer Mode's size selector (radio-style, one active at a time):

- `Date Difference` (active by default)
- `Add / Subtract`

### Date Difference Sub-mode

| Control | Widget | Purpose |
|---------|--------|---------|
| Start Date | `QDateEdit` | First date input |
| End Date | `QDateEdit` | Second date input |
| Calendar icon button | `CalculatorButton` | Opens `QCalendarWidget` popup |
| Swap button | `CalculatorButton` ("#5856d6") | Swaps start and end dates |
| Business days toggle | Checkable `CalculatorButton` | Excludes weekends from count |
| Calculate button | `CalculatorButton` ("#ff9500") | Triggers calculation (also auto-calculates on any change) |
| Results panel | `QLabel` rows | Shows all output formats simultaneously |

### Add / Subtract Sub-mode

| Control | Widget | Purpose |
|---------|--------|---------|
| Start Date | `QDateEdit` | Base date |
| Years field | `QSpinBox` (0–999) | Years to add/subtract |
| Months field | `QSpinBox` (0–11) | Months to add/subtract |
| Weeks field | `QSpinBox` (0–52) | Weeks to add/subtract |
| Days field | `QSpinBox` (0–365) | Days to add/subtract |
| Add / Subtract toggle | Pair of `CalculatorButton` | Direction of operation |
| Business days toggle | Checkable `CalculatorButton` | Skip weekends when counting days |
| Result label | `QLabel` (large font) | Resulting date, prominently displayed |
| Result day label | `QLabel` (smaller, gray) | Day of week of the result |

### History Panel

Same right-side history panel as all other modes: `QListWidget` + "Clear History" button, shared via `self.parent.history_list`.

---

## Rough UI Layout

```
+--------------------------------------------------------------------+
| [=] Calculator                                                      |  <- toolbar
+--------------------------------------------------------------------+
| [Date Difference]  [Add / Subtract]                                 |  <- sub-mode toggle
+--------------------------------------------------------------------+
|                                                                      |
|   START DATE                        END DATE                        |
|   [ Jan  1 2024  v ] [cal]          [ Jun  4 2026  v ] [cal]       |
|                                                                      |
|                  [ Swap  <=>  ]                                      |
|                                                                      |
|   [ Business days only ]                                            |
|                                                                      |
+--------------------------------------------------------------------+
|                                                                      |
|   885 days                                                          |  <- primary result (large)
|                                                                      |
|   126 weeks, 3 days                                                 |
|   29 months, 3 days                                                 |
|   2 years, 5 months, 3 days                                         |
|   633 business days                                                 |
|                                                                      |
+--------------------------------------------------------------------+
|                         HISTORY                                     |
|   Jan 1, 2024 to Jun 4, 2026 = 885 days                            |
|   ...                                                               |
+--------------------------------------------------------------------+
```

For Add/Subtract sub-mode:

```
+--------------------------------------------------------------------+
| [Date Difference]  [Add / Subtract]                                 |
+--------------------------------------------------------------------+
|                                                                      |
|   START DATE                                                         |
|   [ Jan  1 2024  v ] [cal]                                          |
|                                                                      |
|   [+  Add  ]  [-  Subtract  ]                                       |
|                                                                      |
|   Years  [ 2 v ]   Months [ 5 v ]   Weeks [ 0 v ]   Days [ 3 v ]  |
|                                                                      |
|   [ Business days only ]                                            |
|                                                                      |
+--------------------------------------------------------------------+
|                                                                      |
|   June 4, 2026                                                      |  <- primary result
|   Wednesday                                                          |
|                                                                      |
+--------------------------------------------------------------------+
|                         HISTORY                                     |
|   Jan 1, 2024 + 2y 5m 3d = Jun 4, 2026 (Wed)                      |
|   ...                                                               |
+--------------------------------------------------------------------+
```

### Color Application (Consistent with Dark Theme)

| Element | Color |
|---------|-------|
| Active sub-mode button | `#ff9500` (orange) |
| Inactive sub-mode button | `#3a3a3a` |
| Add/Subtract direction buttons | `#4a4a4a` / active `#ff9500` |
| Swap button | `#5856d6` (purple) |
| Business days toggle (on) | `#ff9500` |
| Business days toggle (off) | `#3a3a3a` |
| Calendar popup button | `#4a4a4a` |
| Primary result text | white, 28pt |
| Secondary result rows | `#888888`, 13pt |
| `QDateEdit` background | `#2c2c2e` |

---

## Core Module: `date_calc.py`

Follows the `core.py` pattern: pure functions, no UI imports, `ValueError` for invalid inputs.

Key functions:

```python
def days_between(start: date, end: date) -> int: ...
def business_days_between(start: date, end: date) -> int: ...
def decompose_days(total_days: int) -> dict: ...  # weeks, months, years breakdown
def add_duration(start: date, years: int, months: int, weeks: int, days: int) -> date: ...
def add_business_days(start: date, days: int) -> date: ...
def subtract_duration(start: date, years: int, months: int, weeks: int, days: int) -> date: ...
```

All functions use Python's standard `datetime.date` type. No third-party libraries required.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F6` | Switch to Date Difference sub-mode |
| `F7` | Switch to Add/Subtract sub-mode |
| `Tab` | Move between date fields and spinboxes |
| `Enter` / `=` | Record current result to history |
| `Escape` | Reset all fields to today's date |
| `Ctrl+Shift+S` | Swap start and end dates |

F6/F7 continue the F-key convention established by Programmer Mode (F2-F5 for bases) and Converter Mode (F6-F13 for categories in the existing implementation).

---

## Alternatives Considered and Rejected

### Scientific Mode (Expanded)

The Standard mode already has sin, cos, tan, inverse trig, power, sqrt, and percent. Expanding further (logs, hyperbolic functions, factorials, constants like pi/e) would add more buttons to an already capable mode. The marginal value is low: users who need deeper scientific functions use Wolfram Alpha or a dedicated app. Scientific mode expansion is an incremental improvement, not a new mode.

### Financial / TVM Mode

Time Value of Money calculations (NPV, IRR, loan amortization, bond pricing) are high-value for financial professionals. However, the app's existing audience is developers (the Programmer mode is the most distinctively positioned feature). TVM mode would require a domain-specific UI quite different from the rest of the app, and the formulas (especially IRR, which is iterative) have no clean fit in the existing `core.py` pure-function model. This is a viable future mode for a "professional" tier but not the natural next step.

### Graphing Mode

Plotting functions requires either embedding a third-party widget (matplotlib in Qt, pyqtgraph) or building a custom renderer. Both paths add significant dependency weight and implementation complexity. Graphing is a full sub-application, not a calculator mode. Windows Calculator added this years after launch, and Desmos already dominates the web. Ruled out as out of scope.

### Currency Conversion

Currency conversion is the most-requested converter category that the existing Unit Converter mode does not include. However, live exchange rates require a network API, which introduces a dependency, a potential failure mode, and a privacy consideration. A static fallback would rapidly become stale. This is better addressed as an optional enhancement to the existing Converter mode (with a user-supplied API key) rather than a new standalone mode.

---

## Why Date Calculation Wins

1. **Completes the Windows Calculator feature set**: Standard, Programmer, Unit Converter, Date Calculator are exactly the four modes Windows Calculator ships with. This is a well-validated set.

2. **Zero new dependencies**: Python `datetime` is in the standard library. `QDateEdit` and `QCalendarWidget` are already part of PyQt6.

3. **Clean architectural fit**: One new `date_calc.py` core module, one new `DateCalcModeWidget` class, one new sidebar entry. The pattern is identical to every other mode.

4. **Genuine utility**: Project deadlines, contract terms, age calculations, days until events — these are concrete, everyday needs that users reach for a calculator to solve.

5. **Business days feature differentiates it**: Most standalone date calculators on the web offer only calendar days. A business-days mode (skip weekends) adds meaningful value over a quick web search.

6. **History entries are human-readable without ambiguity**: `"Jan 1, 2024 to Jun 4, 2026 = 885 days"` is self-contained, unlike a unit conversion entry which requires knowing the units were stored correctly.

---

*Recommendation prepared: 2026-06-04*
*Based on analysis of: gui.py, specs/programmer_mode.md, CLAUDE.md, and the existing ConverterModeWidget implementation, plus research on Windows Calculator, macOS Calculator, Android/iOS scientific calculator apps, and financial calculator applications.*
