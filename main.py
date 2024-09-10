import sys
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg
from src.view.game_view import AppView
from src.model.game_model import Cell, GameBoard, GameState
from src.controller.game_controller import GameController

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    

    # # model = GameModel()
    # # view = AppView()
    # controller = GameController(model, view)

    # view.show()

    sys.exit(app.exec())

