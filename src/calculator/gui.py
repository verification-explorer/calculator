"""Graphical user interface for the calculator using PyQt6.

This module provides a GUI that uses the existing core and history modules,
demonstrating the separation of concerns in the calculator architecture.
"""

import math
import sys
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QPoint, QTimer, QSettings
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
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
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
        elif color == "#5856d6":
            return "#6866e6"
        elif color == "#3a3a3a":
            return "#4a4a4a"
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
        elif color == "#5856d6":
            return "#4846c6"
        elif color == "#3a3a3a":
            return "#2a2a2a"
        return color


class StandardModeWidget(QWidget):
    """Widget containing the standard calculator mode UI."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        """Set up the standard mode user interface."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(10)

        self.parent.display = QLineEdit()
        self.parent.display.setReadOnly(True)
        self.parent.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.parent.display.setFont(QFont("Segoe UI", 32))
        self.parent.display.setMinimumHeight(80)
        self.parent.display.setText("0")
        self.parent.display.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        calc_layout.addWidget(self.parent.display)

        self.parent.expression_label = QLabel("")
        self.parent.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.parent.expression_label.setFont(QFont("Segoe UI", 12))
        self.parent.expression_label.setStyleSheet("color: #888; padding-right: 10px;")
        calc_layout.addWidget(self.parent.expression_label)

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
            btn.clicked.connect(lambda checked, t=text: self.parent._on_button_click(t))
            button_layout.addWidget(btn, row, col)

        trig_grid = QGridLayout()
        trig_grid.setSpacing(8)

        self.parent.sin_btn = CalculatorButton("sin", "#5856d6")
        self.parent.sin_btn.clicked.connect(lambda: self.parent._calculate_trig("sin"))
        trig_grid.addWidget(self.parent.sin_btn, 0, 0)

        self.parent.cos_btn = CalculatorButton("cos", "#5856d6")
        self.parent.cos_btn.clicked.connect(lambda: self.parent._calculate_trig("cos"))
        trig_grid.addWidget(self.parent.cos_btn, 1, 0)

        self.parent.tan_btn = CalculatorButton("tan", "#5856d6")
        self.parent.tan_btn.clicked.connect(lambda: self.parent._calculate_trig("tan"))
        trig_grid.addWidget(self.parent.tan_btn, 2, 0)

        self.parent.inv_btn = CalculatorButton("inv", "#5856d6")
        self.parent.inv_btn.clicked.connect(self.parent._toggle_inverse)
        trig_grid.addWidget(self.parent.inv_btn, 3, 0)

        self.parent.rad_btn = CalculatorButton("rad", "#5856d6")
        self.parent.rad_btn.clicked.connect(self.parent._toggle_degrees)
        trig_grid.addWidget(self.parent.rad_btn, 4, 0)

        button_layout.addLayout(trig_grid, 0, 4, 5, 1)

        calc_layout.addLayout(button_layout)
        main_layout.addLayout(calc_layout, stretch=2)

        history_layout = QVBoxLayout()
        history_label = QLabel("History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_label.setStyleSheet("color: white;")
        history_layout.addWidget(history_label)

        self.parent.history_list = QListWidget()
        self.parent.history_list.setFont(QFont("Segoe UI", 11))
        self.parent.history_list.setStyleSheet("""
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
        self.parent.history_list.itemDoubleClicked.connect(self.parent._on_history_item_clicked)
        history_layout.addWidget(self.parent.history_list)

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
        clear_history_btn.clicked.connect(self.parent._clear_history)
        history_layout.addWidget(clear_history_btn)

        main_layout.addLayout(history_layout, stretch=1)


class ProgrammerModeWidget(QWidget):
    """Widget containing the programmer calculator mode UI."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # State variables (event handlers will use these)
        self.current_value = 0
        self.active_base = "HEX"
        self.integer_size = "DWord"
        self.carry_flag = False
        self.current_input = ""
        self.pending_operation = None
        self.pending_operand = None
        self.expression_tokens = []
        self.bit_boxes = []

        self._setup_ui()

    def _setup_ui(self):
        """Set up the programmer mode user interface."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Left side: Calculator panel
        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(10)

        # 1. Integer Size Selector
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        size_label.setStyleSheet("color: white; font-size: 12pt;")
        size_layout.addWidget(size_label)

        self.size_buttons = {}
        for size in ["Byte", "Word", "DWord", "QWord"]:
            btn = QPushButton(size)
            btn.setCheckable(True)
            btn.setChecked(size == "DWord")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3a3a3a;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:checked {
                    background-color: #ff9500;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QPushButton:checked:hover {
                    background-color: #ffaa33;
                }
            """)
            btn.clicked.connect(lambda checked, s=size: self._on_size_changed(s))
            self.size_buttons[size] = btn
            size_layout.addWidget(btn)

        size_layout.addStretch()
        calc_layout.addLayout(size_layout)

        # 2. Carry Flag + Bit Display Panel
        bit_panel_layout = QHBoxLayout()

        # Carry flag checkbox
        self.carry_checkbox = QPushButton("C")
        self.carry_checkbox.setCheckable(True)
        self.carry_checkbox.setFixedSize(40, 30)
        self.carry_checkbox.setToolTip("Carry Flag")
        self.carry_checkbox.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: 2px solid #4a4a4a;
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 10pt;
            }
            QPushButton:checked {
                background-color: #ff9500;
                border-color: #ff9500;
            }
        """)
        bit_panel_layout.addWidget(self.carry_checkbox)

        # Bit display scroll area
        bit_scroll = QScrollArea()
        bit_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        bit_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        bit_scroll.setMaximumHeight(50)
        bit_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)

        bit_container = QWidget()
        self.bit_layout = QHBoxLayout(bit_container)
        self.bit_layout.setSpacing(2)
        self.bit_layout.setContentsMargins(5, 5, 5, 5)

        # Create 32 bit boxes for DWord (will be recreated on size change)
        self._create_bit_boxes(32)

        bit_scroll.setWidget(bit_container)
        bit_panel_layout.addWidget(bit_scroll, stretch=1)

        calc_layout.addLayout(bit_panel_layout)

        # 3-6. Base Input Panels (HEX/DEC/OCT/BIN)
        self.base_buttons = {}
        self.base_inputs = {}

        for base in ["HEX", "DEC", "OCT", "BIN"]:
            base_panel = QHBoxLayout()

            # Base button
            base_btn = QPushButton(base)
            base_btn.setFixedWidth(60)
            base_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3a3a3a;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
            """)
            # Highlight active base
            if base == "HEX":
                base_btn.setStyleSheet(base_btn.styleSheet() + """
                    QPushButton {
                        background-color: #ff9500;
                    }
                """)
            base_btn.clicked.connect(lambda checked, b=base: self._on_base_selected(b))
            self.base_buttons[base] = base_btn
            base_panel.addWidget(base_btn)

            # Base input field
            base_input = QLineEdit()
            base_input.setAlignment(Qt.AlignmentFlag.AlignRight)
            base_input.setFont(QFont("Consolas", 14))
            base_input.setText("0x0" if base == "HEX" else "0")
            base_input.setStyleSheet("""
                QLineEdit {
                    background-color: #1c1c1c;
                    color: white;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    padding: 6px;
                }
            """)
            base_input.textChanged.connect(lambda text, b=base: self._on_base_input_changed(b, text))
            self.base_inputs[base] = base_input
            base_panel.addWidget(base_input, stretch=1)

            calc_layout.addLayout(base_panel)

        # 7. Bit Manipulation Panel
        bit_ops_layout = QHBoxLayout()

        self.bitwise_btn = QPushButton("Bitwise")
        self.bitwise_btn.setFixedHeight(40)
        self.bitwise_btn.setStyleSheet("""
            QPushButton {
                background-color: #5856d6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #6866e6;
            }
        """)
        self.bitwise_btn.clicked.connect(self._show_bitwise_overlay)
        bit_ops_layout.addWidget(self.bitwise_btn)

        self.bitshift_btn = QPushButton("Bitshift")
        self.bitshift_btn.setFixedHeight(40)
        self.bitshift_btn.setStyleSheet("""
            QPushButton {
                background-color: #5856d6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #6866e6;
            }
        """)
        self.bitshift_btn.clicked.connect(self._show_bitshift_overlay)
        bit_ops_layout.addWidget(self.bitshift_btn)

        calc_layout.addLayout(bit_ops_layout)

        # 8. Main Display Area
        self.programmer_display = QLineEdit()
        self.programmer_display.setReadOnly(True)
        self.programmer_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.programmer_display.setFont(QFont("Segoe UI", 32))
        self.programmer_display.setMinimumHeight(80)
        self.programmer_display.setText("0x0")
        self.programmer_display.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        calc_layout.addWidget(self.programmer_display)

        # 9. Expression Label (feedback)
        self.programmer_expression_label = QLabel("")
        self.programmer_expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.programmer_expression_label.setFont(QFont("Segoe UI", 12))
        self.programmer_expression_label.setStyleSheet("color: #888888;")
        calc_layout.addWidget(self.programmer_expression_label)

        # 10. Keyboard Panel (6x5 grid)
        button_layout = QGridLayout()
        button_layout.setSpacing(8)

        buttons = [
            # Row 1
            ("A", 0, 0, "#4a4a4a"), ("<<", 0, 1, "#ff9500"), (">>", 0, 2, "#ff9500"),
            ("CE", 0, 3, "#ff3b30"), ("⌫", 0, 4, "#ff3b30"),
            # Row 2
            ("B", 1, 0, "#4a4a4a"), ("(", 1, 1, "#4a4a4a"), (")", 1, 2, "#4a4a4a"),
            ("%", 1, 3, "#ff9500"), ("/", 1, 4, "#ff9500"),
            # Row 3
            ("C", 2, 0, "#4a4a4a"), ("7", 2, 1, "#4a4a4a"), ("8", 2, 2, "#4a4a4a"),
            ("9", 2, 3, "#4a4a4a"), ("*", 2, 4, "#ff9500"),
            # Row 4
            ("D", 3, 0, "#4a4a4a"), ("4", 3, 1, "#4a4a4a"), ("5", 3, 2, "#4a4a4a"),
            ("6", 3, 3, "#4a4a4a"), ("-", 3, 4, "#ff9500"),
            # Row 5
            ("E", 4, 0, "#4a4a4a"), ("1", 4, 1, "#4a4a4a"), ("2", 4, 2, "#4a4a4a"),
            ("3", 4, 3, "#4a4a4a"), ("+", 4, 4, "#ff9500"),
            # Row 6
            ("F", 5, 0, "#4a4a4a"), ("+/-", 5, 1, "#4a4a4a"), ("0", 5, 2, "#4a4a4a"),
            ("⇄", 5, 3, "#5856d6"), ("=", 5, 4, "#ff9500"),
        ]

        self.keyboard_buttons = {}
        for text, row, col, color in buttons:
            btn = CalculatorButton(text, color)
            btn.clicked.connect(lambda checked, t=text: self._on_programmer_button_click(t))
            self.keyboard_buttons[text] = btn
            button_layout.addWidget(btn, row, col)

        calc_layout.addLayout(button_layout)

        main_layout.addLayout(calc_layout, stretch=2)

        # Right side: History panel (reuse from parent)
        history_layout = QVBoxLayout()
        history_label = QLabel("History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_label.setStyleSheet("color: white;")
        history_layout.addWidget(history_label)

        # Use shared history list from parent
        # (parent will manage history display)
        history_layout.addWidget(self.parent.history_list)

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
        clear_history_btn.clicked.connect(self.parent._clear_history)
        history_layout.addWidget(clear_history_btn)

        main_layout.addLayout(history_layout, stretch=1)

    def _create_bit_boxes(self, num_bits: int):
        """Create bit display boxes for the current integer size."""
        # Clear existing boxes
        for box in self.bit_boxes:
            box.deleteLater()
        self.bit_boxes.clear()

        # Clear layout
        while self.bit_layout.count():
            item = self.bit_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create new boxes (MSB on left, LSB on right)
        for i in range(num_bits - 1, -1, -1):
            box = BitDisplayBox(i, self)
            box.bit_toggled.connect(self._on_bit_toggled)
            self.bit_boxes.append(box)
            self.bit_layout.addWidget(box)

            # Add spacing every 4 bits (nibble grouping)
            if i > 0 and i % 4 == 0:
                self.bit_layout.addSpacing(10)

        self.bit_layout.addStretch()

    # Event Handlers

    def _on_size_changed(self, size: str):
        """Handle integer size change."""
        from calculator import programmer

        # Update checked state
        for s, btn in self.size_buttons.items():
            btn.setChecked(s == size)

        self.integer_size = size

        # Recreate bit display
        bits = programmer.get_size_bits(size)
        self._create_bit_boxes(bits)

        # Apply mask to current value
        self.current_value = programmer.apply_size_mask(self.current_value, size)

        # Update all displays
        self._update_all_displays()

    def _on_base_selected(self, base: str):
        """Handle base mode selection."""
        self.active_base = base

        # Update button styling (highlight active)
        for b, btn in self.base_buttons.items():
            if b == base:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9500;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                        font-size: 11pt;
                    }
                    QPushButton:hover {
                        background-color: #ffaa33;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3a3a3a;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                        font-size: 11pt;
                    }
                    QPushButton:hover {
                        background-color: #4a4a4a;
                    }
                """)

        # Enable/disable keyboard buttons based on base
        self._update_keyboard_button_states()

    def _update_keyboard_button_states(self):
        """Enable/disable keyboard buttons based on active base."""
        # HEX: all enabled
        # DEC: A-F disabled
        # OCT: A-F, 8, 9 disabled
        # BIN: A-F, 2-9 disabled

        disabled_buttons = []
        if self.active_base == "DEC":
            disabled_buttons = ["A", "B", "C", "D", "E", "F"]
        elif self.active_base == "OCT":
            disabled_buttons = ["A", "B", "C", "D", "E", "F", "8", "9"]
        elif self.active_base == "BIN":
            disabled_buttons = ["A", "B", "C", "D", "E", "F", "2", "3", "4", "5", "6", "7", "8", "9"]

        for text, btn in self.keyboard_buttons.items():
            if text in disabled_buttons:
                btn.setEnabled(False)
                btn.setStyleSheet(btn.styleSheet() + """
                    QPushButton { opacity: 0.3; }
                    QPushButton:disabled { background-color: #2a2a2a; }
                """)
            else:
                btn.setEnabled(True)

    def _on_base_input_changed(self, base: str, text: str):
        """Handle manual input in base field."""
        from calculator import programmer

        try:
            # Parse the input
            value = programmer.parse_base_input(text, base)
            # Update canonical value
            self.current_value = programmer.apply_size_mask(value, self.integer_size)
            # Update all other displays
            self._update_all_displays(skip_base=base)
        except (ValueError, AttributeError):
            # Invalid input - ignore
            pass

    def _on_bit_toggled(self, position: int, new_value: bool):
        """Handle bit toggle in bit display."""
        from calculator import programmer

        # Update canonical value
        self.current_value = programmer.set_bit_at(
            self.current_value, position, new_value, self.integer_size
        )

        # Update all displays
        self._update_all_displays()

    def _on_programmer_button_click(self, text: str):
        """Handle keyboard button click."""
        if text == "CE":
            self._clear_entry()
        elif text == "⌫":
            self._backspace()
        elif text == "=":
            self._calculate()
        elif text == "+/-":
            self._toggle_sign()
        elif text == "⇄":
            self._swap_operands()
        elif text in ["<<", ">>"]:
            self.current_input += f" {text} "
            self._update_main_display()
        elif text in ["+", "-", "*", "/", "%", "(", ")"]:
            self.current_input += text
            self._update_main_display()
        else:
            # Digit or hex letter (A-F)
            self._append_digit(text)

    def _append_digit(self, digit: str):
        """Append a digit to current input."""
        self.current_input += digit
        self._update_main_display()

    def _clear_entry(self):
        """Clear current entry."""
        self.current_input = ""
        self.current_value = 0
        self._update_all_displays()

    def _backspace(self):
        """Delete last character."""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self._update_main_display()

    def _toggle_sign(self):
        """Toggle between positive and negative (two's complement)."""
        from calculator import programmer

        # Toggle sign by using two's complement
        if self.current_value == 0:
            return

        # Calculate two's complement
        max_val = programmer.get_size_mask(self.integer_size) + 1
        self.current_value = (max_val - self.current_value) & programmer.get_size_mask(self.integer_size)

        self._update_all_displays()

    def _swap_operands(self):
        """Swap operands in pending operation."""
        # This is a placeholder for more complex expression handling
        # For now, just show a message
        pass

    def _calculate(self):
        """Evaluate the current expression."""
        from calculator import programmer_parser

        if not self.current_input:
            return

        try:
            # Evaluate expression
            normalized, result, new_carry = programmer_parser.evaluate_programmer_expression(
                self.current_input, self.integer_size, self.carry_flag
            )

            # Update state
            self.current_value = result
            self.carry_flag = new_carry
            self.carry_checkbox.setChecked(new_carry)

            # Update displays
            self._update_all_displays()

            # Add to history
            result_str = programmer_parser.programmer.convert_to_base(result, self.active_base, self.integer_size)
            self.parent.history.add(self.current_input, result)
            self.parent._update_history_list()

            # Clear input for next operation
            self.current_input = ""
            self._update_main_display()

        except (ValueError, ZeroDivisionError) as e:
            # Show error
            self.programmer_display.setText(f"Error: {str(e)}")
            self.current_input = ""

    def _show_bitwise_overlay(self):
        """Show the bitwise operations overlay."""
        overlay = BitwiseOverlay(self)
        overlay.operation_selected.connect(self._on_bitwise_operation)

        # Position overlay above keyboard
        pos = self.bitwise_btn.mapToGlobal(self.bitwise_btn.rect().bottomLeft())
        overlay.move(pos)
        overlay.show()

    def _show_bitshift_overlay(self):
        """Show the bitshift operations overlay."""
        overlay = BitshiftOverlay(self)
        overlay.operation_selected.connect(self._on_bitshift_operation)

        # Position overlay above keyboard
        pos = self.bitshift_btn.mapToGlobal(self.bitshift_btn.rect().bottomLeft())
        overlay.move(pos)
        overlay.show()

    def _on_bitwise_operation(self, operation: str):
        """Handle bitwise operation selection."""
        op_map = {
            "AND": " AND ",
            "OR": " OR ",
            "XOR": " XOR ",
            "NOT": "NOT ",
            "NAND": " NAND ",
            "NOR": " NOR ",
        }

        if operation == "NOT":
            # NOT is unary - prepend
            self.current_input = "NOT " + self.current_input
        else:
            # Binary operation - append
            self.current_input += op_map.get(operation, f" {operation} ")

        self._update_main_display()

    def _on_bitshift_operation(self, operation: str):
        """Handle bitshift operation selection."""
        # For now, just add the shift operator
        # The shift amount will be entered after
        if operation == "arithmetic":
            self.current_input += " >> "  # Arithmetic right shift
        elif operation == "logical":
            self.current_input += " >> "  # Logical right shift (default)
        elif operation == "rotate":
            self.current_input += " << "  # Use left shift for rotate (will need special handling)
        elif operation == "rotate_carry":
            self.current_input += " << "  # Use left shift for rotate-carry

        self._update_main_display()

    def _update_all_displays(self, skip_base: str = None):
        """Update all base displays and bit display from canonical value."""
        from calculator import programmer

        # Update base input fields
        for base, input_field in self.base_inputs.items():
            if base != skip_base:
                formatted = programmer.convert_to_base(self.current_value, base, self.integer_size)
                input_field.blockSignals(True)  # Prevent recursive updates
                input_field.setText(formatted)
                input_field.blockSignals(False)

        # Update bit display
        bits = programmer.get_size_bits(self.integer_size)
        for i in range(bits):
            bit_value = programmer.get_bit_at(self.current_value, i)
            # Find the box (they're in reverse order: MSB first)
            box_index = bits - 1 - i
            if box_index < len(self.bit_boxes):
                self.bit_boxes[box_index].set_bit_value(bit_value, animate=False)

        # Update main display
        self._update_main_display()

    def _update_main_display(self):
        """Update the main display with current input or value."""
        from calculator import programmer

        if self.current_input:
            self.programmer_display.setText(self.current_input)
        else:
            # Show current value in active base
            formatted = programmer.convert_to_base(self.current_value, self.active_base, self.integer_size)
            self.programmer_display.setText(formatted)

    def set_initial_value(self, value: int):
        """Set initial value when switching from Standard mode."""
        from calculator import programmer

        self.current_value = programmer.apply_size_mask(value, self.integer_size)
        self.current_input = ""
        self._update_all_displays()


class ConverterModeWidget(QWidget):
    """Widget containing the unit converter mode UI."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # State variables
        self.current_category = "Length"
        self.from_unit = "meter"
        self.to_unit = "foot"
        self.focused_field = "from"
        self.last_edited_field = "from"

        # Track units per category for state persistence
        self._units_per_category: dict = {}

        # Widget references
        self.category_buttons: dict = {}
        self.quick_unit_buttons: list = []

        self._restore_state()
        self._setup_ui()

    def _setup_ui(self):
        """Set up the converter mode user interface."""
        from calculator import converter
        from PyQt6.QtWidgets import QComboBox, QFrame

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Left side: Converter panel
        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(10)

        # 1. Category Selector
        category_layout = QHBoxLayout()
        category_layout.setSpacing(4)

        for cat in converter.get_categories():
            short_name = cat[:4] if cat != "Temperature" else "Temp"
            btn = CalculatorButton(short_name, "#3a3a3a")
            btn.setMinimumSize(70, 40)
            btn.setFont(QFont("Segoe UI", 11))
            btn.clicked.connect(lambda checked, c=cat: self._on_category_changed(c))
            self.category_buttons[cat] = btn
            category_layout.addWidget(btn)

        category_layout.addStretch()
        calc_layout.addLayout(category_layout)

        # 2. FROM Panel
        from_panel = QVBoxLayout()
        from_label = QLabel("FROM")
        from_label.setStyleSheet("color: #888888; font-size: 12pt; font-weight: bold;")
        from_panel.addWidget(from_label)

        from_row = QHBoxLayout()
        self.from_dropdown = QComboBox()
        self.from_dropdown.setFixedWidth(150)
        self.from_dropdown.setFont(QFont("Segoe UI", 12))
        self._style_dropdown(self.from_dropdown)
        self.from_dropdown.currentIndexChanged.connect(self._on_from_unit_changed)
        from_row.addWidget(self.from_dropdown)

        self.from_input = QLineEdit()
        self.from_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.from_input.setFont(QFont("Segoe UI", 20))
        self.from_input.setMinimumHeight(50)
        self.from_input.setText("0")
        self._style_input(self.from_input)
        self.from_input.textChanged.connect(self._on_from_input_changed)
        self.from_input.focusInEvent = lambda e: self._on_focus_changed("from", e)
        from_row.addWidget(self.from_input)

        from_panel.addLayout(from_row)
        calc_layout.addLayout(from_panel)

        # 3. Swap Button
        swap_container = QHBoxLayout()
        swap_container.addStretch()
        swap_btn = CalculatorButton("Swap Units ⇄", "#5856d6")
        swap_btn.setMinimumSize(120, 40)
        swap_btn.setFont(QFont("Segoe UI", 11))
        swap_btn.clicked.connect(self._swap_units)
        swap_container.addWidget(swap_btn)
        swap_container.addStretch()
        calc_layout.addLayout(swap_container)

        # 4. TO Panel
        to_panel = QVBoxLayout()
        to_label = QLabel("TO")
        to_label.setStyleSheet("color: #888888; font-size: 12pt; font-weight: bold;")
        to_panel.addWidget(to_label)

        to_row = QHBoxLayout()
        self.to_dropdown = QComboBox()
        self.to_dropdown.setFixedWidth(150)
        self.to_dropdown.setFont(QFont("Segoe UI", 12))
        self._style_dropdown(self.to_dropdown)
        self.to_dropdown.currentIndexChanged.connect(self._on_to_unit_changed)
        to_row.addWidget(self.to_dropdown)

        self.to_input = QLineEdit()
        self.to_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.to_input.setFont(QFont("Segoe UI", 20))
        self.to_input.setMinimumHeight(50)
        self.to_input.setText("0")
        self._style_input(self.to_input)
        self.to_input.textChanged.connect(self._on_to_input_changed)
        self.to_input.focusInEvent = lambda e: self._on_focus_changed("to", e)
        to_row.addWidget(self.to_input)

        to_panel.addLayout(to_row)
        calc_layout.addLayout(to_panel)

        # 5. Quick Unit Buttons
        self.quick_units_layout = QHBoxLayout()
        self.quick_units_layout.setSpacing(4)
        self.quick_units_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        calc_layout.addLayout(self.quick_units_layout)

        # 6. Numeric Keypad
        keypad_layout = QGridLayout()
        keypad_layout.setSpacing(8)

        keypad_buttons = [
            ("7", 0, 0, "#4a4a4a"),
            ("8", 0, 1, "#4a4a4a"),
            ("9", 0, 2, "#4a4a4a"),
            ("C", 0, 3, "#ff3b30"),
            ("4", 1, 0, "#4a4a4a"),
            ("5", 1, 1, "#4a4a4a"),
            ("6", 1, 2, "#4a4a4a"),
            ("CE", 1, 3, "#ff3b30"),
            ("1", 2, 0, "#4a4a4a"),
            ("2", 2, 1, "#4a4a4a"),
            ("3", 2, 2, "#4a4a4a"),
            ("⌫", 2, 3, "#ff3b30"),
            ("+/−", 3, 0, "#4a4a4a"),
            ("0", 3, 1, "#4a4a4a"),
            (".", 3, 2, "#4a4a4a"),
            ("=", 3, 3, "#ff9500"),
        ]

        for text, row, col, color in keypad_buttons:
            btn = CalculatorButton(text, color)
            btn.clicked.connect(lambda checked, t=text: self._on_keypad_click(t))
            keypad_layout.addWidget(btn, row, col)

        calc_layout.addLayout(keypad_layout)
        calc_layout.addStretch()

        main_layout.addLayout(calc_layout, stretch=2)

        # Right side: History panel
        history_layout = QVBoxLayout()
        history_label = QLabel("History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_label.setStyleSheet("color: white;")
        history_layout.addWidget(history_label)

        history_layout.addWidget(self.parent.history_list)

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
        clear_history_btn.clicked.connect(self.parent._clear_history)
        history_layout.addWidget(clear_history_btn)

        main_layout.addLayout(history_layout, stretch=1)

        # Initialize UI state
        self._update_category_buttons()
        self._update_dropdowns()
        self._update_quick_unit_buttons()

    def _style_dropdown(self, dropdown):
        """Apply dark theme styling to a QComboBox."""
        dropdown.setStyleSheet("""
            QComboBox {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QComboBox:hover {
                background-color: #4a4a4a;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid white;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #ff9500;
                border: 1px solid #3a3a3a;
            }
        """)

    def _style_input(self, input_field):
        """Apply dark theme styling to a QLineEdit."""
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #ff9500;
            }
        """)

    def _on_category_changed(self, category: str):
        """Handle category selection."""
        from calculator import converter

        if category == self.current_category:
            return

        # Save current category's units before switching
        self._units_per_category[self.current_category] = (self.from_unit, self.to_unit)

        self.current_category = category

        # Restore saved units for the new category, or use defaults
        if category in self._units_per_category:
            self.from_unit, self.to_unit = self._units_per_category[category]
        else:
            self.from_unit, self.to_unit = converter.get_default_units(category)

        self.last_edited_field = "from"

        self._update_category_buttons()
        self._update_dropdowns()
        self._update_quick_unit_buttons()

        # Reset input values
        self.from_input.blockSignals(True)
        self.to_input.blockSignals(True)
        self.from_input.setText("0")
        self.to_input.setText("0")
        self.from_input.blockSignals(False)
        self.to_input.blockSignals(False)

        self._save_state()

    def _update_category_buttons(self):
        """Update category button styling."""
        for cat, btn in self.category_buttons.items():
            if cat == self.current_category:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9500;
                        color: white;
                        border: none;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #ffaa33;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3a3a3a;
                        color: white;
                        border: none;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #4a4a4a;
                    }
                """)

    def _update_dropdowns(self):
        """Update dropdown contents for current category."""
        from calculator import converter

        units = converter.get_units_for_category(self.current_category)

        self.from_dropdown.blockSignals(True)
        self.to_dropdown.blockSignals(True)

        self.from_dropdown.clear()
        self.to_dropdown.clear()

        for unit in units:
            abbrev = converter.get_unit_abbreviation(unit)
            display_text = f"{abbrev} - {unit}"
            self.from_dropdown.addItem(display_text, unit)
            self.to_dropdown.addItem(display_text, unit)

        # Set current selections
        from_idx = units.index(self.from_unit) if self.from_unit in units else 0
        to_idx = units.index(self.to_unit) if self.to_unit in units else 0
        self.from_dropdown.setCurrentIndex(from_idx)
        self.to_dropdown.setCurrentIndex(to_idx)

        self.from_dropdown.blockSignals(False)
        self.to_dropdown.blockSignals(False)

    def _update_quick_unit_buttons(self):
        """Update quick unit buttons for current category."""
        from calculator import converter

        # Clear existing buttons
        while self.quick_units_layout.count():
            item = self.quick_units_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.quick_unit_buttons.clear()

        quick_units = converter.get_quick_units(self.current_category)
        for abbrev in quick_units:
            btn = CalculatorButton(abbrev, "#4a4a4a")
            btn.setMinimumSize(50, 50)
            btn.setFont(QFont("Segoe UI", 12))
            btn.clicked.connect(lambda checked, a=abbrev: self._on_quick_unit_clicked(a))
            self.quick_unit_buttons.append(btn)
            self.quick_units_layout.addWidget(btn)

        self._update_quick_unit_highlights()

    def _update_quick_unit_highlights(self):
        """Highlight FROM and TO units in quick buttons."""
        from calculator import converter

        from_abbrev = converter.get_unit_abbreviation(self.from_unit)
        to_abbrev = converter.get_unit_abbreviation(self.to_unit)

        for btn in self.quick_unit_buttons:
            text = btn.text()
            if text == from_abbrev:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a4a4a;
                        color: white;
                        border: 2px solid #ff9500;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #5a5a5a;
                    }
                """)
            elif text == to_abbrev:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a4a4a;
                        color: white;
                        border: 2px solid #5856d6;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #5a5a5a;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4a4a4a;
                        color: white;
                        border: none;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #5a5a5a;
                    }
                """)

    def _on_quick_unit_clicked(self, abbrev: str):
        """Handle quick unit button click."""
        from calculator import converter
        from PyQt6.QtWidgets import QApplication

        try:
            unit = converter.get_unit_from_abbreviation(abbrev, self.current_category)
        except ValueError:
            return

        # Shift+click sets TO unit
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.ShiftModifier:
            self.to_unit = unit
            units = converter.get_units_for_category(self.current_category)
            idx = units.index(unit) if unit in units else 0
            self.to_dropdown.blockSignals(True)
            self.to_dropdown.setCurrentIndex(idx)
            self.to_dropdown.blockSignals(False)
        else:
            self.from_unit = unit
            units = converter.get_units_for_category(self.current_category)
            idx = units.index(unit) if unit in units else 0
            self.from_dropdown.blockSignals(True)
            self.from_dropdown.setCurrentIndex(idx)
            self.from_dropdown.blockSignals(False)

        self._update_quick_unit_highlights()
        self._perform_conversion(self.last_edited_field)

    def _on_from_unit_changed(self, index: int):
        """Handle FROM unit dropdown change."""
        unit = self.from_dropdown.currentData()
        if unit:
            self.from_unit = unit
            self._update_quick_unit_highlights()
            self._perform_conversion(self.last_edited_field)
            self._save_state()

    def _on_to_unit_changed(self, index: int):
        """Handle TO unit dropdown change."""
        unit = self.to_dropdown.currentData()
        if unit:
            self.to_unit = unit
            self._update_quick_unit_highlights()
            self._perform_conversion(self.last_edited_field)
            self._save_state()

    def _on_focus_changed(self, field: str, event):
        """Handle focus change between input fields."""
        self.focused_field = field
        QLineEdit.focusInEvent(
            self.from_input if field == "from" else self.to_input, event
        )

    def _on_from_input_changed(self, text: str):
        """Handle FROM input text change."""
        self.last_edited_field = "from"
        self._perform_conversion("from")

    def _on_to_input_changed(self, text: str):
        """Handle TO input text change."""
        self.last_edited_field = "to"
        self._perform_conversion("to")

    def _perform_conversion(self, source: str):
        """Perform conversion and update the other field."""
        from calculator import converter

        # Same-unit conversion: show "1" in both fields
        if self.from_unit == self.to_unit:
            self.from_input.blockSignals(True)
            self.to_input.blockSignals(True)
            self.from_input.setText("1")
            self.to_input.setText("1")
            self.from_input.blockSignals(False)
            self.to_input.blockSignals(False)
            return

        try:
            if source == "from":
                raw = self.from_input.text().replace(",", "")
                value = float(raw) if raw and raw != "-" else 0.0
                result = converter.convert(
                    value, self.from_unit, self.to_unit, self.current_category
                )
                self.to_input.blockSignals(True)
                self.to_input.setText(converter.format_result(result))
                self.to_input.blockSignals(False)
            else:
                raw = self.to_input.text().replace(",", "")
                value = float(raw) if raw and raw != "-" else 0.0
                result = converter.convert(
                    value, self.to_unit, self.from_unit, self.current_category
                )
                self.from_input.blockSignals(True)
                self.from_input.setText(converter.format_result(result))
                self.from_input.blockSignals(False)
        except (ValueError, ZeroDivisionError):
            pass

    def _swap_units(self):
        """Swap FROM and TO units and values."""
        from calculator import converter

        # Swap units
        self.from_unit, self.to_unit = self.to_unit, self.from_unit

        # Swap values
        from_text = self.from_input.text()
        to_text = self.to_input.text()

        self.from_input.blockSignals(True)
        self.to_input.blockSignals(True)
        self.from_input.setText(to_text)
        self.to_input.setText(from_text)
        self.from_input.blockSignals(False)
        self.to_input.blockSignals(False)

        # Update dropdowns
        units = converter.get_units_for_category(self.current_category)
        from_idx = units.index(self.from_unit) if self.from_unit in units else 0
        to_idx = units.index(self.to_unit) if self.to_unit in units else 0

        self.from_dropdown.blockSignals(True)
        self.to_dropdown.blockSignals(True)
        self.from_dropdown.setCurrentIndex(from_idx)
        self.to_dropdown.setCurrentIndex(to_idx)
        self.from_dropdown.blockSignals(False)
        self.to_dropdown.blockSignals(False)

        self._update_quick_unit_highlights()

    def _on_keypad_click(self, key: str):
        """Handle keypad button click."""
        if key == "C":
            self._clear_all()
        elif key == "CE":
            self._clear_entry()
        elif key == "⌫":
            self._backspace()
        elif key == "+/−":
            self._toggle_sign()
        elif key == "=":
            self._record_to_history()
        else:
            self._append_digit(key)

    def _append_digit(self, digit: str):
        """Append a digit or decimal point to the focused field."""
        input_field = self.from_input if self.focused_field == "from" else self.to_input

        current = input_field.text().replace(",", "")

        # Handle decimal point
        if digit == ".":
            if "." in current:
                return
            if not current or current == "-":
                digit = "0."

        # Replace leading zero (unless adding decimal)
        if current == "0" and digit != ".":
            current = ""

        input_field.setText(current + digit)

    def _clear_all(self):
        """Clear both input fields."""
        self.from_input.blockSignals(True)
        self.to_input.blockSignals(True)
        self.from_input.setText("0")
        self.to_input.setText("0")
        self.from_input.blockSignals(False)
        self.to_input.blockSignals(False)
        self.last_edited_field = "from"

    def _clear_entry(self):
        """Clear the focused input field."""
        input_field = self.from_input if self.focused_field == "from" else self.to_input
        input_field.setText("0")

    def _backspace(self):
        """Delete the last character from the focused field."""
        input_field = self.from_input if self.focused_field == "from" else self.to_input
        current = input_field.text().replace(",", "")

        if len(current) <= 1 or (len(current) == 2 and current.startswith("-")):
            input_field.setText("0")
        else:
            input_field.setText(current[:-1])

    def _toggle_sign(self):
        """Toggle the sign of the focused field."""
        input_field = self.from_input if self.focused_field == "from" else self.to_input
        current = input_field.text().replace(",", "")

        if current.startswith("-"):
            input_field.setText(current[1:])
        elif current != "0":
            input_field.setText("-" + current)

    def _record_to_history(self):
        """Record the current conversion to history."""
        from calculator import converter

        try:
            from_text = self.from_input.text().replace(",", "")
            from_value = float(from_text) if from_text and from_text != "-" else 0.0
            to_text = self.to_input.text().replace(",", "")
            to_value = float(to_text) if to_text and to_text != "-" else 0.0

            # Format the from value for display
            from_display = converter.format_result(from_value)

            self.parent.history.add_converter(
                from_value=from_display,
                to_value=to_value,
                category=self.current_category,
                from_unit=self.from_unit,
                to_unit=self.to_unit,
            )
            self.parent._update_history_list()
        except ValueError:
            pass

    def _save_state(self):
        """Save converter state to QSettings for persistence."""
        settings = QSettings("Calculator", "ConverterMode")
        settings.setValue("category", self.current_category)

        # Save current units to the per-category dict
        self._units_per_category[self.current_category] = (self.from_unit, self.to_unit)

        # Save all category units
        for cat, (from_u, to_u) in self._units_per_category.items():
            settings.setValue(f"units/{cat}/from", from_u)
            settings.setValue(f"units/{cat}/to", to_u)

    def _restore_state(self):
        """Restore converter state from QSettings."""
        from calculator import converter

        settings = QSettings("Calculator", "ConverterMode")

        # Restore category
        saved_category = settings.value("category", "Length")
        if saved_category in converter.get_categories():
            self.current_category = saved_category

        # Restore units per category
        for cat in converter.get_categories():
            default_from, default_to = converter.get_default_units(cat)
            from_u = settings.value(f"units/{cat}/from", default_from)
            to_u = settings.value(f"units/{cat}/to", default_to)

            # Validate units exist for this category
            valid_units = converter.get_units_for_category(cat)
            if from_u not in valid_units:
                from_u = default_from
            if to_u not in valid_units:
                to_u = default_to

            self._units_per_category[cat] = (from_u, to_u)

        # Set current units from restored category
        if self.current_category in self._units_per_category:
            self.from_unit, self.to_unit = self._units_per_category[self.current_category]

    def set_initial_state(self):
        """Reset to initial state when switching to this mode."""
        self.focused_field = "from"
        self.last_edited_field = "from"

        self._update_category_buttons()
        self._update_dropdowns()
        self._update_quick_unit_buttons()

        self.from_input.blockSignals(True)
        self.to_input.blockSignals(True)
        self.from_input.setText("0")
        self.to_input.setText("0")
        self.from_input.blockSignals(False)
        self.to_input.blockSignals(False)


class ModeToolbar(QWidget):
    """Toolbar with hamburger menu for mode switching."""

    hamburger_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_open = False
        self._setup_ui()

    def _setup_ui(self):
        """Set up the toolbar UI."""
        self.setFixedHeight(50)
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1c1c;
                border-bottom: 1px solid #3a3a3a;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.hamburger_btn = QPushButton("☰")
        self.hamburger_btn.setFixedSize(50, 50)
        self.hamburger_btn.setFont(QFont("Segoe UI", 24))
        self.hamburger_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
        """)
        self.hamburger_btn.clicked.connect(self.hamburger_clicked.emit)
        layout.addWidget(self.hamburger_btn)

        layout.addStretch()

    def set_open_state(self, is_open: bool):
        """Update hamburger button appearance based on open state."""
        self.is_open = is_open
        self.hamburger_btn.setText("×" if is_open else "☰")


class SidebarOverlay(QWidget):
    """Semi-transparent overlay that appears when sidebar is open."""

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.3);")
        self.hide()

    def mousePressEvent(self, event):
        """Emit clicked signal when overlay is clicked."""
        self.clicked.emit()
        super().mousePressEvent(event)


class ModeSidebar(QWidget):
    """Sidebar for selecting calculator mode."""

    mode_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = "standard"
        self._setup_ui()

    def _setup_ui(self):
        """Set up the sidebar UI."""
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #1c1c1c;
                border-right: 1px solid #3a3a3a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Calculator Mode")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("""
            QLabel {
                color: white;
                padding: 20px 15px 10px 15px;
                border: none;
            }
        """)
        layout.addWidget(title)

        self.standard_btn = QPushButton("Standard")
        self.standard_btn.setFont(QFont("Segoe UI", 14))
        self.standard_btn.clicked.connect(lambda: self.mode_selected.emit("standard"))
        layout.addWidget(self.standard_btn)

        self.programmer_btn = QPushButton("Programmer")
        self.programmer_btn.setFont(QFont("Segoe UI", 14))
        self.programmer_btn.clicked.connect(lambda: self.mode_selected.emit("programmer"))
        layout.addWidget(self.programmer_btn)

        self.converter_btn = QPushButton("Unit Converter")
        self.converter_btn.setFont(QFont("Segoe UI", 14))
        self.converter_btn.clicked.connect(lambda: self.mode_selected.emit("converter"))
        layout.addWidget(self.converter_btn)

        layout.addStretch()

        self.set_active_mode("standard")
        self.hide()

    def set_active_mode(self, mode: str):
        """Update button styling to highlight the active mode."""
        self.current_mode = mode

        normal_style = """
            QPushButton {
                background-color: transparent;
                color: #ccc;
                padding: 15px 20px;
                text-align: left;
                border: none;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """

        active_style = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                padding: 15px 20px;
                text-align: left;
                border: none;
                border-left: 3px solid #ff9500;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """

        self.standard_btn.setStyleSheet(active_style if mode == "standard" else normal_style)
        self.programmer_btn.setStyleSheet(active_style if mode == "programmer" else normal_style)
        self.converter_btn.setStyleSheet(active_style if mode == "converter" else normal_style)


class CalculatorWindow(QMainWindow):
    """Main calculator window."""

    def __init__(self):
        super().__init__()
        self.history = CalculationHistory()
        self.current_input = ""
        self.last_result: Optional[float] = None
        self.inverse_mode = False
        self.degrees_mode = False
        self.current_mode = "standard"
        self.sidebar_visible = False
        self._setup_ui()
        self._setup_shortcuts()

    def _setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Calculator")
        self.setMinimumSize(400, 500)
        self.setStyleSheet("background-color: #2d2d2d;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add toolbar
        self.toolbar = ModeToolbar()
        self.toolbar.hamburger_clicked.connect(self._toggle_sidebar)
        main_layout.addWidget(self.toolbar)

        # Add mode container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)

        self.mode_stack = QStackedWidget()
        self.standard_widget = StandardModeWidget(self)
        self.programmer_widget = ProgrammerModeWidget(self)
        self.converter_widget = ConverterModeWidget(self)
        self.mode_stack.addWidget(self.standard_widget)      # index 0
        self.mode_stack.addWidget(self.programmer_widget)    # index 1
        self.mode_stack.addWidget(self.converter_widget)     # index 2
        container_layout.addWidget(self.mode_stack)

        main_layout.addWidget(container)

        # Add overlay (initially hidden, positioned absolutely)
        self.overlay = SidebarOverlay(central_widget)
        self.overlay.clicked.connect(self._toggle_sidebar)
        self.overlay.setGeometry(0, 50, self.width(), self.height() - 50)

        # Add sidebar (initially hidden, positioned absolutely)
        self.sidebar = ModeSidebar(central_widget)
        self.sidebar.mode_selected.connect(self._on_mode_selected)
        self.sidebar.setGeometry(-200, 50, 200, self.height() - 50)

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

    def _calculate_trig(self, func: str):
        """Calculate trigonometric function of current input."""
        if not self.current_input:
            return

        try:
            n = float(self.current_input)
            if self.inverse_mode:
                func_name = f"a{func}"
                trig_funcs = {"asin": core.asin, "acos": core.acos, "atan": core.atan}
                result = trig_funcs[func_name](n)
                if self.degrees_mode:
                    result = math.degrees(result)
            else:
                func_name = func
                trig_funcs = {"sin": core.sin, "cos": core.cos, "tan": core.tan}
                if self.degrees_mode:
                    n = math.radians(n)
                result = trig_funcs[func_name](n)

            unit = "°" if self.degrees_mode else ""
            expr = f"{func_name}({self.current_input}{unit})"
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

    def _toggle_inverse(self):
        """Toggle inverse mode for trig functions."""
        self.inverse_mode = not self.inverse_mode
        if self.inverse_mode:
            self.sin_btn.setText("asin")
            self.cos_btn.setText("acos")
            self.tan_btn.setText("atan")
            self.inv_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7876f6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #8886ff;
                }
                QPushButton:pressed {
                    background-color: #6866e6;
                }
            """)
        else:
            self.sin_btn.setText("sin")
            self.cos_btn.setText("cos")
            self.tan_btn.setText("tan")
            self.inv_btn.setStyleSheet("""
                QPushButton {
                    background-color: #5856d6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #6866e6;
                }
                QPushButton:pressed {
                    background-color: #4846c6;
                }
            """)

    def _toggle_degrees(self):
        """Toggle between radians and degrees mode."""
        self.degrees_mode = not self.degrees_mode
        if self.degrees_mode:
            self.rad_btn.setText("deg")
            self.rad_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7876f6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #8886ff;
                }
                QPushButton:pressed {
                    background-color: #6866e6;
                }
            """)
        else:
            self.rad_btn.setText("rad")
            self.rad_btn.setStyleSheet("""
                QPushButton {
                    background-color: #5856d6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #6866e6;
                }
                QPushButton:pressed {
                    background-color: #4846c6;
                }
            """)

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
        import re

        text = item.text()

        # Check if this is a converter history entry: "100 m = 328.084 ft [Length]"
        converter_match = re.match(
            r"^([\d,.\-]+)\s+(\S+)\s+=\s+[\d,.\-e+]+\s+(\S+)\s+\[(\w+)\]$",
            text.strip(),
        )
        if converter_match and self.current_mode == "converter":
            from calculator import converter

            from_value = converter_match.group(1).replace(",", "")
            from_abbr = converter_match.group(2)
            to_abbr = converter_match.group(3)
            category = converter_match.group(4)

            converter_widget = self.mode_stack.widget(2)

            # Switch to the category if different
            if category != converter_widget.current_category:
                converter_widget._on_category_changed(category)

            # Find and set units by abbreviation
            units = converter.get_units_for_category(category)
            from_unit = next(
                (u for u in units if converter.get_unit_abbreviation(u) == from_abbr),
                None,
            )
            to_unit = next(
                (u for u in units if converter.get_unit_abbreviation(u) == to_abbr),
                None,
            )

            if from_unit and to_unit:
                converter_widget.from_unit = from_unit
                converter_widget.to_unit = to_unit
                converter_widget._update_dropdowns()
                converter_widget._update_quick_unit_highlights()

            # Populate FROM field with the original value
            converter_widget.from_input.blockSignals(True)
            converter_widget.from_input.setText(from_value)
            converter_widget.from_input.blockSignals(False)
            converter_widget.last_edited_field = "from"
            converter_widget._perform_conversion("from")
            return

        # Standard/programmer mode: extract result after "="
        if "=" in text:
            result = text.split("=")[-1].strip()
            # Remove any trailing metadata like "[HEX, DWord]"
            if "[" in result:
                result = result.split("[")[0].strip()
            self.current_input = result
            self._update_display()

    def _clear_history(self):
        """Clear the calculation history."""
        self.history.clear()
        self.history_list.clear()

    def _switch_mode(self, mode: str):
        """Switch between calculator modes."""
        if mode == self.current_mode:
            return

        # Preserve current numeric value if switching modes
        current_value = 0
        if self.current_mode == "standard" and self.last_result is not None:
            current_value = int(self.last_result)
        elif self.current_mode == "programmer":
            programmer_widget = self.mode_stack.widget(1)
            current_value = programmer_widget.current_value

        self.current_mode = mode
        self.history.clear()
        self.current_input = ""
        self.last_result = None

        if mode == "standard":
            self.mode_stack.setCurrentIndex(0)
            self.history_list.clear()
            self.display.setText(str(current_value) if current_value != 0 else "0")
            self.expression_label.setText("")
        elif mode == "programmer":
            self.mode_stack.setCurrentIndex(1)
            self.history_list.clear()
            # Set initial value in programmer mode
            programmer_widget = self.mode_stack.widget(1)
            programmer_widget.set_initial_value(current_value)
        elif mode == "converter":
            self.mode_stack.setCurrentIndex(2)
            self.history_list.clear()
            self.converter_widget.set_initial_state()

    def _toggle_sidebar(self):
        """Toggle sidebar visibility with animation."""
        self.sidebar_visible = not self.sidebar_visible
        self.toolbar.set_open_state(self.sidebar_visible)

        # Create animation for sidebar
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"pos")
        self.sidebar_animation.setDuration(200)

        if self.sidebar_visible:
            # Show sidebar and overlay
            self.overlay.show()
            self.sidebar.show()
            self.sidebar_animation.setStartValue(QPoint(-200, 50))
            self.sidebar_animation.setEndValue(QPoint(0, 50))
        else:
            # Hide sidebar and overlay
            self.sidebar_animation.setStartValue(QPoint(0, 50))
            self.sidebar_animation.setEndValue(QPoint(-200, 50))
            self.sidebar_animation.finished.connect(self._on_sidebar_close_finished)

        self.sidebar_animation.start()

    def _on_sidebar_close_finished(self):
        """Called when sidebar close animation finishes."""
        if not self.sidebar_visible:
            self.sidebar.hide()
            self.overlay.hide()

    def _on_mode_selected(self, mode: str):
        """Handle mode selection from sidebar."""
        self._switch_mode(mode)
        self.sidebar.set_active_mode(mode)
        if self.sidebar_visible:
            self._toggle_sidebar()

    def resizeEvent(self, event):
        """Handle window resize to reposition overlay and sidebar."""
        super().resizeEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(0, 50, self.width(), self.height() - 50)
        if hasattr(self, 'sidebar'):
            x = 0 if self.sidebar_visible else -200
            self.sidebar.setGeometry(x, 50, 200, self.height() - 50)

    def keyPressEvent(self, event):
        """Handle keyboard input."""
        # Close sidebar on Escape if open
        if event.key() == Qt.Key.Key_Escape and self.sidebar_visible:
            self._toggle_sidebar()
            return

        # Handle converter mode keyboard shortcuts
        if self.current_mode == "converter":
            converter_widget = self.mode_stack.widget(2)

            # F6-F13 for category switching
            category_keys = {
                Qt.Key.Key_F6: "Length",
                Qt.Key.Key_F7: "Weight",
                Qt.Key.Key_F8: "Temperature",
                Qt.Key.Key_F9: "Volume",
                Qt.Key.Key_F10: "Area",
                Qt.Key.Key_F11: "Speed",
                Qt.Key.Key_F12: "Time",
                Qt.Key.Key_F13: "Data",
            }
            if event.key() in category_keys:
                converter_widget._on_category_changed(category_keys[event.key()])
                return

            # Ctrl+Shift+S for swap
            if (
                event.key() == Qt.Key.Key_S
                and event.modifiers()
                == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier)
            ):
                converter_widget._swap_units()
                return

            # Numeric input
            key = event.text()
            if key.isdigit() or key == ".":
                converter_widget._append_digit(key)
                return

            if event.key() == Qt.Key.Key_Backspace:
                converter_widget._backspace()
                return
            elif event.key() == Qt.Key.Key_Delete:
                converter_widget._clear_entry()
                return
            elif event.key() == Qt.Key.Key_Escape:
                converter_widget._clear_all()
                return
            elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Equal):
                converter_widget._record_to_history()
                return

        # Handle programmer mode keyboard shortcuts
        if self.current_mode == "programmer":
            programmer_widget = self.mode_stack.widget(1)

            # F2-F5: Base switching
            if event.key() == Qt.Key.Key_F2:
                programmer_widget._on_base_selected("HEX")
                return
            elif event.key() == Qt.Key.Key_F3:
                programmer_widget._on_base_selected("DEC")
                return
            elif event.key() == Qt.Key.Key_F4:
                programmer_widget._on_base_selected("OCT")
                return
            elif event.key() == Qt.Key.Key_F5:
                programmer_widget._on_base_selected("BIN")
                return

            # Regular key handling for programmer mode
            key = event.text().upper()
            if key in "0123456789ABCDEF":
                programmer_widget._append_digit(key)
                return
            elif key in "+-*/%()":
                programmer_widget.current_input += key
                programmer_widget._update_main_display()
                return
            elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Equal:
                programmer_widget._calculate()
                return
            elif event.key() == Qt.Key.Key_Backspace:
                programmer_widget._backspace()
                return
            elif event.key() == Qt.Key.Key_Escape:
                programmer_widget._clear_entry()
                return

        # Standard mode keyboard handling
        key = event.text()
        if key.isdigit() or key in "+-*/.^%":
            self._append_to_input(key)
        elif event.key() == Qt.Key.Key_Backspace:
            self.current_input = self.current_input[:-1]
            self._update_display()
        else:
            super().keyPressEvent(event)


class BitDisplayBox(QPushButton):
    """Single bit display box (LED-style) for programmer mode."""

    bit_toggled = pyqtSignal(int, bool)  # (position, new_value)

    def __init__(self, position: int, parent=None):
        super().__init__(parent)
        self.position = position
        self.bit_value = False
        self.setFixedSize(30, 30)
        self.setCheckable(True)
        self.clicked.connect(self._on_clicked)
        self._update_style()

    def set_bit_value(self, value: bool, animate: bool = False):
        """Set the bit value and optionally animate the change."""
        self.bit_value = value
        self.setChecked(value)
        self._update_style()

        if animate:
            # Flash orange for 300ms
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ff9500;
                    border: 2px solid #ff9500;
                    border-radius: 4px;
                    color: white;
                    font-family: 'Consolas', monospace;
                    font-size: 10pt;
                }
            """)
            QTimer.singleShot(300, self._update_style)

    def _update_style(self):
        """Update button style based on bit value."""
        if self.bit_value:
            # Active bit (1) - filled orange
            style = """
                QPushButton {
                    background-color: #ff9500;
                    border: 2px solid #ff9500;
                    border-radius: 4px;
                    color: white;
                    font-family: 'Consolas', monospace;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #ffaa33;
                    border-color: #ffaa33;
                }
            """
        else:
            # Inactive bit (0) - outline only
            style = """
                QPushButton {
                    background-color: transparent;
                    border: 2px solid #4a4a4a;
                    border-radius: 4px;
                    color: #4a4a4a;
                    font-family: 'Consolas', monospace;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    border-color: #5a5a5a;
                    color: #5a5a5a;
                }
            """
        self.setStyleSheet(style)
        self.setText("1" if self.bit_value else "0")

    def _on_clicked(self):
        """Handle click - toggle bit value."""
        self.bit_value = not self.bit_value
        self._update_style()
        self.bit_toggled.emit(self.position, self.bit_value)


class BitwiseOverlay(QWidget):
    """Floating overlay panel for bitwise operations."""

    operation_selected = pyqtSignal(str)  # Operation name

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Popup)
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border: 1px solid #4a4a4a;
                border-radius: 8px;
            }
        """)
        layout = QGridLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        # 2x3 grid of bitwise operations
        operations = [
            ("AND", 0, 0), ("OR", 0, 1), ("NOT", 0, 2),
            ("NAND", 1, 0), ("NOR", 1, 1), ("XOR", 1, 2),
        ]

        for op_name, row, col in operations:
            btn = CalculatorButton(op_name, "#5856d6")
            btn.clicked.connect(lambda checked, op=op_name: self._select_operation(op))
            layout.addWidget(btn, row, col)

    def _select_operation(self, operation: str):
        """Emit operation and close overlay."""
        self.operation_selected.emit(operation)
        self.close()


class BitshiftOverlay(QWidget):
    """Floating overlay panel for bitshift operations."""

    operation_selected = pyqtSignal(str)  # Operation type

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Popup)
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border: 1px solid #4a4a4a;
                border-radius: 8px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        # 4 shift operations
        operations = [
            ("Arithmetic shift", "arithmetic"),
            ("Logical shift", "logical"),
            ("Rotate circular shift", "rotate"),
            ("Rotate through carry", "rotate_carry"),
        ]

        for label, op_type in operations:
            btn = QPushButton(label)
            btn.setFont(QFont("Segoe UI", 14))
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #5856d6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #6866e6;
                }
            """)
            btn.clicked.connect(lambda checked, op=op_type: self._select_operation(op))
            layout.addWidget(btn)

    def _select_operation(self, operation: str):
        """Emit operation and close overlay."""
        self.operation_selected.emit(operation)
        self.close()


def main():
    """Entry point for the calculator GUI."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
