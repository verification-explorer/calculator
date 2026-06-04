"""Tests for converter mode GUI integration."""

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QApplication

from calculator.gui import CalculatorWindow


@pytest.fixture
def window(qtbot):
    """Create a CalculatorWindow instance for testing."""
    win = CalculatorWindow()
    qtbot.addWidget(win)
    return win


@pytest.fixture
def converter_widget(window):
    """Switch to converter mode and return the converter widget."""
    window._switch_mode("converter")
    return window.mode_stack.widget(2)


class TestConverterModeSwitch:
    """Tests for switching to/from converter mode."""

    def test_switch_to_converter_mode(self, window):
        """Test switching to converter mode."""
        window._switch_mode("converter")
        assert window.current_mode == "converter"
        assert window.mode_stack.currentIndex() == 2

    def test_switch_clears_history_list(self, window, qtbot):
        """Test that switching modes clears the history list."""
        window._on_button_click("5")
        window._on_button_click("+")
        window._on_button_click("3")
        window._on_button_click("=")
        assert window.history_list.count() > 0

        window._switch_mode("converter")
        assert window.history_list.count() == 0


class TestCategorySwitching:
    """Tests for category switching behavior."""

    def test_category_switch_updates_state(self, converter_widget):
        """Test that category switch updates current_category."""
        converter_widget._on_category_changed("Temperature")
        assert converter_widget.current_category == "Temperature"

    def test_category_switch_clears_inputs(self, converter_widget):
        """Test that category switch resets input fields to 0."""
        converter_widget.from_input.setText("100")
        converter_widget.to_input.setText("328")

        converter_widget._on_category_changed("Weight")

        assert converter_widget.from_input.text() == "0"
        assert converter_widget.to_input.text() == "0"

    def test_category_switch_remembers_units(self, converter_widget):
        """Test that switching back to a category restores previous units."""
        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "kilometer"
        converter_widget.to_unit = "mile"
        converter_widget._units_per_category["Length"] = ("kilometer", "mile")

        converter_widget._on_category_changed("Weight")
        converter_widget._on_category_changed("Length")

        assert converter_widget.from_unit == "kilometer"
        assert converter_widget.to_unit == "mile"


class TestSameUnitConversion:
    """Tests for same-unit conversion behavior."""

    def test_same_unit_shows_one_in_both_fields(self, converter_widget):
        """Test that selecting same FROM and TO unit shows 1 in both."""
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "meter"
        converter_widget.from_input.setText("123")

        converter_widget._perform_conversion("from")

        assert converter_widget.from_input.text() == "1"
        assert converter_widget.to_input.text() == "1"


class TestSwapButton:
    """Tests for swap button behavior."""

    def test_swap_exchanges_units(self, converter_widget):
        """Test that swap exchanges FROM and TO units."""
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"

        converter_widget._swap_units()

        assert converter_widget.from_unit == "foot"
        assert converter_widget.to_unit == "meter"

    def test_swap_exchanges_values(self, converter_widget):
        """Test that swap exchanges FROM and TO values."""
        converter_widget.from_input.blockSignals(True)
        converter_widget.to_input.blockSignals(True)
        converter_widget.from_input.setText("100")
        converter_widget.to_input.setText("328.084")
        converter_widget.from_input.blockSignals(False)
        converter_widget.to_input.blockSignals(False)

        converter_widget._swap_units()

        assert converter_widget.from_input.text() == "328.084"
        assert converter_widget.to_input.text() == "100"


class TestQuickUnitButtons:
    """Tests for quick unit button behavior."""

    def test_quick_unit_sets_from_unit(self, converter_widget, qtbot):
        """Test that clicking quick unit sets FROM unit."""
        converter_widget._on_category_changed("Length")
        converter_widget._on_quick_unit_clicked("km")

        assert converter_widget.from_unit == "kilometer"

    def test_quick_unit_shift_click_sets_to_unit(self, converter_widget, qtbot, monkeypatch):
        """Test that Shift+click on quick unit sets TO unit."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import QApplication

        converter_widget._on_category_changed("Length")

        monkeypatch.setattr(
            QApplication, "keyboardModifiers", staticmethod(lambda: Qt.KeyboardModifier.ShiftModifier)
        )

        converter_widget._on_quick_unit_clicked("km")

        assert converter_widget.to_unit == "kilometer"


class TestBidirectionalEditing:
    """Tests for bidirectional input field editing."""

    def test_editing_from_updates_to(self, converter_widget):
        """Test that editing FROM field updates TO field."""
        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"

        converter_widget.from_input.setText("1")
        converter_widget._on_from_input_changed("1")

        to_value = float(converter_widget.to_input.text().replace(",", ""))
        assert abs(to_value - 3.28084) < 0.001

    def test_editing_to_updates_from(self, converter_widget):
        """Test that editing TO field updates FROM field."""
        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"

        converter_widget.to_input.setText("1")
        converter_widget._on_to_input_changed("1")

        from_value = float(converter_widget.from_input.text().replace(",", ""))
        assert abs(from_value - 0.3048) < 0.001


class TestHistoryIntegration:
    """Tests for converter history integration."""

    def test_equals_records_to_history(self, window, converter_widget):
        """Test that pressing = records conversion to history."""
        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"
        converter_widget.from_input.setText("100")
        converter_widget._perform_conversion("from")

        converter_widget._record_to_history()

        assert len(window.history) == 1
        assert window.history_list.count() == 1

    def test_history_entry_format(self, window, converter_widget):
        """Test that history entry has correct format."""
        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"
        converter_widget.from_input.setText("100")
        converter_widget._perform_conversion("from")
        converter_widget._record_to_history()

        entry_text = window.history_list.item(0).text()
        assert "m" in entry_text
        assert "ft" in entry_text
        assert "[Length]" in entry_text


class TestStatePersistence:
    """Tests for state persistence across sessions."""

    def test_state_saves_on_unit_change(self, converter_widget):
        """Test that state is saved when units change."""
        settings = QSettings("Calculator", "ConverterMode")
        settings.clear()

        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "kilometer"
        converter_widget._save_state()

        saved = settings.value("units/Length/from")
        assert saved == "kilometer"

    def test_state_restores_on_init(self, qtbot):
        """Test that state is restored when widget is created."""
        settings = QSettings("Calculator", "ConverterMode")
        settings.setValue("category", "Weight")
        settings.setValue("units/Weight/from", "kilogram")
        settings.setValue("units/Weight/to", "pound")

        window = CalculatorWindow()
        qtbot.addWidget(window)
        window._switch_mode("converter")
        widget = window.mode_stack.widget(2)

        assert widget.current_category == "Weight"
        assert widget.from_unit == "kilogram"
        assert widget.to_unit == "pound"

        settings.clear()


class TestKeyboardShortcuts:
    """Tests for keyboard shortcuts in converter mode."""

    @pytest.mark.parametrize(
        "key,expected_category",
        [
            (Qt.Key.Key_F6, "Length"),
            (Qt.Key.Key_F7, "Weight"),
            (Qt.Key.Key_F8, "Temperature"),
            (Qt.Key.Key_F9, "Volume"),
            (Qt.Key.Key_F10, "Area"),
            (Qt.Key.Key_F11, "Speed"),
            (Qt.Key.Key_F12, "Time"),
            (Qt.Key.Key_F13, "Data"),
        ],
    )
    def test_function_key_switches_category(
        self, window, converter_widget, qtbot, key, expected_category
    ):
        """Test that F6-F13 switch categories."""
        from PyQt6.QtGui import QKeyEvent
        from PyQt6.QtCore import QEvent

        event = QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
        window.keyPressEvent(event)

        assert converter_widget.current_category == expected_category

    def test_escape_clears_inputs(self, window, converter_widget, qtbot):
        """Test that Escape clears input fields."""
        from PyQt6.QtGui import QKeyEvent
        from PyQt6.QtCore import QEvent

        converter_widget.from_input.setText("123")
        converter_widget.to_input.setText("456")

        event = QKeyEvent(
            QEvent.Type.KeyPress, Qt.Key.Key_Escape, Qt.KeyboardModifier.NoModifier
        )
        window.keyPressEvent(event)

        assert converter_widget.from_input.text() == "0"
        assert converter_widget.to_input.text() == "0"

    def test_ctrl_shift_s_swaps(self, window, converter_widget, qtbot):
        """Test that Ctrl+Shift+S swaps units and values."""
        from PyQt6.QtGui import QKeyEvent
        from PyQt6.QtCore import QEvent

        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"
        converter_widget.from_input.setText("100")
        converter_widget.to_input.setText("328")

        event = QKeyEvent(
            QEvent.Type.KeyPress,
            Qt.Key.Key_S,
            Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
        )
        window.keyPressEvent(event)

        assert converter_widget.from_unit == "foot"
        assert converter_widget.to_unit == "meter"


class TestHistoryRecall:
    """Tests for history recall functionality."""

    def test_double_click_history_populates_from(self, window, converter_widget, qtbot):
        """Test that double-clicking history populates FROM field."""
        converter_widget._on_category_changed("Length")
        converter_widget.from_unit = "meter"
        converter_widget.to_unit = "foot"
        converter_widget.from_input.setText("100")
        converter_widget._perform_conversion("from")
        converter_widget._record_to_history()

        converter_widget.from_input.setText("0")
        converter_widget.to_input.setText("0")

        item = window.history_list.item(0)
        window._on_history_item_clicked(item)

        assert converter_widget.from_input.text() == "100"

    def test_double_click_history_switches_category(self, window, converter_widget, qtbot):
        """Test that double-clicking history from different category switches."""
        converter_widget._on_category_changed("Weight")
        converter_widget.from_unit = "kilogram"
        converter_widget.to_unit = "pound"
        converter_widget.from_input.setText("50")
        converter_widget._perform_conversion("from")
        converter_widget._record_to_history()

        converter_widget._on_category_changed("Length")

        item = window.history_list.item(0)
        window._on_history_item_clicked(item)

        assert converter_widget.current_category == "Weight"
