import pygame
from game.snake import Snake
from game.food import Food
from game.settings import BLOCK_SIZE, WIDTH, HEIGHT, SPEED
from game.utils import draw_background

# Terminer le jeu
def end_game(is_dead):
    print(f"Game Over! You're dead! Reason: {is_dead}")
    pygame.quit()
    quit()

# Gérer les événements du jeu
def event_handler(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT \
        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

# Boucle principale du jeu
def game_loop(screen, snake, food, game_start):

    event_handler(snake)

    if game_start:
        snake.move()

    # Vérifier si le serpent a mangé une pomme
    for item in food.get_food_list():
        if snake.get_head() == item["position"]:
            if item["type"] == "green":
                snake.grow()
            elif item["type"] == "red":
                snake.shrink()
            food.replace_food(item)

    # Vérifier si le serpent est mort
    is_dead = snake.is_dead()
    if is_dead != False:
        end_game(is_dead)

    # Dessiner les éléments du jeu
    draw_background(screen)
    snake.draw(screen)
    food.draw(screen)


def main():
    pygame.init()  # Initialisation ici avant d'utiliser Pygame

    screen = pygame.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Learn2Slither")

    snake = Snake()
    food = Food()

    game_start = False

    while True:
        clock = pygame.time.Clock()
        game_loop(screen, snake, food, game_start)
        pygame.display.update()
        clock.tick(SPEED)
        game_start = True


if __name__ == "__main__":
    main()