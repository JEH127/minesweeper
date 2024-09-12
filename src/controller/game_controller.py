from ..model.game_model import GameBoard
from ..view.game_view import GameView, CustomButton

class GameController:

    def __init__(self, model : GameBoard, view : GameView):
        self.model = model
        self.view = view
        
        
        # Connect buttons in the view to their respective handler methods
        self.connect_buttons()
            
    def connect_buttons(self) -> None:
        '''
        Connect each button in the grid to the custom click signal.
        '''
        buttons = self.view.get_buttons()
        for row in buttons:
            for btn in row:
                btn.click_signal.connect(self.handle_button_click)
            
    '''
    After each action (click on a cell), check for defeat or victory by calling the appropriate methods from the model.
    '''
    
    def handle_button_click(self, click_type : str, button : CustomButton) -> None:
        '''
        Handle button click event based on type (left or right).
        '''
        if click_type == "left":
            self.model._reveal_cell(button.row, button.col)
        elif click_type == "right":
            self.model._flag_cell(button.row, button.col)
            
        self.update_view()
            
    def new_game(self):    
        '''
        Initialize a new game according to the chosen difficulty (call the model's methods to generate a new grid).
        '''
        pass
    
    def update_view(self) -> None:
        """
        Update the view based on the model.
        This method updates each button to reflect the state of the corresponding cell in the model.
        """
        # TODO , getter et setter model
        for row in range(self.model.rows):
            for col in range(self.model.cols):
                cell = self.model.board[row][col]
                button = self.view.get_buttons()[row][col]
                
                # Update button appearance based on flagged status
                if cell.is_flagged:
                    self.view.flag_cell(True, button)
                else:
                    self.view.flag_cell(False, button)
                    
                # Update button appearance based on reveal status
                if cell.is_revealed:
                    # SPIRITS
                    if cell.is_mine:
                        self.view.reveal_cell('mine', button)
                    elif cell.adjacent_mines == 0:
                        # FLOOR
                        self.view.reveal_cell('safe', button)
                    else:
                        self.view.reveal_cell('number', button, cell.adjacent_mines)
                else:
                    button.setText("")  # Clear text if the cell is not revealed

    
        # game over or win check
        self.game_over_or_win_check()
        
        # mine_counter updated in view
        self.update_mine_counter()


    def update_mine_counter(self) -> None:
        '''
        Update the number of remaining mines in the view.
        '''
        self.view.update_view_mine_counter(self.model.get_count_mines())

    def game_over_or_win_check(self)  -> None:
        '''
        Check if the game is over or won.
        Update the view with appropriate messages.
        '''
        if self.model.is_game_won:
            self.view.show_game_over_message(won=True)
        elif self.model.is_game_over:
            self.view.show_game_over_message(won=False)
        