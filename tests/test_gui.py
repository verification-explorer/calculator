"""Tests for calculator.gui module."""

import pytest

pytest.importorskip("PyQt6")

from calculator.gui import CalculatorWindow, CalculatorButton


class TestCalculatorButton:
    """Tests for the CalculatorButton class."""

    def test_button_creation(self, qtbot):
        """Test that a calculator button can be created."""
        btn = CalculatorButton("5")
        qtbot.addWidget(btn)
        assert btn.text() == "5"

    def test_button_with_custom_color(self, qtbot):
        """Test button with custom color."""
        btn = CalculatorButton("+", "#ff9500")
        qtbot.addWidget(btn)
        assert btn.text() == "+"


class TestCalculatorWindow:
    """Tests for the CalculatorWindow class."""

    def test_window_creation(self, qtbot):
        """Test that the main window can be created."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        assert window.windowTitle() == "Calculator"

    def test_initial_display(self, qtbot):
        """Test initial display shows 0."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        assert window.display.text() == "0"

    def test_number_input(self, qtbot):
        """Test entering numbers."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("5")
        assert window.display.text() == "5"
        window._on_button_click("3")
        assert window.display.text() == "53"

    def test_clear(self, qtbot):
        """Test clear functionality."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("5")
        window._on_button_click("C")
        assert window.display.text() == "0"

    def test_addition(self, qtbot):
        """Test addition calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("5")
        window._on_button_click("+")
        window._on_button_click("3")
        window._on_button_click("=")
        assert window.display.text() == "8"

    def test_subtraction(self, qtbot):
        """Test subtraction calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("9")
        window._on_button_click("-")
        window._on_button_click("4")
        window._on_button_click("=")
        assert window.display.text() == "5"

    def test_multiplication(self, qtbot):
        """Test multiplication calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("6")
        window._on_button_click("*")
        window._on_button_click("7")
        window._on_button_click("=")
        assert window.display.text() == "42"

    def test_division(self, qtbot):
        """Test division calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("1")
        window._on_button_click("5")
        window._on_button_click("/")
        window._on_button_click("3")
        window._on_button_click("=")
        assert window.display.text() == "5"

    def test_division_by_zero(self, qtbot):
        """Test division by zero shows error."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("5")
        window._on_button_click("/")
        window._on_button_click("0")
        window._on_button_click("=")
        assert window.display.text() == "Error"

    def test_square_root(self, qtbot):
        """Test square root calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("1")
        window._on_button_click("6")
        window._on_button_click("√")
        assert window.display.text() == "4"

    def test_square_root_negative(self, qtbot):
        """Test square root of negative shows error."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window.current_input = "-4"
        window._calculate_sqrt()
        assert window.display.text() == "Error"

    def test_power(self, qtbot):
        """Test power calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("2")
        window._on_button_click("^")
        window._on_button_click("8")
        window._on_button_click("=")
        assert window.display.text() == "256"

    def test_modulo(self, qtbot):
        """Test modulo calculation."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("1")
        window._on_button_click("7")
        window._on_button_click("%")
        window._on_button_click("5")
        window._on_button_click("=")
        assert window.display.text() == "2"

    def test_decimal_input(self, qtbot):
        """Test decimal number input."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("3")
        window._on_button_click(".")
        window._on_button_click("1")
        window._on_button_click("4")
        assert window.display.text() == "3.14"

    def test_history_tracking(self, qtbot):
        """Test that calculations are added to history."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("2")
        window._on_button_click("+")
        window._on_button_click("2")
        window._on_button_click("=")
        assert len(window.history) == 1
        assert window.history_list.count() == 1

    def test_clear_history(self, qtbot):
        """Test clearing history."""
        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._on_button_click("1")
        window._on_button_click("+")
        window._on_button_click("1")
        window._on_button_click("=")
        window._clear_history()
        assert len(window.history) == 0
        assert window.history_list.count() == 0
