from PyQt6.QtWidgets import QGridLayout, QPushButton, QWidget, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QComboBox
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
import settings as st
import sys

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
    def __init__(self, board_settings : tuple[int, int, int]) -> None:
        super().__init__()

        self.buttons = []        
        self.initUI(board_settings)
        self.show()

    def initUI(self, board_settings : tuple[int, int, int]) -> None:
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
        self.font_2 = QFont(self.font_family, 12)


        main_layout = QVBoxLayout()
        # add by claude
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(main_layout)

        # Top bar with mine counter and difficulty selector
        top_bar = QHBoxLayout()
        
        # Mine counter
        self.mine_counter = QLabel(f"Mines: {board_settings[2]}")
        self.mine_counter.setFont(QFont(self.font_2))
        self.mine_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.addWidget(self.mine_counter)

        # Spacer to push difficulty selector to the right (Claude)
        top_bar.addStretch(1)


        # Difficulty selector
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setFont(QFont(self.font_2))
        top_bar.addWidget(difficulty_label)

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_selector.setFont(QFont(self.font_2))
        self.difficulty_selector.setStyleSheet("QComboBox { background-color: transparent; color: white; }")
        
        top_bar.addWidget(self.difficulty_selector)

        # Add top bar to main layout
        main_layout.addLayout(top_bar)

        # Set up the background music
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(st.MUSIC_PATH))
        self.audio_output.setVolume(10)
        self.player.play()
        
        # Set Sounds effects
        self.player_2 = QMediaPlayer()
        self.audio_output_2 = QAudioOutput() 
        self.player_2.setAudioOutput(self.audio_output)
        self.audio_output_2.setVolume(10)
 
        # Create a grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)
        # before claude
        # self.setLayout(grid_layout)

        # Add buttons to the grid
        for row in range(board_settings[0]):
            row_buttons = []
            for col in range(board_settings[1]):
                btn = CustomButton(row, col, "")
                btn.setFixedSize(QSize(50, 50))  # Set a fixed button size
                btn.clicked.connect(self.on_click)  # Connect the "clicked" signal to a slot
                row_buttons.append(btn)
                grid_layout.addWidget(btn, row, col)
            self.buttons.append(row_buttons)

        # claude
        # Add grid layout to main layout
        main_layout.addLayout(grid_layout)

    def on_click(self) -> None:
        '''
        Handle button click event
        '''
        button = self.sender()  # Get the button that triggered the event

    
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
    
    def reveal_cell(self, type : str, button : CustomButton, adjacent_mines : int = None) -> None:
        # Put an icon only if the button is not already revealed
        if not button.revealed:
            if type == 'mine':
                # SPIRIT
                button.setIcon(QIcon(st.get_random_image('spirits')))
                button.setIconSize(QSize(45, 45))
                print(st.get_random_image('spirits'))
                self.play_sound('game_over')
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

        layout = QVBoxLayout()
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
        
        layout.addWidget(message_label)
        layout.addWidget(image_label)
        dialog.setLayout(layout)
        dialog.exec()

    def update_view_mine_counter(self, mine_counter : int) -> None:
        '''
        Update the mine counter label
        '''
        self.mine_counter.setText(f"Mines: {mine_counter}")
        
    def play_sound(self, sound_type : str) -> None:
        match sound_type:
            case 'game_over':
                file_path = st.GAME_OVER_PATH
            case 'victory':
                file_path = st.VICTORY_PATH
            case 'floor':
                file_path = st.get_random_image('floor_sound')
            case 'number_1':
                file_path = st.NUMBERS_SOUNDS[0]
            case 'number_2' :
                file_path = st.NUMBERS_SOUNDS[1]
            case 'number_3' :
                file_path = st.NUMBERS_SOUNDS[2]
        
        self.player_2.setSource(QUrl.fromLocalFile(file_path))
        self.player_2.play()