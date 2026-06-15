from enum import Enum


class Config(Enum):
    """
    Configuration parameters for the Snake game and the learning agent.
    """

    # Window parameters
    GRID_BLOCK_SIZE = 64
    GRID_WIDTH = 10
    GRID_HEIGHT = 10
    MARGIN = 10
    INFO_PANEL_HEIGHT = GRID_BLOCK_SIZE + (MARGIN * 2)
    WINDOWS_WIDTH = GRID_WIDTH * GRID_BLOCK_SIZE
    WINDOWS_HEIGHT = GRID_HEIGHT * GRID_BLOCK_SIZE + INFO_PANEL_HEIGHT

    # Game parameters
    FPS = {
        -2: 0.25,
        -1: 0.5,
        0: 1,
        1: 5,
        2: 20,
        3: float('inf'),
    }

    # Snake parameters
    INITIAL_SNAKE_LENGTH = 3
    SNAKE_COLOR = "yellow"  # yellow, orange, blue, purple

    # Apple parameters
    GREEN_APPLE = 2
    RED_APPLE = 1


    # Agent parameters 
    ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']  # Possible actions
    NUM_ACTIONS = len(ACTIONS)
    EPISODES = 1  # 1000


    # Q-learning parameters (Long-term)
    # LEARNING_RATE = 0.1
    # DISCOUNT_FACTOR = 0.99
    # EXPLORATION_RATE = 1
    # MIN_EXPLORATION = 0.01 # Final exploration rate after decay
    # EXPLORATION_DECAY = 0.999  # 0.99
    # VISION_SIZE = 10 # Size of the vision grid (e.g., 3 for a 3x3 grid around the snake's head)
    # REWARDS = {
    #     "GREEN": 10,
    #     "RED": -10,
    #     "DEAD": -20,
    #     "MOVE": -1
    # }

    # Q-learning parameters (Short-term)
    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.9
    EXPLORATION_RATE = 1
    EXPLORATION_DECAY = 0.99
    MIN_EXPLORATION = 0.01  # Final exploration rate after decay
    VISION_SIZE = 5  # Size of the vision grid (e.g., 3 for a 3x3 grid around the snake's head)
    REWARDS = {
        "GREEN": 50,
        "RED": -50,
        "DEAD": -50,
        "MOVE": -1
    }


    def display(self) -> None:
        """Display the configuration parameters"""
        print("\nConfiguration parameters:")
        for key, value in self.__dict__.items():
            print(f"{key} : {value}")
