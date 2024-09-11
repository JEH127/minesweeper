import pytest
from model.game_model import Cell, GameBoard

def test_cell_initialization():
    cell = Cell()
    assert not cell.is_mine
    assert not cell.is_revealed
    assert not cell.is_flagged
    assert cell.adjacent_mines == 0

    mine_cell = Cell(is_mine=True)
    assert mine_cell.is_mine

def test_gameboard_initialization():
    board = GameBoard(10, 10, 10)
    assert board.rows == 10
    assert board.cols == 10
    assert board.num_mines == 10
    assert len(board.board) == 10
    assert len(board.board[0]) == 10
    assert not board.is_game_over
    assert not board.is_game_won

def test_mine_placement():
    board = GameBoard(10, 10, 10)
    mine_count = sum(cell.is_mine for row in board.board for cell in row)
    assert mine_count == 10

def test_adjacent_mines_calculation():
    board = GameBoard(3, 3, 1)
    # Force a mine placement for testing
    board.board[1][1].is_mine = True
    board._set_adjacent_mines()

    expected_adjacent_mines = [
        [1, 2, 1],
        [2, 0, 2],
        [1, 2, 1]
    ]

    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                assert board.board[i][j].is_mine
                assert board.board[i][j].adjacent_mines == 0
            else:
                assert board.board[i][j].adjacent_mines == expected_adjacent_mines[i][j], \
                    f"Mismatch at position ({i}, {j}): expected {expected_adjacent_mines[i][j]}, " \
                    f"got {board.board[i][j].adjacent_mines}"

def test_reveal_cell():
    board = GameBoard(5, 5, 1)
    # Force a mine placement for testing
    board.board[2][2].is_mine = True
    board._set_adjacent_mines()

    # Reveal a non-mine cell
    board._reveal_cell(0, 0)
    assert board.board[0][0].is_revealed
    assert not board.is_game_over

    # Reveal a mine cell
    board._reveal_cell(2, 2)
    assert board.board[2][2].is_revealed
    assert board.is_game_over

def test_flag_cell():
    board = GameBoard(5, 5, 1)
    board.flag_cell(0, 0)
    assert board.board[0][0].is_flagged

    # Unflag the cell
    board.flag_cell(0, 0)
    assert not board.board[0][0].is_flagged

    # Try to flag a revealed cell
    board.board[1][1].is_revealed = True
    board.flag_cell(1, 1)
    assert not board.board[1][1].is_flagged

def test_check_victory():
    board = GameBoard(3, 3, 1)
    # Force a mine placement for testing
    board.board[1][1].is_mine = True
    board._set_adjacent_mines()

    # Reveal all non-mine cells
    for i in range(3):
        for j in range(3):
            if i != 1 or j != 1:
                board._reveal_cell(i, j)

    board._check_victory()
    assert board.is_game_won

@pytest.mark.parametrize("row,col", [(-1, 0), (0, -1), (10, 0), (0, 10)])
def test_reveal_cell_out_of_bounds(row, col):
    board = GameBoard(10, 10, 10)
    with pytest.raises(IndexError):
        board._reveal_cell(row, col)

def test_reveal_adjacent_cells():
    board = GameBoard(5, 5, 1)
    # Force a mine placement for testing
    board.board[4][4].is_mine = True
    board._set_adjacent_mines()

    # Reveal a cell with no adjacent mines
    board._reveal_cell(0, 0)

    # Check that at least the clicked cell is revealed
    assert board.board[0][0].is_revealed, "The clicked cell should be revealed"

    # Check if any adjacent cells are revealed
    adjacent_revealed = any(
        board.board[i][j].is_revealed
        for i in range(2) for j in range(2)
        if (i, j) != (0, 0)
    )
    
    assert adjacent_revealed, "At least one adjacent cell should be revealed"

    # Check that cells far from the revealed cell are not revealed
    assert not board.board[4][4].is_revealed, "Cells far from the revealed cell should not be revealed"

    # Print the state of the board for debugging
    print("\nBoard state after revealing (0, 0):")
    for i in range(5):
        row = " ".join("R" if board.board[i][j].is_revealed else "." for j in range(5))
        print(row)

if __name__ == "__main__":
    pytest.main()