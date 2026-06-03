---
paths:
  - "src/calculator/gui.py"
  - "src/calculator/programmer.py"
---

# GUI Rules

- Always reuse `CalculatorButton` — never create a raw `QPushButton` in calculator views
- Match the existing dark theme; do not introduce new colors without a strong reason
- Mode switching uses `QStackedWidget` — do not open new windows
- The sidebar overlays the layout — it does not push content
- Histories clear on mode switch
- PyQt6 version 6.4.0+ — do not use PyQt5 or PySide2/6 APIs
