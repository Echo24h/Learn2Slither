import time

import pyglet
from pyglet import shapes
from pyglet.window import key, mouse

from config import Config
from game import Snake, Food


class Display:
    """
    Class to manage the game display using pyglet.
    It handles rendering the snake, food, score, speed, and coefficients.
    It also manages user input for pausing and adjusting game speed.
    """

    def __init__(self, step_by_step: bool = False):
        self.__step_by_step = step_by_step
        self.__step_by_step_update = False
        self.__is_closed = False

        self.window = pyglet.window.Window(
            width=Config.WINDOWS_WIDTH.value,
            height=Config.WINDOWS_HEIGHT.value,
            caption="Learn2Slither",
            resizable=False
        )
        self.window.push_handlers(self)

        self.__last_frame_time = time.perf_counter()
        self.ticks_index = 0
        self.isPause = False

        self.font_name = "Bahnschrift"
        self.font_size = 25

        self.snake_head_texture = self.__load_texture(
            'assets/snake_head_' + Config.SNAKE_COLOR.value + '.png'
        )
        self.snake_body_texture = self.__load_texture(
            'assets/snake_body_' + Config.SNAKE_COLOR.value + '.png'
        )
        self.red_apple_texture = self.__load_texture('assets/red_apple.png')
        self.green_apple_texture = self.__load_texture('assets/green_apple.png')

        self.button_arrow_left_default = self.__load_texture(
            'assets/button_arrow_left_default.png'
        )
        self.button_arrow_right_default = self.__load_texture(
            'assets/button_arrow_right_default.png'
        )
        self.button_pause_default = self.__load_texture(
            'assets/button_pause_default.png'
        )
        self.button_play_default = self.__load_texture(
            'assets/button_play_default.png'
        )

        self.pause_button_rect = (
            (Config.WINDOWS_WIDTH.value - Config.GRID_BLOCK_SIZE.value) / 2,
            Config.MARGIN.value,
            Config.GRID_BLOCK_SIZE.value,
            Config.GRID_BLOCK_SIZE.value,
        )
        # Alias explicite : meme zone que pause_button_rect, le bouton
        # play est dessine au meme endroit que le bouton pause.
        self.play_button_rect = self.pause_button_rect

        self.arrow_left_button_rect = (
            (Config.WINDOWS_WIDTH.value - Config.GRID_BLOCK_SIZE.value) / 2 -
            Config.GRID_BLOCK_SIZE.value - Config.MARGIN.value,
            Config.MARGIN.value,
            Config.GRID_BLOCK_SIZE.value,
            Config.GRID_BLOCK_SIZE.value,
        )
        self.arrow_right_button_rect = (
            (Config.WINDOWS_WIDTH.value - Config.GRID_BLOCK_SIZE.value) / 2 +
            Config.GRID_BLOCK_SIZE.value + Config.MARGIN.value,
            Config.MARGIN.value,
            Config.GRID_BLOCK_SIZE.value,
            Config.GRID_BLOCK_SIZE.value,
        )

    def __load_texture(self, path):
        texture = pyglet.image.load(path).get_texture()
        if texture.width == 0 or texture.height == 0:
            raise ValueError(f"Invalid texture loaded from {path!r}: "
                             f"size is {texture.width}x{texture.height}")
        texture.anchor_x = texture.width // 2
        texture.anchor_y = texture.height // 2
        return texture

    def __logical_y(self, grid_y: int) -> float:
        return (Config.INFO_PANEL_HEIGHT.value +
                (Config.GRID_HEIGHT.value - grid_y - 1) *
                Config.GRID_BLOCK_SIZE.value)

    def __create_sprite(self, texture, grid_x: int, grid_y: int,
                        rotation: float = 0.0):
        sprite = pyglet.sprite.Sprite(
            texture,
            x=grid_x * Config.GRID_BLOCK_SIZE.value +
              Config.GRID_BLOCK_SIZE.value / 2,
            y=self.__logical_y(grid_y) + Config.GRID_BLOCK_SIZE.value / 2
        )
        sprite.scale = Config.GRID_BLOCK_SIZE.value / texture.width
        sprite.rotation = rotation
        return sprite

    def __rect_contains(self, rect, x: int, y: int) -> bool:
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh

    def on_close(self):
        self.close()
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.close()
        elif symbol == key.SPACE:
            if self.__step_by_step:
                self.__step_by_step_update = True
            else:
                self.isPause = not self.isPause
                self.__last_frame_time = time.perf_counter()
        elif symbol == key.LEFT:
            self.__change_ticks(-1)
        elif symbol == key.RIGHT:
            self.__change_ticks(1)

    def on_mouse_press(self, x, y, button, modifiers):
        if button != mouse.LEFT:
            return
        if self.__rect_contains(self.pause_button_rect, x, y):
            if self.__step_by_step:
                self.__step_by_step_update = True
            else:
                self.isPause = not self.isPause
                self.__last_frame_time = time.perf_counter()
        elif self.__step_by_step:
            # En mode pas-a-pas, seul le bouton pause/play est actif :
            # les fleches de vitesse n'ont pas de sens ici.
            return
        elif self.__rect_contains(self.arrow_left_button_rect, x, y):
            self.__change_ticks(-1)
        elif self.__rect_contains(self.arrow_right_button_rect, x, y):
            self.__change_ticks(1)

    def __get_snake_sprite_rotation_angle(self, snake: Snake) -> int:
        direction_angles = {
            (0, -1): 0,
            (1, 0): 90,
            (0, 1): 180,
            (-1, 0): 270
        }
        return direction_angles.get(snake.get_direction(), 0)

    def __change_ticks(self, change: int) -> None:
        # ticks_index doit rester une clé valide dans Config.FPS.value.
        min_index = min(Config.FPS.value)
        max_index = max(Config.FPS.value)
        new_index = self.ticks_index + change
        if min_index <= new_index <= max_index:
            self.ticks_index = new_index
            # Repartir d'un timing propre : evite le decalage d'1 frame
            # du au "elapsed" calcule sur l'ancienne vitesse.
            self.__last_frame_time = time.perf_counter()

    def __handle_events(self) -> None:
        if self.__is_closed:
            raise RuntimeError("Game display closed")
        self.window.dispatch_events()

    def draw_grid(self) -> None:
        LIGHT_GRAY = (169, 169, 169)
        DARK_GRAY = (105, 105, 105)
        size = Config.GRID_BLOCK_SIZE.value

        for y in range(Config.GRID_HEIGHT.value):
            for x in range(Config.GRID_WIDTH.value):
                color = LIGHT_GRAY if (x + y) % 2 == 0 else DARK_GRAY
                rectangle = shapes.Rectangle(
                    x * size,
                    self.__logical_y(y),
                    size,
                    size,
                    color=color
                )
                rectangle.draw()

    def __get_centered_position(self, text_label, block_x: int,
                                block_y: int) -> tuple[float, float]:
        text_width = text_label.content_width
        text_height = text_label.content_height
        x = (block_x * Config.GRID_BLOCK_SIZE.value +
             (Config.GRID_BLOCK_SIZE.value - text_width) / 2)
        y = (self.__logical_y(block_y) +
             (Config.GRID_BLOCK_SIZE.value - text_height) / 2)
        return x, y

    def __get_colored_text(self, coef: float) -> pyglet.text.Label:
        if coef < -5:
            color = (255, 0, 0, 255)
        elif coef > 5:
            color = (0, 255, 0, 255)
        else:
            color = (255, 255, 0, 255)

        return pyglet.text.Label(
            f"{coef:.1f}",
            font_name=self.font_name,
            font_size=self.font_size,
            x=0,
            y=0,
            color=color,
            anchor_x='left',
            anchor_y='baseline'
        )

    def draw_coefs(self, snake_head: tuple[int, int],
                   coefs: dict[str, float]) -> None:
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

        up_value.x, up_value.y = up_pos
        down_value.x, down_value.y = down_pos
        right_value.x, right_value.y = right_pos
        left_value.x, left_value.y = left_pos

        # Ne dessiner que les coefficients qui restent dans la grille
        # de jeu, pour ne pas deborder sur le panneau d'info ou hors fenetre.
        if snake_head[1] - 1 >= 0:
            up_value.draw()
        if snake_head[1] + 1 < Config.GRID_HEIGHT.value:
            down_value.draw()
        if snake_head[0] + 1 < Config.GRID_WIDTH.value:
            right_value.draw()
        if snake_head[0] - 1 >= 0:
            left_value.draw()

    def draw_buttons(self) -> None:

        if self.__step_by_step:
            texture = self.button_play_default
            step_sprite = pyglet.sprite.Sprite(
                texture,
                x=self.pause_button_rect[0] + Config.GRID_BLOCK_SIZE.value / 2,
                y=self.pause_button_rect[1] + Config.GRID_BLOCK_SIZE.value / 2
            )
            step_sprite.scale = Config.GRID_BLOCK_SIZE.value / texture.width
            step_sprite.draw()
            return  # In step-by-step mode, only the play button is drawn.        

        if self.isPause:
            texture = self.button_play_default
        else:
            texture = self.button_pause_default

        pause_sprite = pyglet.sprite.Sprite(
            texture,
            x=self.pause_button_rect[0] + Config.GRID_BLOCK_SIZE.value / 2,
            y=self.pause_button_rect[1] + Config.GRID_BLOCK_SIZE.value / 2
        )
        pause_sprite.scale = Config.GRID_BLOCK_SIZE.value / texture.width
        pause_sprite.draw()

        left_sprite = pyglet.sprite.Sprite(
            self.button_arrow_left_default,
            x=self.arrow_left_button_rect[0] + Config.GRID_BLOCK_SIZE.value / 2,
            y=self.arrow_left_button_rect[1] + Config.GRID_BLOCK_SIZE.value / 2
        )
        left_sprite.scale = Config.GRID_BLOCK_SIZE.value / self.button_arrow_left_default.width
        left_sprite.draw()

        right_sprite = pyglet.sprite.Sprite(
            self.button_arrow_right_default,
            x=self.arrow_right_button_rect[0] + Config.GRID_BLOCK_SIZE.value / 2,
            y=self.arrow_right_button_rect[1] + Config.GRID_BLOCK_SIZE.value / 2
        )
        right_sprite.scale = Config.GRID_BLOCK_SIZE.value / self.button_arrow_right_default.width
        right_sprite.draw()

    def draw_snake(self, snake: Snake) -> None:
        snake_body = snake.get_body()
        for i, segment in enumerate(snake_body):
            x, y = segment
            if i == 0:
                head_sprite = self.__create_sprite(
                    self.snake_head_texture,
                    x,
                    y,
                    rotation=self.__get_snake_sprite_rotation_angle(snake)
                )
                head_sprite.draw()
            elif snake_body[0] != snake_body[1]:
                body_sprite = self.__create_sprite(
                    self.snake_body_texture,
                    x,
                    y,
                    rotation=self.__get_snake_sprite_rotation_angle(snake)
                )
                body_sprite.draw()

    def draw_food(self, food: Food) -> None:
        for item in food.get_food_list():
            texture = (
                self.green_apple_texture
                if item['type'] == 'green'
                else self.red_apple_texture
            )
            x, y = item['position']
            food_sprite = self.__create_sprite(texture, x, y)
            food_sprite.draw()

    def draw_score(self, score: int) -> None:
        value = pyglet.text.Label(
            f"Score: {score}",
            font_name=self.font_name,
            font_size=self.font_size,
            x=Config.MARGIN.value,
            y=Config.MARGIN.value,
            color=(255, 255, 255, 255),
            anchor_x='left',
            anchor_y='bottom'
        )
        value.draw()

    def draw_speed(self) -> None:
        value = pyglet.text.Label(
            f"Speed: x{Config.FPS.value[self.ticks_index]}",
            font_name=self.font_name,
            font_size=self.font_size,
            x=Config.WINDOWS_WIDTH.value - Config.MARGIN.value,
            y=Config.MARGIN.value,
            color=(255, 255, 255, 255),
            anchor_x='right',
            anchor_y='bottom'
        )
        value.draw()

    def update_display(self, snake: Snake, food: Food,
                       coefs: dict[str, float]) -> bool:
        self.__handle_events()
        if self.isPause:
            self.window.clear()
            self.draw_grid()
            self.draw_snake(snake)
            self.draw_food(food)
            self.draw_coefs(snake.get_head(), coefs)
            self.draw_score(snake.score())
            self.draw_speed()
            self.draw_buttons()
            self.window.flip()
            return self.isPause

        self.window.clear()
        self.draw_grid()
        self.draw_snake(snake)
        self.draw_food(food)
        self.draw_score(snake.score())
        self.draw_speed()
        self.draw_coefs(snake.get_head(), coefs)
        self.draw_buttons()
        self.window.flip()

        if self.__step_by_step:
            self.__step_by_step_update = False
            while not self.__step_by_step_update:
                self.__handle_events()
        else:
            target_fps = Config.FPS.value[self.ticks_index]
            if target_fps != float('inf'):
                now = time.perf_counter()
                elapsed = now - self.__last_frame_time
                delay = max(0, 1 / target_fps - elapsed)
                if delay > 0:
                    time.sleep(delay)
                self.__last_frame_time = time.perf_counter()
        return self.isPause

    def close(self) -> None:
        if not self.__is_closed:
            self.__is_closed = True
            self.window.close()