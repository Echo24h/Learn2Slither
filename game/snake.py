import pygame
import random
from .settings import BLOCK_SIZE, WIDTH, HEIGHT, INITIAL_SNAKE_LENGTH, SNAKE_COLOR
from .utils import load_sprite


class Snake:

    def __init__(self):

        self.move_count = 0

        # Charger les sprites du serpent
        self.head_sprite = load_sprite('assets/snake_head_' + SNAKE_COLOR + '.png')
        self.body_sprite = load_sprite('assets/snake_body_' + SNAKE_COLOR + '.png')

        self.length = 1 # Longueur initiale du serpent
        self.direction = self.__generate_random_direction()  # Direction initiale du serpent
        self.dir_x, self.dir_y = self.direction
        self.body = self.__generate_random_position()  # Position initiale du serpent

        # Initialiser le serpent avec la longueur donnée
        for _ in range(0, INITIAL_SNAKE_LENGTH - 1):
            self.grow()


    def __generate_random_position(self):
        """Générer une position aléatoire pour le serpent en tenant compte de la direction et la longueur"""
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        return [(x,y)]
    
    
    def __generate_random_direction(self):
        """Générer une direction aléatoire pour le serpent"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return random.choice(directions)
    


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
        if self.length > 0:
            self.body.pop()  # Retirer le dernier segment du serpent
            self.length -= 1


    def change_direction(self, new_direction):
        """Changer la direction du serpent"""
        if new_direction == "UP" and (self.dir_x, self.dir_y) != (0, 1):
            self.direction = (0, -1)
        elif new_direction == "DOWN" and (self.dir_x, self.dir_y) != (0, -1):
            self.direction = (0, 1)
        elif new_direction == "LEFT" and (self.dir_x, self.dir_y)!= (1, 0):
            self.direction = (-1, 0)
        elif new_direction == "RIGHT" and (self.dir_x, self.dir_y) != (-1, 0):
            self.direction = (1, 0)


    def get_head(self):
        """Retourner la position de la tête du serpent"""
        return self.body[0]


    def is_dead(self):
        """Vérifier si le serpent est mort"""

        if self.length == 0:
            return 1 # Mort par longueur nulle

        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return 2 # Mort par collision avec les bords

        if ((head_x, head_y) in self.body[1:]) and self.move_count > 0:
            return 3 # Mort par collision avec soi-même

        return 0 # Le serpent est vivant


    def __get_rotation_angle(self):
        """Retourner l'angle de rotation en fonction de la direction actuelle"""
        if self.direction == (0, -1):  # Haut
            return 0
        elif self.direction == (-1, 0):  # Gauche
            return 90
        elif self.direction == (0, 1):  # Bas
            return 180
        elif self.direction == (1, 0):  # Droite
            return 270


    def draw(self, screen):
        """Dessiner le serpent sur l'écran avec les sprites"""
        for i, segment in enumerate(self.body):
            x, y = segment
            if i == 0:  # Tête
                rotated_head = pygame.transform.rotate(self.head_sprite, self.__get_rotation_angle())
                screen.blit(rotated_head, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            elif self.body[0] != self.body[1]:
                rotated_body = pygame.transform.rotate(self.body_sprite, self.__get_rotation_angle())
                screen.blit(rotated_body, (x * BLOCK_SIZE, y * BLOCK_SIZE))
