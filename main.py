import sys
from PyQt6.QtWidgets import QApplication
from src.view.game_view import GameView
from src.model.game_model import Cell, GameBoard
from src.controller.game_controller import GameController


def main():
    app = QApplication(sys.argv)

    controller = GameController()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


