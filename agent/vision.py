"""
Module to manage the vision of the snake.
It provides functions to get and print the vision of the snake.
"""

from config import Config
from game import Food
from game import Snake


def is_food_position(x: int, y: int, food_list: list) -> str | bool:
    """
    Verify if the position is already occupied by a food.

    Parameters:
    - x, y (int): Coordinates of the position
    - food_list (list): List of food items
    Return:
    - "G" if the food is green
    - "R" if the food is red
    - False if the position is empty
    """
    for food in food_list:
        if (x, y) == food["position"]:
            if food["type"] == "green":
                return "G"
            elif food["type"] == "red":
                return "R"
    return False


def get_vision(snake: Snake, food: Food) -> dict[str, list[str]]:
    """
    Return the vision of the snake.

    Parameters:
    - snake (Snake): Instance of the snake
    - food (Food): Instance of the food
    Return:
    - vision (dict): Dictionary of directions with visible elements

    Vision example:

    {
        'UP': ['0', 'W'],
        'DOWN': ['S', '0', '0', '0', '0', '0', '0', '0', 'W'],
        'LEFT': ['0', 'W'],
        'RIGHT': ['0', '0', '0', '0', '0', '0', '0', '0', 'W']
    }

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

    for dir, (dx, dy) in direction.items():
        x, y = head_x, head_y
        while True:
            x += dx
            y += dy
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


# TODO: This function can be improved for performance if needed
def get_preprocess_vision(snake: Snake, food: Food) -> dict[str, str]:
    """
    Return the preprocessed vision of the snake.

    Parameters:
    - snake (Snake): Instance of the snake
    - food (Food): Instance of the food
    Return:
    - preprocess_vision (dict): Dictionary of directions with visible elements

    Vision example:

    {
        'UP': 'OW',
        'DOWN': 'S0W',
        'LEFT': '0W',
        'RIGHT': '00000000W'
    }
    """
    vision = get_vision(snake, food)
    preprocess_vision = {}

    for dir, values in vision.items():
        preprocess_vision[dir] = "".join(values)
    return preprocess_vision


def print_vision(snake: Snake, food: Food) -> None:
    """
    Print the current vision of the snake in the console.

    Parameters:
    - snake (Snake): Instance of the snake
    - food (Food): Instance of the food
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

    while y < Config.GRID_HEIGHT.value + 1:
        while x < Config.GRID_WIDTH.value + 1:
            if x == x_head or y == y_head:
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
