from PyQt6.QtWidgets import QGridLayout, QPushButton, QWidget, QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import settings as st

class CustomButton(QPushButton):
    # Define a custom signal to emit click type and button reference
    click_signal = pyqtSignal(str, object)  # 'str' for click type, 'object' for button

    def __init__(self, row : int, col : int, revealed : bool = False, flagged : bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Position of the button
        self.row = row
        self.col = col
        # Tell if the button is already revealed or flagged
        self.revealed = revealed
        self.flagged = flagged

    def mousePressEvent(self, event : Qt.MouseButton) -> None:
        '''
        Override mousePressEvent to differentiate between left and right clicks.
        '''
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_signal.emit("left", self)  # Emit signal with click type and button
        elif event.button() == Qt.MouseButton.RightButton:
            self.click_signal.emit("right", self)  # Emit signal with click type and button

class GameView(QWidget):
    def __init__(self, rows: int, cols: int) -> None:
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.buttons = []
        
        self.initUI()

    def initUI(self) -> None:
        '''
        Initialize the user interface
        '''
        self.setWindowTitle("Haunted Manor")
        self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(QIcon(st.ICON_PATH))
        
        # Set up the font
        self.font_id = QFontDatabase.addApplicationFont(st.FONT_PATH)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font = QFont(self.font_family, 20)
        
        # # Set up the background music
        # self.player = QMediaPlayer()
        # self.audio_output = QAudioOutput()
        # self.player.setAudioOutput(self.audio_output)
        # self.player.setSource(QUrl.fromLocalFile(st.MUSIC_PATH))
        # self.audio_output.setVolume(10)
        # self.player.play()
    
        # Create a grid layout
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Add buttons to the grid
        for row in range(self.rows):
            row_buttons = []
            for col in range(self.cols):
                btn = CustomButton(row, col, "")
                btn.setFixedSize(QSize(50, 50))  # Set a fixed button size
                btn.clicked.connect(self.on_click)  # Connect the "clicked" signal to a slot
                row_buttons.append(btn)
                grid_layout.addWidget(btn, row, col)
            self.buttons.append(row_buttons)

    def on_click(self) -> None:
        '''
        Handle button click event
        '''
        button = self.sender()  # Get the button that triggered the event

    # def show_game_over_message(self, won: bool) -> None:
    #     '''
    #     Display a message when the game is over
    #     '''
    #     msg = QMessageBox()
    #     if won:
    #         msg.setText("Congratulations! You won!")
    #     else:
    #         msg.setText("Sorry! You lost!")
    #     msg.exec()
    
    # def reset_board(self) -> None:
    #     '''
    #     Reset all the buttons
    #     '''
    #     for row in self.buttons:
    #         for btn in row:
    #             btn.setText("")
    
    def get_buttons(self) -> list[list[CustomButton]]:
        '''
        Return all buttons as a 2D list
        '''
        return self.buttons
    
    def update_view(self) -> None:
        '''
        Update the view based on the model
        '''
        for row in range(self.model.rows):
            for col in range(self.model.cols):
                value = self.model.get_cell(row, col)
                self.buttons[row][col].setText(str(value))

    def reveal_cell(self, type : str, button : CustomButton, adjacent_mines : int = None) -> None:
        # Put an icon only if the button is not already revealed
        if not button.revealed:
            if type == 'mine':
                # SPIRIT
                button.setIcon(QIcon(st.get_random_image('spirits')))
                button.setIconSize(QSize(45, 45))
                print(st.get_random_image('spirits'))
            elif type == 'safe':
                # FLOOR
                button.setIcon(QIcon(st.get_random_image('floors')))
                button.setIconSize(QSize(45, 45))
            else:
                # NUMBER
                button.setText(str(adjacent_mines))
                button.setFont(self.font)
            button.revealed = True
    
    def flag_cell(self, flag : bool, button : CustomButton) -> None:
        # Put an icon only if the button is not already flagged
        if not button.flagged and flag: 
            button.setIcon(QIcon(st.get_random_image('sigils')))
            button.setIconSize(QSize(45, 45))
            button.flagged = True 
        # Remove the icon only if the button is already flagged
        elif button.flagged and not flag:
            button.setIcon(QIcon())
            button.flagged = False

    def show_game_over_message(self, won: bool) -> None:
        '''
        Display a message when the game is over with an image
        '''
        # Create a custom dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Fate Sealed")

        # Create layout for the dialog
        layout = QVBoxLayout()

        # Create label for the text
        message_label = QLabel()
        if won:
            image_path = st.GAME_STATUS[1]
        else:
            image_path = st.GAME_STATUS[0]

        # Create label for the image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add labels to the layout
        layout.addWidget(message_label)
        layout.addWidget(image_label)

        # Set the layout to the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec()