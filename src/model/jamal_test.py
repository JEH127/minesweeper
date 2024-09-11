import random

class Cell:
    def __init__(self, is_mine=False):
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def __repr__(self):
        if self.is_revealed:
            return 'R' if not self.is_mine else 'M'
        return 'F' if self.is_flagged else 'H'

class GameBoard:
    
    NEIGHBORS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = self._create_board()
        self._place_mines()
        self.is_game_over = False
        self.is_game_won = False       

    def _create_board(self) -> list:
        '''
        Create a grid with customizable size
        '''
        board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]  
        return board     

    def _place_mines(self) -> None:
        '''
        Randomly place a defined number of mines on the grid.
        '''
        mine_positions = set() # uniqueness of the positions, faster than a list
        
        while len(mine_positions) < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in mine_positions: # don't place multiple mines in the same location.
                mine_positions.add((row, col))
                self.board[row][col].is_mine = True # the game board as a mine by setting its is_mine attribute to True.

    def flag_cell(self, row, col):
        '''
        Allow to mark/unmark a suspected mine. (RIGHT CLICK)
        '''
        if self.board[row][col].is_revealed:
            print("You cannot flag a revealed cell!")
            return

        self.board[row][col].is_flagged = not self.board[row][col].is_flagged
        print(f"Cell at ({row}, {col}) flagged status: {self.board[row][col].is_flagged}")

    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print()

# Example usage:
game = GameBoard(5, 5, 3)
game.print_board()

# Flagging a cell
game.flag_cell(2, 3)
game.print_board()

# Unflagging the same cell
game.flag_cell(2, 3)
game.print_board()

### OUTPUTS ###
'''
H H H H H
H H H H H
H H H H H
H H H H H
H H H H H

Cell at (2, 3) flagged status: True
H H H H H
H H H H H
H H H F H
H H H H H
H H H H H

Cell at (2, 3) flagged status: False
H H H H H
H H H H H
H H H H H
H H H H H
H H H H H

'''