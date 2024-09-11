import pytest
from model.game_model import Cell, GameBoard

# Cell Class Test
def test_cell_initialization():
    cell = Cell()
    assert cell.is_mine == False
    assert cell.is_revealed == False
    assert cell.is_flagged == False
    assert cell.adjacent_mines == 0

def test_cell_initialization_with_mine():
    cell = Cell(is_mine=True)
    assert cell.is_mine == True
    assert cell.is_revealed == False
    assert cell.is_flagged == False
    assert cell.adjacent_mines == 0


# GameBoard Class Test
def test_gameboard_initialization():
    board = GameBoard(5, 5, 5)
    assert board.rows == 5
    assert board.cols == 5
    assert board.num_mines == 5
    assert board.is_game_over == False
    assert board.is_game_won == False

def test_check_index():
    board = GameBoard(5, 5, 5)
    assert board.check_index(2, 2) == True
    assert board.check_index(5, 5) == False
    assert board.check_index(-1, 0) == False

def test_count_near_mines():
    board = GameBoard(5, 5, 5)
    board.board[1][1].is_mine = True
    board.board[0][0].is_mine = True

    assert board.count_near_mines(0, 1) == 2

def test_reveal_cell_without_mine():
    board = GameBoard(5, 5, 5)
    board.board[0][0].adjacent_mines = 0
    board.reveal_cell(0, 0)
    assert board.board[0][0].is_revealed == True
    assert board.is_game_over == False

def test_reveal_cell_with_mine():
    board = GameBoard(5, 5, 5)
    board.board[2][2].is_mine = True
    board.reveal_cell(2, 2)
    assert board.board[2][2].is_revealed == True
    assert board.is_game_over == True

def test_reveal_adjacent_cells():
    board = GameBoard(5, 5, 5)
    board.board[2][2].adjacent_mines = 0
    board._reveal_adjacent_cells(2, 2)
    assert board.board[1][1].is_revealed == True
    assert board.board[2][3].is_revealed == True
    assert board.board[3][2].is_revealed == True


def test_flag_cell():
    # Test flagging an unrevealed cell
    game_board = GameBoard(5, 5, 3)
    game_board.flag_cell(2, 3)
    assert game_board.board[2][3].is_flagged == True, "Cell (2, 3) should be flagged."

    # Test unflagging a flagged cell
    game_board.flag_cell(2, 3)
    assert game_board.board[2][3].is_flagged == False, "Cell (2, 3) should be unflagged."

    # Test flagging a revealed cell should have no effect
    game_board.board[2][3].is_revealed = True
    game_board.flag_cell(2, 3)
    assert game_board.board[2][3].is_flagged == False, "Revealed cell (2, 3) should not be flagged."

    # Test multiple flag and unflag operations
    game_board.board[2][3].is_revealed = False  # Reset cell to unrevealed state
    game_board.flag_cell(2, 3)
    assert game_board.board[2][3].is_flagged == True, "Cell (2, 3) should be flagged again."
    game_board.flag_cell(2, 3)
    assert game_board.board[2][3].is_flagged == False, "Cell (2, 3) should be unflagged again."
    game_board.flag_cell(2, 3)
    assert game_board.board[2][3].is_flagged == True, "Cell (2, 3) should be flagged once more."


def test_check_victory():
    # Create a GameBoard instance with 5 rows, 5 columns, and 5 mines
    game_board = GameBoard(5, 5, 5)
    
    # Initially, the game should not be won
    assert not game_board._check_victory()
    
    # Reveal all non-mine cells
    game_board.reveal_all_non_mine_cells()
    
    # Now, the game should be won
    assert game_board._check_victory()
    assert game_board.is_game_won