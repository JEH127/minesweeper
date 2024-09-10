from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

class CellView(QWidget):

    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass  

class GameBoardView(QWidget):

    def __init__(self, *args, **kwargs):
        pass

class MainView(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass