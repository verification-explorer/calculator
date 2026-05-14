# Calculator

A simple yet powerful calculator application built in Python, featuring core mathematical operations, calculation history tracking, and an interactive command-line interface.

## Features

- **Core Operations**: Addition, subtraction, multiplication, division, power, square root, and modulo
- **History Tracking**: Keep track of your calculations with timestamps
- **Interactive CLI**: User-friendly command-line interface for quick calculations
- **Comprehensive API**: Use the calculator programmatically in your Python code

## Installation

### Basic Installation

```bash
pip install calculator
```

### Development Installation

```bash
git clone <repository-url>
cd calculator
pip install -e ".[dev]"
```

## Quick Start

### Command Line

```bash
calc
```

```
Calculator - Type 'help' for commands, 'quit' to exit

calc> 5 + 3
  = 8
calc> sqrt(16)
  = 4.0
calc> history
Calculation History:
  1. 5 + 3 = 8
  2. sqrt(16) = 4.0
calc> quit
Goodbye!
```

### Python API

```python
from calculator import add, subtract, multiply, divide, power, square_root, modulo

result = add(5, 3)          # 8
result = divide(15, 3)      # 5.0
result = power(2, 8)        # 256
result = square_root(16)    # 4.0
```

## Supported Operations

| Operation      | CLI Syntax   | Python Function    |
|----------------|--------------|-------------------|
| Addition       | `5 + 3`      | `add(5, 3)`       |
| Subtraction    | `10 - 4`     | `subtract(10, 4)` |
| Multiplication | `6 * 7`      | `multiply(6, 7)`  |
| Division       | `15 / 3`     | `divide(15, 3)`   |
| Power          | `2 ^ 8`      | `power(2, 8)`     |
| Square Root    | `sqrt(16)`   | `square_root(16)` |
| Modulo         | `17 % 5`     | `modulo(17, 5)`   |

## CLI Commands

- `help` - Show help information
- `history` - Display calculation history
- `clear` - Clear calculation history
- `quit` - Exit the calculator

## Running Tests

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Building Documentation

```bash
cd docs
make html
```

Open `docs/_build/html/index.html` in your browser.

## License

MIT License
