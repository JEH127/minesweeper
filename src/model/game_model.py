class Cell:
    def __init__(self, is_mine=False):
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class GameBoard:
    
    NEIGHBORS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self._create_board()
        self._place_mines()
        self.is_game_over = False
        self.is_game_won = False       

    def _create_board(self):
        '''
        Create a grid with customizable size
        '''
                   
    def _place_mines(self):
        '''
        Randomly place a defined number of mines on the grid.
        '''
        pass

    def count_near_mines(self, row : int, col : int) -> int:
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
      
    def check_index(self, row : int, col : int) -> bool:
        '''
        Check if the index is in the range of the board

        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        :raises IndexError: If the indices are out of range.
        '''
        return (0 <= row < self.rows and 0 <= col < self.cols)
               
    def reveal_cell(self, row : int, col : int) -> None:
        '''
        Reveals the cell at the specified location and updates the game state.

        - Marks the cell as revealed.
        - Checks if the cell contains a mine and ends the game if it does.
        - If the cell has no adjacent mines, recursively reveals adjacent cells.

        :param row: The row index of the cell to reveal.
        :param col: The column index of the cell to reveal.
        '''
        # Check if the index is in the range of the board
        if self.check_index(row, col):
        
            # Reveal the cell
            if not self.board[row][col].is_revealed:
                self.board[row][col].is_revealed = True
            
                # Check if there is a mine
                if self.board[row][col].is_mine:    
                    self.is_game_over = True
                    
                # Reveal adjacent cells if there are no mines
                elif self.board[row][col].adjacent_mines == 0:      
                    self._reveal_adjacent_cells(row, col)
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

                if not self.check_index(row, col):
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

    def flag_cell(self, row, col):
        '''
        Allow to mark/unmark a suspected mine. (RIGHT CLICK)
        '''
        pass
   
    def check_victory(self):
        '''
        Check for victory when all non-mined cells are revealed.
        '''  
        pass

# Fonctionnalitées Bonus   

# class Timer:
#     def __init__(self):
#         self.time_elapsed = 0

#     def start(self):
#         pass

#     def stop(self):
#         pass