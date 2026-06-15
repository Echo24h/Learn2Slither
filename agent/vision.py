"""Module to manage the vision of the snake.

Provides functions to get and process the snake's vision, which is used
by the Q-learning agent to make decisions.
"""

from config import Config
from game import Food
from game import Snake


def is_food_position(x: int, y: int, food_list: list) -> str | bool:
    """Verify if a position contains food.

    Args:
        x: X coordinate
        y: Y coordinate
        food_list: List of food items

    Returns:
        "G" if green food, "R" if red food, False if empty
    """
    for food in food_list:
        if (x, y) == food["position"]:
            if food["type"] == "green":
                return "G"
            elif food["type"] == "red":
                return "R"
    return False


def get_vision(
        snake: Snake, food: Food, vision_size: int) -> dict[str, list[str]]:
    """Return the vision of the snake in all four directions.

    Args:
        snake: Snake instance
        food: Food instance
        vision_size: Number of cells the snake can see in each direction

    Returns:
        Dictionary mapping directions to lists of visible elements

    Example:
        {
            'UP': ['0', 'W'],
            'DOWN': ['S', '0', '0', '0', '0', '0', '0', '0', 'W'],
            'LEFT': ['0', 'W'],
            'RIGHT': ['0', '0', '0', '0', '0', '0', '0', '0', 'W']
        }

    Legend:
        H: Head of the snake
        S: Body of the snake
        G: Green apple
        R: Red apple
        W: Wall
        0: Empty space
    """
    vision = {"UP": [], "DOWN": [], "LEFT": [], "RIGHT": []}

    direction = {"UP": (0, -1), "DOWN": (0, 1),
                 "LEFT": (-1, 0), "RIGHT": (1, 0)}

    head_x, head_y = snake.get_head()
    body = snake.get_body()
    food_list = food.get_food_list()

    max_distance = vision_size

    for dir, (dx, dy) in direction.items():
        x, y = head_x, head_y
        distance = 0
        while distance < max_distance:
            x += dx
            y += dy
            distance += 1
            if (x < 0 or x >= Config.GRID_WIDTH.value or
                    y < 0 or y >= Config.GRID_HEIGHT.value):
                vision[dir].append('W')
                break
            food_type = is_food_position(x, y, food_list)
            if food_type is not False:
                vision[dir].append(food_type)
            elif (x, y) in body:
                vision[dir].append('S')
            else:
                vision[dir].append('0')
    return vision


def get_preprocess_vision(
        snake: Snake, food: Food, vision_size: int) -> dict[str, str]:
    """Return the preprocessed (flattened) vision of the snake.

    Args:
        snake: Snake instance
        food: Food instance
        vision_size: Number of cells the snake can see in each direction

    Returns:
        Dictionary mapping directions to concatenated vision strings

    Example:
        {
            'UP': 'OW',
            'DOWN': 'S0W',
            'LEFT': '0W',
            'RIGHT': '00000000W'
        }
    """
    vision = get_vision(snake, food, vision_size)
    return {direction: "".join(values) for direction, values in vision.items()}


def remove_rear_vision(snake: Snake, vision: dict[str, str]) -> dict[str, str]:
    """Remove the rear vision of the snake based on its current direction.

    Args:
        snake: Snake instance
        vision: Dictionary of the snake's vision

    Returns:
        Updated vision dictionary with rear direction removed
    """
    current_direction = snake.get_direction()
    if current_direction == (0, -1):  # UP
        del vision["DOWN"]
    elif current_direction == (0, 1):  # DOWN
        del vision["UP"]
    elif current_direction == (-1, 0):  # LEFT
        del vision["RIGHT"]
    elif current_direction == (1, 0):  # RIGHT
        del vision["LEFT"]
    return vision


def print_vision(snake: Snake, food: Food, vision_size: int) -> None:
    """
    Print the current vision of the snake in the console.

    Parameters:
    - snake (Snake): Instance of the snake
    - food (Food): Instance of the food
    - vision_size (int): Number of cells the snake can see in each direction

    Return:
    - None

    Print example:

    "                           W
                                0
                                0
      W 0 0 0 0 0 0 0 0 0 0 0 0 H S 0 0 0 0 0 0 W
                                0
                                0
                                0
                                0
                                0
                                0
                                0
                                W                 "

    H: Head of the snake
    S: Body of the snake
    G: Green apple
    R: Red apple
    W: Wall
    0: Empty space
    """
    x = -1
    y = -1
    x_head, y_head = snake.get_head()
    snake_body = snake.get_body()
    food_list = food.get_food_list()
    max_distance = vision_size

    while y < Config.GRID_HEIGHT.value + 1:
        while x < Config.GRID_WIDTH.value + 1:
            if (x == x_head or y == y_head) \
                and abs(x - x_head) <= max_distance \
                    and abs(y - y_head) <= max_distance:
                if (x == -1 or x == Config.GRID_WIDTH.value or
                        y == -1 or y == Config.GRID_HEIGHT.value):
                    print("W", end=" ")
                elif (x, y) == (x_head, y_head):
                    print("H", end=" ")
                elif (x, y) in snake_body:
                    print("S", end=" ")
                elif is_food_position(x, y, food_list) == "G":
                    print("G", end=" ")
                elif is_food_position(x, y, food_list) == "R":
                    print("R", end=" ")
                else:
                    print("0", end=" ")
            else:
                print(" ", end=" ")
            x += 1
        y += 1
        x = -1
        print("")
