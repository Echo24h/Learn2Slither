import pygame
from config import Config
from game import Snake, Food


class Display:
    """
    Class to manage the game display using Pygame.
    It handles rendering the snake, food, score, speed, and coefficients.
    It also manages user input for pausing and adjusting game speed.
    """

    def __init__(self, step_by_step: bool = False):

        pygame.init()

        self.__step_by_step = step_by_step
        self.__step_by_step_update = False

        # Fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 25)

        # Entities
        self.snake_head_sprite = self.__load_sprite(
            'assets/snake_head_' + Config.SNAKE_COLOR.value + '.png'
        )
        self.snake_body_sprite = self.__load_sprite(
            'assets/snake_body_' + Config.SNAKE_COLOR.value + '.png'
        )
        self.red_apple_sprite = self.__load_sprite('assets/red_apple.png')
        self.green_apple_sprite = self.__load_sprite(
            'assets/green_apple.png')

        # Buttons
        self.button_arrow_left_default = self.__load_sprite(
            'assets/button_arrow_left_default.png'
        )
        self.button_arrow_right_default = self.__load_sprite(
            'assets/button_arrow_right_default.png'
        )
        self.button_pause_default = self.__load_sprite(
            'assets/button_pause_default.png'
        )
        self.button_play_default = self.__load_sprite(
            'assets/button_play_default.png'
        )

        self.pause_button_rect = pygame.Rect(
            ((Config.WINDOWS_WIDTH.value - Config.GRID_BLOCK_SIZE.value) /
             2),
            (Config.WINDOWS_HEIGHT.value -
             Config.INFO_PANEL_HEIGHT.value +
             Config.MARGIN.value),
            Config.GRID_BLOCK_SIZE.value,
            Config.GRID_BLOCK_SIZE.value,
        )
        self.play_button_rect = self.pause_button_rect

        self.arrow_left_button_rect = pygame.Rect(
            ((Config.WINDOWS_WIDTH.value - Config.GRID_BLOCK_SIZE.value) /
             2 - Config.GRID_BLOCK_SIZE.value - Config.MARGIN.value),
            (Config.WINDOWS_HEIGHT.value -
             Config.INFO_PANEL_HEIGHT.value +
             Config.MARGIN.value),
            Config.GRID_BLOCK_SIZE.value,
            Config.GRID_BLOCK_SIZE.value,
        )
        self.arrow_right_button_rect = pygame.Rect(
            ((Config.WINDOWS_WIDTH.value - Config.GRID_BLOCK_SIZE.value) /
             2 + Config.GRID_BLOCK_SIZE.value + Config.MARGIN.value),
            (Config.WINDOWS_HEIGHT.value -
             Config.INFO_PANEL_HEIGHT.value +
             Config.MARGIN.value),
            Config.GRID_BLOCK_SIZE.value,
            Config.GRID_BLOCK_SIZE.value,
        )

        # Pygame screen setup
        self.screen = pygame.display.set_mode(
            (Config.WINDOWS_WIDTH.value, Config.WINDOWS_HEIGHT.value))
        pygame.display.set_caption("Learn2Slither")
        self.clock = pygame.time.Clock()
        self.ticks_index = 0
        self.isPause = False

    def __load_sprite(self, path) -> pygame.Surface:
        """
        Load a sprite from an image file and scale it to the grid block size.
        """
        sprite = pygame.image.load(path)
        return pygame.transform.scale(
            sprite, (Config.GRID_BLOCK_SIZE.value,
                     Config.GRID_BLOCK_SIZE.value))

    def __get_snake_sprite_rotation_angle(self, snake: Snake) -> int:
        """Return the rotation angle based on the snake's direction"""
        if snake.get_direction() == (0, -1):  # Up
            return 0
        elif snake.get_direction() == (-1, 0):  # Left
            return 90
        elif snake.get_direction() == (0, 1):  # Down
            return 180
        elif snake.get_direction() == (1, 0):  # Right
            return 270

    def __change_ticks(self, change: int) -> None:
        """Change the game speed"""
        if ((change == -1 and self.ticks_index > -2) or
                (change == 1 and self.ticks_index < 3)):
            self.ticks_index += change

    def __handle_events(self) -> None:
        """Handle game events"""
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and
                     event.key == pygame.K_ESCAPE)):
                self.close()
            # Mouse clicks and keyboard events
            if not self.__step_by_step:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button_rect.collidepoint(event.pos):
                        self.isPause = not self.isPause
                    elif self.arrow_left_button_rect.collidepoint(
                            event.pos):
                        self.__change_ticks(-1)
                    elif self.arrow_right_button_rect.collidepoint(
                            event.pos):
                        self.__change_ticks(1)
                # space key
                elif (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_SPACE):
                    self.isPause = not self.isPause
                # left arrow key
                elif (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_LEFT):
                    self.__change_ticks(-1)
                # right arrow key
                elif (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_RIGHT):
                    self.__change_ticks(1)
            # Step by step mode
            else:
                if (event.type == pygame.KEYDOWN and
                        event.key == pygame.K_SPACE):
                    self.__step_by_step_update = True

    def draw_grid(self) -> None:
        """Draw a checkerboard background on the screen"""

        light_gray = (169, 169, 169)  # Light gray
        dark_gray = (105, 105, 105)   # Dark gray

        for y in range(0, Config.GRID_HEIGHT.value):
            for x in range(0, Config.GRID_WIDTH.value):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(
                        self.screen, light_gray,
                        pygame.Rect(
                            x * Config.GRID_BLOCK_SIZE.value,
                            y * Config.GRID_BLOCK_SIZE.value,
                            Config.GRID_BLOCK_SIZE.value,
                            Config.GRID_BLOCK_SIZE.value))
                else:
                    pygame.draw.rect(
                        self.screen, dark_gray,
                        pygame.Rect(
                            x * Config.GRID_BLOCK_SIZE.value,
                            y * Config.GRID_BLOCK_SIZE.value,
                            Config.GRID_BLOCK_SIZE.value,
                            Config.GRID_BLOCK_SIZE.value))

    def __get_centered_position(self, text_surface, block_x: int,
                                block_y: int) -> tuple[int, int]:
        """Return the centered position of the text in the given block"""
        text_width, text_height = text_surface.get_size()
        x = ((block_x * Config.GRID_BLOCK_SIZE.value) +
             (Config.GRID_BLOCK_SIZE.value - text_width) // 2)

        y = ((block_y * Config.GRID_BLOCK_SIZE.value) +
             (Config.GRID_BLOCK_SIZE.value - text_height) // 2)
        return x, y

    def __get_colored_text(self, coef: float) -> pygame.Surface:
        """Return colored text based on the value
        (red if negative, yellow if neutral, green if positive)"""
        if coef < -5:
            return self.font_style.render(
                f"{coef:.1f}", True, (255, 0, 0))
        elif coef > 5:
            return self.font_style.render(
                f"{coef:.1f}", True, (0, 255, 0))
        else:
            return self.font_style.render(
                f"{coef:.1f}", True, (255, 255, 0))

    def draw_coefs(self, snake_head: tuple[int, int],
                   coefs: dict[str, float]) -> None:
        """Draw the coefficients around the snake's head."""
        up_value = self.__get_colored_text(coefs['UP'])
        down_value = self.__get_colored_text(coefs['DOWN'])
        right_value = self.__get_colored_text(coefs['RIGHT'])
        left_value = self.__get_colored_text(coefs['LEFT'])

        up_pos = self.__get_centered_position(
            up_value, snake_head[0], snake_head[1] - 1)
        down_pos = self.__get_centered_position(
            down_value, snake_head[0], snake_head[1] + 1)
        right_pos = self.__get_centered_position(
            right_value, snake_head[0] + 1, snake_head[1])
        left_pos = self.__get_centered_position(
            left_value, snake_head[0] - 1, snake_head[1])

        self.screen.blit(up_value, up_pos)
        self.screen.blit(down_value, down_pos)
        self.screen.blit(right_value, right_pos)
        self.screen.blit(left_value, left_pos)

    def draw_buttons(self) -> None:
        """Draw the pause and play buttons"""
        # Draw the buttons
        if self.isPause:
            self.screen.blit(
                self.button_play_default, self.pause_button_rect)
        else:
            self.screen.blit(
                self.button_pause_default, self.play_button_rect)
        self.screen.blit(
            self.button_arrow_left_default, self.arrow_left_button_rect)
        self.screen.blit(
            self.button_arrow_right_default, self.arrow_right_button_rect)

    def draw_snake(self, snake: Snake) -> None:
        """Draw the snake on the screen with sprites"""
        snake_body = snake.get_body()
        for i, segment in enumerate(snake_body):
            x, y = segment
            if i == 0:  # Head
                rotated_head = pygame.transform.rotate(
                    self.snake_head_sprite,
                    self.__get_snake_sprite_rotation_angle(snake))
                self.screen.blit(
                    rotated_head,
                    (x * Config.GRID_BLOCK_SIZE.value,
                     y * Config.GRID_BLOCK_SIZE.value))
            elif snake_body[0] != snake_body[1]:
                rotated_body = pygame.transform.rotate(
                    self.snake_body_sprite,
                    self.__get_snake_sprite_rotation_angle(snake))
                self.screen.blit(
                    rotated_body,
                    (x * Config.GRID_BLOCK_SIZE.value,
                     y * Config.GRID_BLOCK_SIZE.value))

    def draw_food(self, food: Food) -> None:
        """Draw the apples on the screen."""
        for food in food.get_food_list():
            position = food["position"]
            sprite = (
                self.green_apple_sprite if food["type"] == "green"
                else self.red_apple_sprite
            )
            x, y = position
            self.screen.blit(
                sprite, (x * Config.GRID_BLOCK_SIZE.value,
                         y * Config.GRID_BLOCK_SIZE.value))

    def draw_score(self, score: int) -> None:
        """Display the score on the screen"""
        value = self.font_style.render(
            f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(
            value, [Config.MARGIN.value, Config.MARGIN.value])

    def draw_speed(self) -> None:
        """Display the game speed on the screen"""
        value = self.font_style.render(
            f"Speed: x{Config.FPS.value[self.ticks_index]}",
            True, (255, 255, 255))
        self.screen.blit(
            value, [Config.MARGIN.value,
                    Config.WINDOWS_HEIGHT.value -
                    Config.INFO_PANEL_HEIGHT.value +
                    Config.MARGIN.value])

    def update_display(self, snake: Snake, food: Food,
                       coefs: dict[str, float]) -> bool:
        """Update the screen"""
        self.__handle_events()
        if not self.isPause:
            self.screen.fill((30, 30, 30))
            self.draw_grid()
            self.draw_snake(snake)
            self.draw_food(food)
            self.draw_score(snake.score())
            self.draw_speed()
            self.draw_coefs(snake.get_head(), coefs)
        self.draw_buttons()
        pygame.display.flip()

        if self.__step_by_step:
            self.__step_by_step_update = False
            while not self.__step_by_step_update:
                self.__handle_events()
        else:
            self.clock.tick(Config.FPS.value[self.ticks_index])
            return self.isPause

    def close(self) -> None:
        """Close the game window"""
        pygame.quit()
        quit()
