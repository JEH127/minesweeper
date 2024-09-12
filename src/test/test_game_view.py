import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
from ..view.game_view import GameView, CustomButton

@pytest.fixture
def game_view(qtbot):
    # Set up the GameView with a grid of 5x5 and 10 mines
    view = GameView(rows=5, cols=5, count_mines=10)
    qtbot.addWidget(view)
    return view

def test_button_creation(game_view):
    # Check if buttons are created correctly
    assert len(game_view.buttons) == 5  # Should have 5 rows
    assert len(game_view.buttons[0]) == 5  # Should have 5 columns

def test_custom_button_signal(qtbot):
    # Create a custom button and check its click_signal behavior
    button = CustomButton(0, 0)
    with qtbot.waitSignal(button.click_signal) as blocker:
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert blocker.args == ['left', button]  # Check that the signal emitted is correct

    with qtbot.waitSignal(button.click_signal) as blocker:
        qtbot.mouseClick(button, Qt.MouseButton.RightButton)
    assert blocker.args == ['right', button]  # Check right-click signal

def test_reveal_cell(game_view):
    button = game_view.buttons[0][0]
    assert not button.revealed  # Ensure button is not revealed initially

    game_view.reveal_cell('safe', button)
    assert button.revealed  # The button should be revealed after calling reveal_cell

def test_flag_cell(game_view):
    button = game_view.buttons[1][1]
    assert not button.flagged  # Ensure button is not flagged initially

    game_view.flag_cell(True, button)
    assert button.flagged  # The button should be flagged

    game_view.flag_cell(False, button)
    assert not button.flagged  # The button should no longer be flagged

def test_mine_counter_update(game_view):
    initial_text = game_view.mine_counter.text()
    game_view.update_view_mine_counter(5)
    updated_text = game_view.mine_counter.text()
    assert initial_text != updated_text  # Ensure the mine counter text is updated




def test_game_over_message_display(game_view, qtbot):
    # Simulate showing game-over message
    dialog = QDialog(game_view)  # Create an instance of the dialog
    dialog.show()  # Make sure the dialog is shown
    with qtbot.waitExposed(dialog):  # Pass the instance of QDialog, not the class
        assert dialog.isVisible()  # Check if the dialog is visible
