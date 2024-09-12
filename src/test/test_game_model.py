import pytest
from ..model.game_model import GameBoard, Cell

@pytest.fixture
def sample_board():
    return GameBoard(rows=5, cols=5, num_mines=5)

def test_board_initialization(sample_board):
    assert len(sample_board.board) == 5
    assert len(sample_board.board[0]) == 5

def test_placing_mines(sample_board):
    mine_count = sum(cell.is_mine for row in sample_board.board for cell in row)
    assert mine_count == 5

def test_reveal_cell(sample_board):
    # Mock reveal operation on a specific cell
    sample_board._reveal_cell(0, 0)
    assert sample_board.board[0][0].is_revealed

def test_flag_cell(sample_board):
    # Mock flag operation on a specific cell
    sample_board._flag_cell(1, 1)
    assert sample_board.board[1][1].is_flagged

def test_check_victory(sample_board):
    # Simulate revealing all non-mine cells to check for victory
    for row in range(sample_board.rows):
        for col in range(sample_board.cols):
            if not sample_board.board[row][col].is_mine:
                sample_board._reveal_cell(row, col)
    
    # Check victory status
    sample_board._check_victory()
    
    assert sample_board.is_game_won

