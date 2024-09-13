from PyQt6.QtWidgets import QGridLayout, QPushButton, QWidget, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QComboBox
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
    def __init__(self, board_settings : tuple[int, int, int, str]) -> None:
        super().__init__()

        self.buttons = []        
        self.initUI(board_settings)
        self.show()

    def initUI(self, board_settings : tuple[int, int, int, str]) -> None:
        '''
        Initialize the user interface
        '''
        self.setWindowTitle("Haunted Manor")
        self.setFixedSize(700, 700)
        self.setWindowIcon(QIcon(st.ICON_PATH))
        self.center_window()
        # Set the size of the buttons/icons based on the difficulty
        self.button_size = min(600 // board_settings[0], 600 // board_settings[1])
        self.icon_size = self.button_size
        self.font_1_size = self.button_size - 10
        
        
        # Set up the fonts
        self.font_id = QFontDatabase.addApplicationFont(st.FONT_PATH_1)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font = QFont(self.font_family, self.font_1_size)
        
        self.font_id = QFontDatabase.addApplicationFont(st.FONT_PATH_2)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font_2 = QFont(self.font_family, 12)
        self.font_2.setWeight(QFont.Weight.Bold)

        main_layout = QVBoxLayout()
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
        
        # Help Button
        self.help_button = QPushButton("Help?")
        self.help_button.setFont(QFont(self.font_2))
        self.help_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #6E6E6E;
                                            color: black;
                                            border: 2px solid white;
                                            border-radius: 4px;
                                            padding: 10px;
                                        }

                                        QPushButton:hover {
                                            background-color: black;
                                            color: white;
                                        }

                                        QPushButton:pressed {
                                            background-color: black; /* Une teinte plus sombre pour l'effet de pression */
                                            color: white;
                                        }
                                        """)
        top_bar.addWidget(self.help_button)

        # Spacer to push difficulty selector to the right
        top_bar.addStretch(1)
        
        # New Game Button
        self.new_game_button = QPushButton("New Game")
        self.new_game_button.setFont(QFont(self.font_2))
        self.new_game_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #4A0000; /* Rouge sang foncé */
                                            color: white;
                                            border: 2px solid black;
                                            border-radius: 4px;
                                            padding: 10px;
                                        }

                                        QPushButton:hover {
                                            background-color: #6A0000; /* Une teinte plus claire pour l'effet de survol */
                                            color: white;
                                        }

                                        QPushButton:pressed {
                                            background-color: #3A0000; /* Une teinte plus sombre pour l'effet de pression */
                                            color: white;
                                        }
                                        """)
        top_bar.addWidget(self.new_game_button)

        # Difficulty selector
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setFont(QFont(self.font_2))
        top_bar.addWidget(difficulty_label)

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_selector.setFont(QFont(self.font_2))
        self.difficulty_selector.setStyleSheet("QComboBox { background-color: transparent; color: white; }")
        self.difficulty_selector.setCurrentText(board_settings[3])
        top_bar.addWidget(self.difficulty_selector)

        # Add top bar to main layout
        main_layout.addLayout(top_bar)

        # Set up the background music
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(st.MUSIC_PATH))
        self.audio_output.setVolume(0.2)
        self.player.play()
        
        # Set Sounds effects
        self.player_2 = QMediaPlayer()
        self.audio_output_2 = QAudioOutput() 
        self.player_2.setAudioOutput(self.audio_output_2)
        self.audio_output_2.setVolume(0.5)
 
        # Create a grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(2)

        # Add buttons to the grid
        for row in range(board_settings[0]):
            row_buttons = []
            for col in range(board_settings[1]):
                btn = CustomButton(row, col, "")
                btn.setFixedSize(QSize(self.button_size, self.button_size)) 
                btn.setStyleSheet("background-color: #1a1a1a;\
                                  border: 2 px solid white;\
                                  border-radius: 4px;")
                btn.clicked.connect(self.on_click) 
                row_buttons.append(btn)
                grid_layout.addWidget(btn, row, col)
            self.buttons.append(row_buttons)

        # Add grid layout to main layout
        main_layout.addLayout(grid_layout)
        
    def on_click(self) -> None:
        '''
        Handle button click event
        '''
        button = self.sender()  # Get the button that triggered the event
    
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
                button.setIconSize(QSize(self.icon_size, self.icon_size))
                print(st.get_random_image('spirits'))
            elif type == 'safe':
                # FLOOR
                button.setIcon(QIcon(st.get_random_image('floors')))
                button.setIconSize(QSize(self.icon_size, self.icon_size))
                # self.play_sound('floor')
            else:
                # NUMBER
                button.setText(str(adjacent_mines))
                button.setFont(self.font)
                # self.play_sound(str(adjacent_mines))
            button.revealed = True
    
    def flag_cell(self, flag : bool, button : CustomButton) -> None:
        # Put an icon only if the button is not already flagged
        if not button.flagged and flag: 
            button.setIcon(QIcon(st.get_random_image('sigils')))
            button.setIconSize(QSize(self.icon_size, self.icon_size))
            button.flagged = True 
            self.play_sound('sigil')
        # Remove the icon only if the button is already flagged
        elif button.flagged and not flag:
            button.setIcon(QIcon())
            button.flagged = False

    def show_message(self, type : str) -> None:
        '''
        Display a message with an image
        '''
        # Create a custom dialog
        dialog = QDialog(self)
        layout = QVBoxLayout()
        
        match type:
            case 'victory':
                image_path = st.GAME_STATUS[1]
                dialog.setWindowTitle("Evil Banished")
            case 'game_over':
                image_path = st.GAME_STATUS[0]
                dialog.setWindowTitle("Fate Sealed")
            case 'intro':
                image_path = st.GAME_STATUS[2]
                dialog.setWindowTitle("Why?")
            case 'help':
                image_path = st.GAME_STATUS[3]
                dialog.setWindowTitle("Help?")
            
        # Create label for the image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        layout.addWidget(image_label)
        dialog.setLayout(layout)
        dialog.resize(800, 400)
        dialog.exec()

    def update_view_mine_counter(self, mine_counter : int) -> None:
        '''
        Update the mine counter label
        '''
        self.mine_counter.setText(f"Mines: {mine_counter}")
        
    def play_sound(self, sound_type: str) -> None:
        """
        Play a sound based on the provided sound type.

        This function plays a sound corresponding to the specified `sound_type`. If `sound_type`
        matches one of the predefined cases, the corresponding sound file is played. If `sound_type`
        does not match any predefined case, a default sound (associated with '3') is played.

        :param sound_type: A string representing the type of sound to play. It can be one of the following:
                        - 'game_over': Plays the game over sound.
                        - 'victory': Plays the victory sound.
                        - 'floor': Plays a random floor sound.
                        - '1': Plays the sound associated with the number 1.
                        - '2': Plays the sound associated with the number 2.
                        - '3': Plays the sound associated with the number 3.
        :return: None. This function does not return any value.
        
        :raises: This function does not explicitly raise any exceptions. If an invalid `sound_type` is provided,
                it defaults to playing the sound associated with '3'.
        """
        match sound_type:
            case 'game_over':
                file_path = st.GAME_OVER_PATH
            case 'victory':
                file_path = st.VICTORY_PATH
            case 'sigil':
                file_path = st.SIGIL_PATH
            case 'floor':
                file_path = st.get_random_image('floor_sound')
            case '1':
                file_path = st.NUMBERS_SOUNDS[0]
            case '2':
                file_path = st.NUMBERS_SOUNDS[1]
            case '3':
                file_path = st.NUMBERS_SOUNDS[2]
            case _:
                file_path = st.NUMBERS_SOUNDS[2]  # Default to '3' sound if `sound_type` is unrecognized
                
        # Set the source of the player to the chosen file path and play the sound
        self.player_2.setSource(QUrl.fromLocalFile(file_path))
        self.player_2.play()
     
    def center_window(self) -> None:
        '''
        Center the window on the screen
        '''
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()

        # Calculate the position to center the window
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Move the window to the calculated position
        self.move(x, y)