import random
from config import Config


class Food:

    def __init__(self, snake_body: list):

        self.food_list = self.__generate_initial_food(snake_body)


    def __generate_initial_food(self, snake_body: list):
        """Générer les positions initiales des pommes."""
        food_list = []
        for _ in range(Config.GREEN_APPLE.value):
            food_list.append({"position": self.__generate_position(food_list, snake_body), "type": "green"})
        for _ in range(Config.RED_APPLE.value):
            food_list.append({"position": self.__generate_position(food_list, snake_body), "type": "red"})
        return food_list


    def __generate_position(self, food_list, snake_body: list):
        """Générer une position unique pour une pomme."""
        while True:
            position = (
                random.randint(0, Config.GRID_WIDTH.value - 1),
                random.randint(0, Config.GRID_HEIGHT.value - 1)
            )
            # Vérifier si la position est déjà utilisée
            if not any(food["position"] == position for food in food_list) and position not in snake_body:
                return position


    def replace_food(self, food_item, snake_body: list):
        """Remplacer une pomme mangée par une nouvelle pomme."""
        food_item["position"] = self.__generate_position(self.food_list, snake_body)


    def get_food_list(self):
        """Retourner la liste des pommes."""
        return self.food_list