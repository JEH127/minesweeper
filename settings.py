import os
import random

# Base path for assets
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Fonts Path
FONT_PATH_1 = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'fonts', 'Creepster', 'Creepster-Regular.ttf')
FONT_PATH_2 = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'fonts', 'Cutive_Mono', 'CutiveMono-Regular.ttf')

# Music Path
MUSIC_PATH = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'musics', 'ES_The Haunted Concert Hall - Luella Gren.mp3')

# Sounds Path
GAME_OVER_PATH = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'sounds', 'game_over.mp3')
VICTORY_PATH = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'sounds', 'victory.mp3')
SIGIL_PATH = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'sounds', 'sigil.mp3')

FLOOR_SOUNDS = [
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'sounds', 'floor', f'{i}.mp3')
    for i in range(1, 5)
]

NUMBERS_SOUNDS = [
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'sounds', 'number', f'{i}.wav')
    for i in range(1, 4)
]

# Images paths
ICON_PATH = os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'images', 'icon.png')

FLOOR_IMAGES = [
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'images', 'floors', f'{i}.png')
    for i in range(1, 13)
]

SIGIL_IMAGES = [
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'images', 'sigils', f'{i}.png')
    for i in range(1, 6)
]

SPIRIT_IMAGES = [
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'images', 'spirits', f'{i}.png')
    for i in range(1, 5)
]

GAME_STATUS = [ 
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'images', 'game_state', 'game_over.png'),
    os.path.join(BASE_DIR, 'minesweeper', 'src', 'assets', 'images', 'game_state', 'victory.png')
]

# Choose a random image from a list
def get_random_image(image_list : str) -> str:
    '''
    Selects a random image from a list of image paths.
    '''
    match image_list:
        case 'spirits':
            list = SPIRIT_IMAGES
        case 'floors':
            list = FLOOR_IMAGES
        case 'sigils':
            list = SIGIL_IMAGES
        case 'floor_sound' :
            list = FLOOR_SOUNDS
            
    return random.choice(list)
