import sys
from PyQt6.QtWidgets import QApplication
# import pyqtgraph as pg
from src.view.game_view import GameView
from src.model.game_model import Cell, GameBoard
from src.controller.game_controller import GameController


def main():
    app = QApplication(sys.argv)

    model = GameBoard(5, 5,1)
    view = GameView(5, 5)
    controller = GameController(model, view)
    
    # model = GameBoard()
    # view = GameView()
    # controller = GameController(model, view)
    
    view.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


