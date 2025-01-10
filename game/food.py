import random
from .utils import load_sprite
from .settings import BLOCK_SIZE, WIDTH, HEIGHT, GREEN_APPLE, RED_APPLE

class Food:
    def __init__(self):

        self.food_list = self.__generate_initial_food()

        # Charger les sprites des pommes
        self.red_apple_sprite = load_sprite('assets/red_apple.png')
        self.green_apple_sprite = load_sprite('assets/green_apple.png')


    def __generate_initial_food(self):
        """Générer les positions initiales des pommes."""
        food_list = []
        for _ in range(GREEN_APPLE):
            food_list.append({"position": self.__generate_position(food_list), "type": "green"})
        for _ in range(RED_APPLE):
            food_list.append({"position": self.__generate_position(food_list), "type": "red"})
        return food_list


    def __generate_position(self, food_list):
        """Générer une position unique pour une pomme."""
        while True:
            position = (
                random.randint(0, WIDTH - 1),
                random.randint(0, HEIGHT - 1)
            )
            # Vérifier si la position est déjà utilisée
            if not any(food["position"] == position for food in food_list):
                return position


    def replace_food(self, food_item):
        """Remplacer une pomme mangée par une nouvelle pomme."""
        food_item["position"] = self.__generate_position(self.food_list)


    def draw(self, screen):
        """Dessiner les pommes sur l'écran."""
        for food in self.food_list:
            position = food["position"]
            sprite = (
                self.green_apple_sprite if food["type"] == "green" else self.red_apple_sprite
            )
            x, y = position
            screen.blit(sprite, (x * BLOCK_SIZE, y * BLOCK_SIZE))


    def get_food_list(self):
        """Retourner la liste des pommes."""
        return self.food_list