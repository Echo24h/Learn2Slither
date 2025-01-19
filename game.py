import pygame
from game.snake import Snake
from game.food import Food
from game.settings import BLOCK_SIZE, WIDTH, HEIGHT, SPEED
from game.utils import draw_background

# Terminer le jeu
def end_game(reason):
    print(f"Game Over! Reason: {reason}")
    pygame.quit()
    quit()

# Gérer les événements du jeu
def event_handler(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT \
        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            end_game("Exited")
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
def game_loop(screen, snake, food):

    event_handler(snake)

    snake.move()

    # Vérifier si le serpent a mangé une pomme
    for item in food.get_food_list():
        if snake.get_head() == item["position"]:
            if item["type"] == "green":
                snake.grow()
            elif item["type"] == "red":
                snake.shrink()
            food.replace_food(item)

    if (reason := snake.is_dead()):
        end_game(reason)

    # Dessiner les éléments du jeu
    draw_background(screen)
    snake.draw(screen)
    food.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE))
    pygame.display.set_caption("Learn2Slither")

    snake = Snake()
    food = Food()

    clock = pygame.time.Clock()

    while True:
        game_loop(screen, snake, food)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()