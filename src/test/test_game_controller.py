# import pytest
# from unittest.mock import Mock, patch
# from ..controller.game_controller import GameController
# from ..model.game_model import GameBoard
# from ..view.game_view import GameView, CustomButton

# @pytest.fixture
# def mock_model():
#     mock = Mock(spec=GameBoard)
#     mock.rows = 3
#     mock.cols = 3
#     mock.board = [[Mock() for _ in range(3)] for _ in range(3)]
#     mock.is_game_won = False
#     mock.is_game_over = False
#     mock.get_count_mines.return_value = 5
#     return mock

# @pytest.fixture
# def mock_view():
#     mock = Mock(spec=GameView)
#     mock_buttons = [[Mock(spec=CustomButton) for _ in range(3)] for _ in range(3)]
#     mock.get_buttons.return_value = mock_buttons
#     return mock

# @pytest.fixture
# def game_controller(mock_model, mock_view):
#     return GameController(mock_model, mock_view)

# def test_init(game_controller, mock_model, mock_view):
#     assert game_controller.model == mock_model
#     assert game_controller.view == mock_view

# def test_connect_buttons(game_controller, mock_view):
#     mock_buttons = mock_view.get_buttons()
#     game_controller.connect_buttons()
    
#     # Ensure that each button's connect method is called only once
#     for row in mock_buttons:
#         for btn in row:
#             btn.click_signal.connect.assert_called_once_with(game_controller.handle_button_click)

# def test_handle_button_click_left(game_controller, mock_model):
#     mock_button = Mock(spec=CustomButton)
#     mock_button.row = 1
#     mock_button.col = 2
    
#     game_controller.handle_button_click("left", mock_button)
    
#     mock_model._reveal_cell.assert_called_once_with(1, 2)
#     mock_model._flag_cell.assert_not_called()

# def test_handle_button_click_right(game_controller, mock_model):
#     mock_button = Mock(spec=CustomButton)
#     mock_button.row = 1
#     mock_button.col = 2
    
#     game_controller.handle_button_click("right", mock_button)
    
#     mock_model._flag_cell.assert_called_once_with(1, 2)
#     mock_model._reveal_cell.assert_not_called()

# @patch.object(GameController, 'update_view')
# def test_handle_button_click_updates_view(mock_update_view, game_controller):
#     mock_button = Mock(spec=CustomButton)
#     mock_button.row = 1
#     mock_button.col = 2
    
#     game_controller.handle_button_click("left", mock_button)
#     mock_update_view.assert_called_once()

# def test_update_view(game_controller, mock_model, mock_view):
#     mock_buttons = mock_view.get_buttons()
    
#     # Setup cell attributes in mock_model
#     for row in mock_model.board:
#         for cell in row:
#             cell.is_flagged = False
#             cell.is_revealed = False
#             cell.is_mine = False
#             cell.adjacent_mines = 0
    
#     game_controller.update_view()
    
#     # Check that flag_cell and reveal_cell are called appropriately
#     for row in range(mock_model.rows):
#         for col in range(mock_model.cols):
#             cell = mock_model.board[row][col]
#             button = mock_buttons[row][col]
            
#             if cell.is_flagged:
#                 mock_view.flag_cell.assert_any_call(True, button)
#             else:
#                 mock_view.flag_cell.assert_any_call(False, button)
            
#             if cell.is_revealed:
#                 if cell.is_mine:
#                     mock_view.reveal_cell.assert_any_call('mine', button)
#                 elif cell.adjacent_mines == 0:
#                     mock_view.reveal_cell.assert_any_call('safe', button)
#                 else:
#                     mock_view.reveal_cell.assert_any_call('number', button, cell.adjacent_mines)
#             else:
#                 button.setText.assert_called_with("")

# @patch.object(GameController, 'game_over_or_win_check')
# @patch.object(GameController, 'update_mine_counter')
# def test_update_view_calls_checks(mock_update_counter, mock_game_over_check, game_controller):
#     game_controller.update_view()
#     mock_game_over_check.assert_called_once()
#     mock_update_counter.assert_called_once()

# def test_update_mine_counter(game_controller, mock_model, mock_view):
#     mock_model.get_count_mines.return_value = 5
    
#     game_controller.update_mine_counter()
    
#     mock_view.update_view_mine_counter.assert_called_once_with(5)

# def test_game_over_or_win_check_win(game_controller, mock_model, mock_view):
#     mock_model.is_game_won = True
#     mock_model.is_game_over = False
    
#     game_controller.game_over_or_win_check()
    
#     mock_view.show_game_over_message.assert_called_once_with(won=True)

# def test_game_over_or_win_check_lose(game_controller, mock_model, mock_view):
#     mock_model.is_game_won = False
#     mock_model.is_game_over = True
    
#     game_controller.game_over_or_win_check()
    
#     mock_view.show_game_over_message.assert_called_once_with(won=False)

# def test_game_over_or_win_check_ongoing(game_controller, mock_model, mock_view):
#     mock_model.is_game_won = False
#     mock_model.is_game_over = False
    
#     game_controller.game_over_or_win_check()
    
#     mock_view.show_game_over_message.assert_not_called()

import pytest
from unittest.mock import Mock, patch
from ..controller.game_controller import GameController
from ..model.game_model import GameBoard
from ..view.game_view import GameView, CustomButton

@pytest.fixture
def mock_model():
    mock = Mock(spec=GameBoard)
    mock.rows = 3
    mock.cols = 3
    mock.board = [[Mock() for _ in range(3)] for _ in range(3)]
    mock.is_game_won = False
    mock.is_game_over = False
    mock.get_count_mines.return_value = 5
    return mock

@pytest.fixture
def mock_view():
    mock = Mock(spec=GameView)
    mock_buttons = [[Mock(spec=CustomButton) for _ in range(3)] for _ in range(3)]
    mock.get_buttons.return_value = mock_buttons
    return mock

@pytest.fixture
def game_controller(mock_model, mock_view):
    return GameController(mock_model, mock_view)

def test_init(game_controller, mock_model, mock_view):
    assert game_controller.model == mock_model
    assert game_controller.view == mock_view

def test_connect_buttons(game_controller, mock_view):
    mock_buttons = mock_view.get_buttons()
    
    # Clear any previous calls to connect
    for row in mock_buttons:
        for btn in row:
            btn.click_signal.connect.reset_mock()
    
    game_controller.connect_buttons()

    # Ensure that each button's connect method is called only once with the correct handler
    for row in mock_buttons:
        for btn in row:
            btn.click_signal.connect.assert_called_once_with(game_controller.handle_button_click)

def test_handle_button_click_left(game_controller, mock_model):
    mock_button = Mock(spec=CustomButton)
    mock_button.row = 1
    mock_button.col = 2
    
    game_controller.handle_button_click("left", mock_button)
    
    mock_model._reveal_cell.assert_called_once_with(1, 2)
    mock_model._flag_cell.assert_not_called()

def test_handle_button_click_right(game_controller, mock_model):
    mock_button = Mock(spec=CustomButton)
    mock_button.row = 1
    mock_button.col = 2
    
    game_controller.handle_button_click("right", mock_button)
    
    mock_model._flag_cell.assert_called_once_with(1, 2)
    mock_model._reveal_cell.assert_not_called()

@patch.object(GameController, 'update_view')
def test_handle_button_click_updates_view(mock_update_view, game_controller):
    mock_button = Mock(spec=CustomButton)
    mock_button.row = 1
    mock_button.col = 2
    
    game_controller.handle_button_click("left", mock_button)
    mock_update_view.assert_called_once()

def test_update_view(game_controller, mock_model, mock_view):
    mock_buttons = mock_view.get_buttons()
    
    # Setup cell attributes in mock_model
    for row in mock_model.board:
        for cell in row:
            cell.is_flagged = False
            cell.is_revealed = False
            cell.is_mine = False
            cell.adjacent_mines = 0
    
    game_controller.update_view()
    
    # Check that flag_cell and reveal_cell are called appropriately
    for row in range(mock_model.rows):
        for col in range(mock_model.cols):
            cell = mock_model.board[row][col]
            button = mock_buttons[row][col]
            
            if cell.is_flagged:
                mock_view.flag_cell.assert_any_call(True, button)
            else:
                mock_view.flag_cell.assert_any_call(False, button)
            
            if cell.is_revealed:
                if cell.is_mine:
                    mock_view.reveal_cell.assert_any_call('mine', button)
                elif cell.adjacent_mines == 0:
                    mock_view.reveal_cell.assert_any_call('safe', button)
                else:
                    mock_view.reveal_cell.assert_any_call('number', button, cell.adjacent_mines)
            else:
                button.setText.assert_called_with("")

@patch.object(GameController, 'game_over_or_win_check')
@patch.object(GameController, 'update_mine_counter')
def test_update_view_calls_checks(mock_update_counter, mock_game_over_check, game_controller):
    game_controller.update_view()
    mock_game_over_check.assert_called_once()
    mock_update_counter.assert_called_once()

def test_update_mine_counter(game_controller, mock_model, mock_view):
    mock_model.get_count_mines.return_value = 5
    
    game_controller.update_mine_counter()
    
    mock_view.update_view_mine_counter.assert_called_once_with(5)

def test_game_over_or_win_check_win(game_controller, mock_model, mock_view):
    mock_model.is_game_won = True
    mock_model.is_game_over = False
    
    game_controller.game_over_or_win_check()
    
    mock_view.show_game_over_message.assert_called_once_with(won=True)

def test_game_over_or_win_check_lose(game_controller, mock_model, mock_view):
    mock_model.is_game_won = False
    mock_model.is_game_over = True
    
    game_controller.game_over_or_win_check()
    
    mock_view.show_game_over_message.assert_called_once_with(won=False)

def test_game_over_or_win_check_ongoing(game_controller, mock_model, mock_view):
    mock_model.is_game_won = False
    mock_model.is_game_over = False
    
    game_controller.game_over_or_win_check()
    
    mock_view.show_game_over_message.assert_not_called()
