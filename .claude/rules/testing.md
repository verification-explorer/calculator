---
paths:
  - "tests/*.py"
---

# Testing Rules

- Use **pytest** — not unittest
- Use `@pytest.mark.parametrize` for input variations — do not write repetitive test functions
- Shared fixtures are in `conftest.py`: `empty_history`, `populated_history`, `sample_history_entries`
- Every new function in `core.py` needs a corresponding test class in `test_core.py`
- Every new public method in `programmer.py` needs coverage in `test_programmer.py`
- Tests must not depend on execution order
- Do not hardcode timestamps — use fixtures or `datetime.now()`
- GUI tests require a `QApplication` instance — use the existing `qt_app` fixture pattern
