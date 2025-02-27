from enum import Enum

class Config(Enum):

    # Paramètres de la fenêtre
    GRID_BLOCK_SIZE = 64
    GRID_WIDTH = 10
    GRID_HEIGHT = 10
    MARGIN = 10
    INFO_PANEL_HEIGHT = GRID_BLOCK_SIZE + (MARGIN * 2)
    WINDOWS_WIDTH = GRID_WIDTH * GRID_BLOCK_SIZE
    WINDOWS_HEIGHT = GRID_HEIGHT * GRID_BLOCK_SIZE + INFO_PANEL_HEIGHT


    # Paramètres du jeu
    FPS = {
        -2: 0.25,
        -1: 0.5,
        0: 1,
        1: 5,
        2: 20,
        3: float('inf'),
    }

    # Paramètres du serpent
    INITIAL_SNAKE_LENGTH = 3
    SNAKE_COLOR = "yellow" # yellow, orange, blue, purple

    # Paramètres des pommes
    GREEN_APPLE = 2
    RED_APPLE = 1

    # Paramètres de l'agent
    ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']  # Actions possibles
    NUM_ACTIONS = len(ACTIONS)
    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.99
    EXPLORATION_RATE = 1
    EXPLORATION_DECAY = 0.999 # 0.99
    MIN_EXPLORATION = 0
    EPISODES = 100000 # 1000
    REWARDS = {
        "GREEN": 10,
        "RED": -10,
        "DEAD": -20,
        "MOVE": -1
    }


    def display(self):
        """Afficher les paramètres de la configuration"""
        print("\nParamètres de la configuration :")
        for key, value in self.__dict__.items():
            print(f"{key} : {value}")