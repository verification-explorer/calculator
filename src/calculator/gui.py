"""Graphical user interface for the calculator using PyQt6.

This module provides a GUI that uses the existing core and history modules,
demonstrating the separation of concerns in the calculator architecture.
"""

import sys
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from calculator import core
from calculator.history import CalculationHistory


class CalculatorButton(QPushButton):
    """A styled calculator button."""

    def __init__(self, text: str, color: str = "#4a4a4a"):
        super().__init__(text)
        self.setMinimumSize(60, 60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setFont(QFont("Segoe UI", 16))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {self._lighten(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken(color)};
            }}
        """)

    def _lighten(self, color: str) -> str:
        """Lighten a hex color."""
        if color == "#4a4a4a":
            return "#5a5a5a"
        elif color == "#ff9500":
            return "#ffaa33"
        elif color == "#d4d4d2":
            return "#e4e4e2"
        elif color == "#ff3b30":
            return "#ff5a50"
        return color

    def _darken(self, color: str) -> str:
        """Darken a hex color."""
        if color == "#4a4a4a":
            return "#3a3a3a"
        elif color == "#ff9500":
            return "#dd8000"
        elif color == "#d4d4d2":
            return "#c4c4c2"
        elif color == "#ff3b30":
            return "#dd2a20"
        return color


class CalculatorWindow(QMainWindow):
    """Main calculator window."""

    def __init__(self):
        super().__init__()
        self.history = CalculationHistory()
        self.current_input = ""
        self.last_result: Optional[float] = None
        self._setup_ui()
        self._setup_shortcuts()

    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Calculator")
        self.setMinimumSize(400, 500)
        self.setStyleSheet("background-color: #2d2d2d;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(10)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Segoe UI", 32))
        self.display.setMinimumHeight(80)
        self.display.setText("0")
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        calc_layout.addWidget(self.display)

        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_label.setFont(QFont("Segoe UI", 12))
        self.expression_label.setStyleSheet("color: #888; padding-right: 10px;")
        calc_layout.addWidget(self.expression_label)

        button_layout = QGridLayout()
        button_layout.setSpacing(8)

        buttons = [
            ("C", 0, 0, "#ff3b30"), ("√", 0, 1, "#ff9500"), ("%", 0, 2, "#ff9500"), ("/", 0, 3, "#ff9500"),
            ("7", 1, 0, "#4a4a4a"), ("8", 1, 1, "#4a4a4a"), ("9", 1, 2, "#4a4a4a"), ("*", 1, 3, "#ff9500"),
            ("4", 2, 0, "#4a4a4a"), ("5", 2, 1, "#4a4a4a"), ("6", 2, 2, "#4a4a4a"), ("-", 2, 3, "#ff9500"),
            ("1", 3, 0, "#4a4a4a"), ("2", 3, 1, "#4a4a4a"), ("3", 3, 2, "#4a4a4a"), ("+", 3, 3, "#ff9500"),
            ("0", 4, 0, "#4a4a4a"), (".", 4, 1, "#4a4a4a"), ("^", 4, 2, "#ff9500"), ("=", 4, 3, "#ff9500"),
        ]

        for text, row, col, color in buttons:
            btn = CalculatorButton(text, color)
            btn.clicked.connect(lambda checked, t=text: self._on_button_click(t))
            button_layout.addWidget(btn, row, col)

        calc_layout.addLayout(button_layout)
        main_layout.addLayout(calc_layout, stretch=2)

        history_layout = QVBoxLayout()
        history_label = QLabel("History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_label.setStyleSheet("color: white;")
        history_layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setFont(QFont("Segoe UI", 11))
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #4a4a4a;
            }
        """)
        self.history_list.itemDoubleClicked.connect(self._on_history_item_clicked)
        history_layout.addWidget(self.history_list)

        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.setFont(QFont("Segoe UI", 10))
        clear_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        clear_history_btn.clicked.connect(self._clear_history)
        history_layout.addWidget(clear_history_btn)

        main_layout.addLayout(history_layout, stretch=1)

    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        QShortcut(QKeySequence("Return"), self, self._calculate)
        QShortcut(QKeySequence("Enter"), self, self._calculate)
        QShortcut(QKeySequence("Escape"), self, self._clear)

    def _on_button_click(self, text: str):
        """Handle button clicks."""
        if text == "C":
            self._clear()
        elif text == "=":
            self._calculate()
        elif text == "√":
            self._calculate_sqrt()
        else:
            self._append_to_input(text)

    def _append_to_input(self, text: str):
        """Append text to the current input."""
        if self.current_input == "0" and text.isdigit():
            self.current_input = text
        else:
            self.current_input += text
        self._update_display()

    def _update_display(self):
        """Update the display with current input."""
        display_text = self.current_input if self.current_input else "0"
        self.display.setText(display_text)

    def _clear(self):
        """Clear the current input."""
        self.current_input = ""
        self.expression_label.setText("")
        self._update_display()

    def _calculate(self):
        """Evaluate the current expression."""
        if not self.current_input:
            return

        expr = self.current_input
        try:
            result = self._evaluate_expression(expr)
            self.expression_label.setText(f"{expr} =")
            self.display.setText(self._format_result(result))
            self.history.add(expr, result)
            self._update_history_list()
            self.current_input = str(result)
            self.last_result = result
        except ValueError as e:
            self.display.setText("Error")
            self.expression_label.setText(str(e))
            self.current_input = ""

    def _calculate_sqrt(self):
        """Calculate square root of current input."""
        if not self.current_input:
            return

        try:
            n = float(self.current_input)
            result = core.square_root(n)
            expr = f"√({self.current_input})"
            self.expression_label.setText(f"{expr} =")
            self.display.setText(self._format_result(result))
            self.history.add(expr, result)
            self._update_history_list()
            self.current_input = str(result)
            self.last_result = result
        except ValueError as e:
            self.display.setText("Error")
            self.expression_label.setText(str(e))
            self.current_input = ""

    def _evaluate_expression(self, expr: str) -> float:
        """Evaluate a simple binary expression."""
        operators = ["+", "-", "*", "/", "^", "%"]

        for op in operators:
            if op in expr:
                parts = expr.rsplit(op, 1)
                if len(parts) == 2 and parts[0] and parts[1]:
                    a = float(parts[0])
                    b = float(parts[1])

                    operations = {
                        "+": core.add,
                        "-": core.subtract,
                        "*": core.multiply,
                        "/": core.divide,
                        "^": core.power,
                        "%": core.modulo,
                    }
                    return operations[op](a, b)

        return float(expr)

    def _format_result(self, result: float) -> str:
        """Format a result for display."""
        if result == int(result):
            return str(int(result))
        return f"{result:.10g}"

    def _update_history_list(self):
        """Update the history list widget."""
        self.history_list.clear()
        for entry in self.history.get_all():
            self.history_list.addItem(str(entry))
        self.history_list.scrollToBottom()

    def _on_history_item_clicked(self, item):
        """Handle double-click on history item to reuse result."""
        text = item.text()
        if "=" in text:
            result = text.split("=")[-1].strip()
            self.current_input = result
            self._update_display()

    def _clear_history(self):
        """Clear the calculation history."""
        self.history.clear()
        self.history_list.clear()

    def keyPressEvent(self, event):
        """Handle keyboard input."""
        key = event.text()
        if key.isdigit() or key in "+-*/.^%":
            self._append_to_input(key)
        elif event.key() == Qt.Key.Key_Backspace:
            self.current_input = self.current_input[:-1]
            self._update_display()
        else:
            super().keyPressEvent(event)


def main():
    """Entry point for the calculator GUI."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
