import random
from config import Config


class Snake:
    """
    Class to manage the snake in the Snake game.
    It handles the snake's movement, growth, shrinking,
    and collision detection.
    """

    def __init__(self):

        self.move_count = 0

        # Initial length of the snake
        self.length = 1
        # Initial random direction and position
        self.direction = self.__generate_random_direction()
        self.dir_x, self.dir_y = self.direction
        self.body = self.__generate_random_position()

        # Initialize the snake with the given length
        for _ in range(0, Config.INITIAL_SNAKE_LENGTH.value - 1):
            self.grow()

    def __generate_random_position(self) -> list[tuple[int, int]]:
        """Generate a random starting position for the snake."""
        safe_distance = 0
        x = random.randint(
            safe_distance, Config.GRID_WIDTH.value - 1 - safe_distance
        )
        y = random.randint(
            safe_distance, Config.GRID_HEIGHT.value - 1 - safe_distance
        )
        return [(x, y)]

    def __generate_random_direction(self) -> tuple[int, int]:
        """Generate a random direction for the snake"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return random.choice(directions)

    def get_direction(self) -> tuple[int, int]:
        """Return the direction of the snake"""
        return self.direction

    def size(self) -> int:
        """Return the size of the snake"""
        return self.length

    def score(self) -> int:
        """Return the score of the snake"""
        return self.length - Config.INITIAL_SNAKE_LENGTH.value

    def move(self) -> None:
        """Move the snake in the current direction"""
        self.move_count += 1
        head_x, head_y = self.body[0]
        self.dir_x, self.dir_y = self.direction
        new_head = (head_x + self.dir_x, head_y + self.dir_y)
        self.body = [new_head] + self.body[:-1]  # Move the snake

    def grow(self) -> None:
        """Make the snake grow"""
        tail_x, tail_y = self.body[-1]
        self.body.append((tail_x, tail_y))  # Add a new segment at the tail
        self.length += 1

    def shrink(self) -> None:
        """Make the snake shrink"""
        if self.length > 1:
            self.body.pop()  # Remove the last segment of the snake
            self.length -= 1

    def change_direction(self, new_direction: str) -> None:
        """Change the direction of the snake."""
        direction_map = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0)
        }
        self.direction = direction_map.get(new_direction, self.direction)

    def get_head(self) -> tuple[int, int]:
        """Return the position of the snake's head"""
        return self.body[0]

    def get_body(self) -> list[tuple[int, int]]:
        """Return the list of the snake's segments"""
        return self.body

    def is_dead(self) -> str | None:
        """Check if the snake is dead.

        Returns:
            str: Reason of death ("Poison", "Collision with a wall",
                 "Collision with yourself")
            None: If the snake is alive
        """

        if self.length == 0:
            return "Poison"

        head_x, head_y = self.body[0]
        if (
            head_x < 0
            or head_x >= Config.GRID_WIDTH.value
            or head_y < 0
            or head_y >= Config.GRID_HEIGHT.value
        ):
            return "Collision with a wall"

        if ((head_x, head_y) in self.body[1:]) and self.move_count > 0:
            return "Collision with yourself"

        return None  # The snake is alive
