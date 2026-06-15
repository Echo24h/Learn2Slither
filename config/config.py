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

    # Q-learning parameters (Long-term ~ 20 000 episodes)
    # LEARNING_RATE = 0.1 # Learning rate (alpha)
    # DISCOUNT_FACTOR = 0.999 # Discount factor (gamma)
    # EXPLORATION_RATE = 1 # Initial exploration rate (epsilon)
    # MIN_EXPLORATION = 0.0001 # Final exploration rate after decay
    # EXPLORATION_DECAY = 0.999 # Exploration decay rate per episode
    # VISION_SIZE = 10 # Number of cells the snake can see in each direction
    # REWARDS = {
    #     "GREEN": 10,
    #     "RED": -10,
    #     "DEAD": -20,
    #     "MOVE": -1
    # }

    # Q-learning parameters (Mid-term ~ 1 000 episodes)
    LEARNING_RATE = 0.1
    DISCOUNT_FACTOR = 0.9
    EXPLORATION_RATE = 1
    EXPLORATION_DECAY = 0.99
    MIN_EXPLORATION = 0.01
    VISION_SIZE = 5
    REWARDS = {
        "GREEN": 15,
        "RED": -15,
        "DEAD": -30,
        "MOVE": -1
    }

    # Q-learning parameters (Short-term ~ 100 episodes)
    # LEARNING_RATE = 0.1
    # DISCOUNT_FACTOR = 0.8
    # EXPLORATION_RATE = 1
    # EXPLORATION_DECAY = 0.95
    # MIN_EXPLORATION = 0.01
    # VISION_SIZE = 3
    # REWARDS = {
    #     "GREEN": 20,
    #     "RED": -20,
    #     "DEAD": -50,
    #     "MOVE": -0.5
    # }
