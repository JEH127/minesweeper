import sys
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg
from src.view.game_view import GameView
from src.model.game_model import Cell, GameBoard
from src.controller.game_controller import GameController


def main():
    app = QApplication(sys.argv)

    model = GameBoard(4, 4, 2)
    view = GameView(4, 4)
    controller = GameController(model, view)

    view.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


