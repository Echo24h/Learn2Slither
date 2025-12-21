import random
from config import Config


class Food:
    """
    Class to manage the food (apples) in the Snake game.
    There are two types of apples: green and red.
    Green apples make the snake grow, while red apples make it shrink.
    """

    def __init__(self, snake_body: list):

        self.food_list = self.__generate_initial_food(snake_body)

    def __generate_initial_food(self, snake_body: list) -> list:
        """Generate the initial positions of the apples."""
        food_list = []
        for _ in range(Config.GREEN_APPLE.value):
            food_list.append(
                {
                    "position": self.__generate_position(
                        food_list, snake_body
                    ),
                    "type": "green"
                }
            )
        for _ in range(Config.RED_APPLE.value):
            food_list.append(
                {
                    "position": self.__generate_position(
                        food_list, snake_body
                    ),
                    "type": "red"
                }
            )
        return food_list

    def __generate_position(
            self, food_list: list, snake_body: list) -> tuple[int, int]:
        """Generate a unique position for an apple."""
        while True:
            position = (
                random.randint(0, Config.GRID_WIDTH.value - 1),
                random.randint(0, Config.GRID_HEIGHT.value - 1)
            )
            # Check if the position is already used
            if (
                not any(food["position"] == position for food in food_list)
                and position not in snake_body
            ):
                return position

    def replace_food(self, food_item: dict, snake_body: list) -> None:
        """Replace an eaten apple with a new apple."""
        food_item["position"] = self.__generate_position(
            self.food_list, snake_body
        )

    def get_food_list(self) -> list:
        """Return the list of apples."""
        return self.food_list
