from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

class CellView(QWidget):
    # Signals to notify the controller of user actions
    cell_left_clicked = pyqtSignal(int, int)
    cell_right_clicked = pyqtSignal(int, int)

    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col
        self.setFixedSize(30, 30)  # Fixed size for each cell
        self.setStyleSheet("border: 1px solid black;")  # Border to visualize cells
        self.setAutoFillBackground(True)
        self.set_background_color(Qt.gray)

        # Handle left and right mouse clicks
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_right_click)
        self.mousePressEvent = self.handle_mouse_click

    def handle_mouse_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.cell_left_clicked.emit(self.row, self.col)
        elif event.button() == Qt.MouseButton.RightButton:
            self.cell_right_clicked.emit(self.row, self.col)

    def on_right_click(self, pos):
        self.cell_right_clicked.emit(self.row, self.col)

    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def update_view(self, cell):
        if cell.is_revealed:
            if cell.is_mine:
                self.set_background_color(Qt.red)
            else:
                self.set_background_color(Qt.white)
                self.setToolTip(str(cell.adjacent_mines) if cell.adjacent_mines > 0 else '')
        else:
            self.set_background_color(Qt.gray)
        if cell.is_flagged:
            self.setStyleSheet("background-color: yellow; border: 1px solid black;")
