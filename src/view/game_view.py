import sys
from PyQt6.QtWidgets import QApplication, QGridLayout, QPushButton, QWidget, QMessageBox
from PyQt6.QtCore import QSize


class GameView(QWidget):
    def __init__(self, rows: int, cols: int):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.buttons = []
        
        self.initUI()

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("Minesweeper")
        self.setGeometry(100, 100, 400, 400)

        # Create a grid layout
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Add buttons to the grid
        for row in range(self.rows):
            row_buttons = []
            for col in range(self.cols):
                btn = QPushButton("")
                btn.setFixedSize(QSize(40, 40))  # Set a fixed button size
                btn.clicked.connect(self.on_click)  # Connect the "clicked" signal to a slot
                row_buttons.append(btn)
                grid_layout.addWidget(btn, row, col)
            self.buttons.append(row_buttons)

    def on_click(self):
        """Handle button click event"""
        button = self.sender()  # Get the button that triggered the event
        # Here you could call a controller method to update the view
        button.setText("X")  # Set "X" as a placeholder for click, to be replaced by actual game logic
    
    def show_game_over_message(self, won: bool):
        """Display a message when the game is over"""
        msg = QMessageBox()
        if won:
            msg.setText("Congratulations! You won!")
        else:
            msg.setText("Sorry! You lost!")
        msg.exec()

    def reset_board(self):
        """Reset all the buttons"""
        for row in self.buttons:
            for btn in row:
                btn.setText("")
