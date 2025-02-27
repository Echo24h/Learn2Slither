import random
from config import Config


class Snake:

    def __init__(self):

        self.move_count = 0

        self.length = 1 # Longueur initiale du serpent
        self.direction = self.__generate_random_direction()  # Direction initiale du serpent
        self.dir_x, self.dir_y = self.direction
        self.body = self.__generate_random_position()  # Position initiale du serpent

        # Initialiser le serpent avec la longueur donnée
        for _ in range(0, Config.INITIAL_SNAKE_LENGTH.value - 1):
            self.grow()


    def __generate_random_position(self):
        """Générer une position aléatoire pour le serpent en tenant compte de la direction et la longueur"""
        safe_distance = 0
        x = random.randint(safe_distance, Config.GRID_WIDTH.value - 1 - safe_distance)
        y = random.randint(safe_distance, Config.GRID_HEIGHT.value - 1 - safe_distance)
        return [(x,y)]
    
    
    def __generate_random_direction(self):
        """Générer une direction aléatoire pour le serpent"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return random.choice(directions)
    

    def get_direction(self):
        """Retourner la direction du serpent"""
        return self.direction


    def size(self):
        """Retourner la taille du serpent"""
        return self.length
    

    def score(self):
        """Retourner le score du serpent"""
        return self.length - Config.INITIAL_SNAKE_LENGTH.value


    def move(self):
        """Déplacer le serpent dans la direction actuelle"""
        self.move_count += 1
        head_x, head_y = self.body[0]
        self.dir_x, self.dir_y = self.direction
        new_head = (head_x + self.dir_x, head_y + self.dir_y)
        self.body = [new_head] + self.body[:-1]  # Déplacer le serpent


    def grow(self):
        """Faire grandir le serpent"""
        tail_x, tail_y = self.body[-1]
        self.body.append((tail_x, tail_y))  # Ajouter un segment à la fin du serpent
        self.length += 1


    def shrink(self):
        """Faire rétrécir le serpent"""
        if self.length > 1:
            self.body.pop()  # Retirer le dernier segment du serpent
            self.length -= 1


    def change_direction(self, new_direction):
        """Changer la direction du serpent"""
        if new_direction == "UP":
            self.direction = (0, -1)
        elif new_direction == "DOWN":
            self.direction = (0, 1)
        elif new_direction == "LEFT":
            self.direction = (-1, 0)
        elif new_direction == "RIGHT":
            self.direction = (1, 0)


    def get_head(self):
        """Retourner la position de la tête du serpent"""
        return self.body[0]
    

    def get_body(self):
        """Retourner la liste des segments du serpent"""
        return self.body


    def is_dead(self):
        """Vérifier si le serpent est mort"""

        if self.length == 0:
            return "Poison"

        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= Config.GRID_WIDTH.value or head_y < 0 or head_y >= Config.GRID_HEIGHT.value:
            return "Collision with a wall"

        if ((head_x, head_y) in self.body[1:]) and self.move_count > 0:
            return "Collision with yourself"

        return 0 # Le serpent est vivant