import random

class Cell:
    def __init__(self, is_mine = False) -> None:
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class GameBoard:
    
    NEIGHBORS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    
    def __init__(self, difficulty : str = 'Easy') -> None:
        self.difficulty = difficulty
        self.rows, self.cols, self.num_mines = self.set_difficulty(self.difficulty) 
        self.board = self._create_board()
        self._place_mines()
        self._set_adjacent_mines()
        self.is_game_over = False
        self.is_game_won = False  
        self.count_mines = self.num_mines
        self.count_flags = 0
        
    def set_difficulty(self, difficulty):
        if difficulty == 'Easy':
            return 8, 8, 10
        elif difficulty == 'Medium':
            return 16, 16, 40
        elif difficulty == 'Hard':
            return 20, 20, 75
        
    def _create_board(self) -> list[list[Cell]]:
        '''
        Create a grid with customizable size
        '''
        board = [[Cell() for _ in range(self.rows)] for _ in range(self.cols)]  
        return board     

    def _place_mines(self) -> None:
        '''
        Randomly place a defined number of mines on the grid.
        '''
        # It will store the coordinates of mines as tuples.
        mine_positions = set() # uniqueness of the positions, faster than a list
        
        while len(mine_positions) < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if (row, col) not in mine_positions: # don't place multiple mines in the same location.
                mine_positions.add((row, col))
                self.board[row][col].is_mine = True # the game board as a mine by setting its is_mine attribute to True.  

    def _count_near_mines(self, row : int, col : int) -> int:
        '''
        Count the number of mine near the cell (LEFT CLICK)
        
        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        :return: The number of mine near the cell
        '''
        count = 0
        
        for dx, dy in self.NEIGHBORS:
            nx, ny = row + dx, col + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if self.board[nx][ny].is_mine:
                    count += 1
        
        return count 
    
    def _set_adjacent_mines(self) -> None:
        '''
        Set the number of adjacent mines for each cell on the board.
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                # If the cell is not a mine, calculate the number of nearby mines
                if not self.board[row][col].is_mine:
                    self.board[row][col].adjacent_mines = self._count_near_mines(row, col)
        
    def _check_index(self, row : int, col : int) -> bool:
        '''
        Check if the index is in the range of the board

        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        :return: If the indices are out of range.
        '''
        return (0 <= row < self.rows and 0 <= col < self.cols)
               
    def _reveal_cell(self, row : int, col : int) -> None:
        '''
        Reveals the cell at the specified location and updates the game state.

        - Marks the cell as revealed.
        - Checks if the cell contains a mine and ends the game if it does.
        - If the cell has no adjacent mines, recursively reveals adjacent cells.

        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        '''
        # Check if the index is in the range of the board
        if self._check_index(row, col):
            # Can't reveal if flagged
            if not self.board[row][col].is_flagged:
                if not self.board[row][col].is_revealed:
                    # Reveal adjacent cells if there are no mines
                    if self.board[row][col].adjacent_mines == 0 and not self.board[row][col].is_mine:    
                        self._reveal_adjacent_cells(row, col)
                    else:
                        # Reveal the cell
                        self.board[row][col].is_revealed = True
                    # Check if there is a mine
                    if self.board[row][col].is_mine:    
                        self.is_game_over = True    
        else:
            raise IndexError('Index out of range')
                      
    def _reveal_adjacent_cells(self, row : int, col : int) -> None:
        '''
        Automatically reveal neighboring cells if a cell with no adjacent mines is revealed.
        
        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        ''' 
        try:  
            stack = [(row, col)] 
            while stack:
                r, c = stack.pop()
                if not self._check_index(r, c):
                    continue

                if self.board[r][c].is_revealed:
                    continue

                self.board[r][c].is_revealed = True
                if self.board[r][c].adjacent_mines == 0:
                    for dx, dy in self.NEIGHBORS:
                        nx, ny = r + dx, c + dy
                        stack.append((nx, ny)) 
                        
        except Exception as e:
            print(f"Error while revealing adjacent cells: {e}")

    def _flag_cell(self, row : int, col : int) -> None:
        '''
        Allow to mark/unmark a suspected mine. (RIGHT CLICK)
        Increment and decrement my counter of suspected mines

        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        '''
        # If the cell at the given row and column has already been revealed
        if self.board[row][col].is_revealed:
            # return => early exit
            return
        
        # Player can't flag if he is out of flag.
        if not self.board[row][col].is_flagged and self.count_flags == self.num_mines:
            return
        # If the cell is not revealed, this line toggles the is_flagged attribute of the cell  
        self.board[row][col].is_flagged = not self.board[row][col].is_flagged
        # Mine counter can't go negative
        if self.board[row][col].is_flagged and self.count_mines > 0:
            self.count_mines -= 1
            self.count_flags += 1
        elif not self.board[row][col].is_flagged:
            self.count_mines += 1
            self.count_flags -= 1
        
    def _check_victory(self) -> None:
        '''
        Check for victory when all non-mined cells are revealed.
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
               
                # if the current cell is not a mine and is not revealed
                if not cell.is_mine and not cell.is_revealed:
                    return False
        # At this point, all non-mined cells are revealed and the game is won
        # the loops complete without finding any non-mine unrevealed cells
        self.is_game_won = True

    def get_count_mines(self) -> int:
        '''
        Get the total number of mines on the board.
        :return: The total number of mines on the board
        '''

        return self.count_mines

    def get_difficulty(self) -> str:
        '''
        Get the difficulty
        :return: return the difficulty
        '''

        return self.difficulty
    
    def get_board_settings(self) -> tuple[int, int, int, str]:
        '''
            Returns the settings of the game board.

            :return: A tuple containing three integers:
                    - The number of rows (rows)
                    - The number of columns (cols)
                    - The number of mines (num_mines)
        '''
        return self.rows, self.cols, self.num_mines, self.difficulty