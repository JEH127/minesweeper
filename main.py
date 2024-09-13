import sys
from PyQt6.QtWidgets import QApplication
from src.controller.game_controller import GameController

def main():
    
    app = QApplication(sys.argv)
    
    controller = GameController()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


