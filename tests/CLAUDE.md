# Testing Instructions

Applies when working with files in `tests/`.

## Framework & Fixtures

- Use **pytest** — not unittest
- Shared fixtures are in `conftest.py`: `empty_history`, `populated_history`, `sample_history_entries`
- Use `@pytest.mark.parametrize` for input variations — do not write repetitive test functions

## Running Tests

```bash
# All tests
venv/bin/pytest tests/ -v

# Single class
venv/bin/pytest tests/test_core.py::TestDivide -v

# With coverage
venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing
```

## GUI Tests

- GUI tests in `test_gui.py` require a `QApplication` instance
- Use the existing `qt_app` fixture pattern — do not instantiate `QApplication` directly in tests

## Rules

- Every new function in `core.py` needs a corresponding test class in `test_core.py`
- Every new public method in `programmer.py` needs coverage in `test_programmer.py`
- Tests must not depend on execution order
- Do not hardcode timestamps — use fixtures or `datetime.now()`
