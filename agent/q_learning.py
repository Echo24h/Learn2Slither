import random
import numpy as np

from config import Config
from game import Snake, Food, Display
from .q_data import QData
from .vision import get_preprocess_vision
from .training_stats import TrainingStats


class QLearning:
    """
    Q-Learning agent for the Snake game.
    """

    def __init__(self, visual: bool = True,
                 episodes: int = Config.EPISODES.value,
                 step_by_step: bool = False,
                 learn: bool = True) -> None:

        # Initialize Q-data
        self.__q_data = QData()
        self.__episodes = episodes
        self.__visual = visual
        self.__step_by_step = step_by_step
        self.__learn = learn

        # Statistics tracking
        self.__stats = TrainingStats()

    def __check_vision(self, vision: dict[str, str]) -> None:
        """Ensure all states in vision are initialized in the Q-table."""
        for direction, state in vision.items():
            if state not in self.__q_data.q_table:
                self.__q_data.q_table[state] = 0

    def __get_coefs(self, vision: dict[str, str]) -> dict[str, float]:
        return {direction: self.__q_data.q_table[state]
                for direction, state in vision.items()}

    def __choose_action(self, vision: dict[str, str]) -> str:
        """Choose the best action based on the Q-table or explore randomly."""
        self.__check_vision(vision)

        if random.random() < self.__q_data.exploration_rate:
            return Config.ACTIONS.value[random.choice(
                range(Config.NUM_ACTIONS.value))]
        else:
            # Choose randomly if multiple actions have the same Q-value
            max_q = max(self.__q_data.q_table[state]
                        for state in vision.values())
            best_actions = [direction for direction, state in vision.items()
                            if self.__q_data.q_table[state] == max_q]
            return random.choice(best_actions)

    def __check_food_eaten(self, snake: Snake, food: Food) -> int:
        """Check if the snake has eaten food and return the reward."""
        reward = Config.REWARDS.value["MOVE"]
        for item in food.get_food_list():
            if snake.get_head() == item["position"]:
                if item["type"] == "green":
                    snake.grow()
                    reward = Config.REWARDS.value["GREEN"]
                elif item["type"] == "red":
                    snake.shrink()
                    reward = Config.REWARDS.value["RED"]
                food.replace_food(item, snake.get_body())
                break
        return reward

    def __step(self, action: str, snake: Snake,
               food: Food) -> tuple[int, bool]:
        """Execute one step and return reward and done status."""
        snake.change_direction(action)
        snake.move()

        if snake.is_dead() is not None:
            reward = Config.REWARDS.value["DEAD"]
            done = True
        else:
            reward = self.__check_food_eaten(snake, food)
            done = False

        return reward, done

    def __update_q_table(self, state: str, next_vision: dict[str, str],
                         reward: int) -> None:
        """Update Q-table using the Q-learning formula."""
        gamma = self.__q_data.discount_factor
        alpha = self.__q_data.learning_rate
        max_next_Q = np.max(
            [self.__q_data.q_table[value]
             for _, value in next_vision.items()])

        self.__q_data.q_table[state] = (
            self.__q_data.q_table[state] + alpha *
            (reward + gamma * (max_next_Q - self.__q_data.q_table[state]))
        )

    def load_model(self, model_file_path: str = None) -> None:
        """Load a Q-table model from a file."""
        if model_file_path:
            self.__q_data = QData(model_file_path)
            if not self.__learn:
                self.__q_data.exploration_rate = self.__q_data.min_exploration  # No exploration if not learning

    def save_model(self, model_file_path: str = None) -> None:
        """Save the current Q-table to a file."""
        if model_file_path:
            self.__q_data.save_q_data(model_file_path)

    def run(self) -> None:
        """Run the Q-learning algorithm for specified episodes."""
        if self.__visual:
            display = Display(self.__step_by_step)

        try:
            for episode in range(self.__episodes):
                snake = Snake()
                food = Food(snake.get_body())
                vision = get_preprocess_vision(snake, food)
                done = False
                steps = 0

                while not done:
                    action = self.__choose_action(vision)
                    state = vision[action]

                    if self.__visual:
                        # Update display
                        while display.update_display(
                                snake, food, self.__get_coefs(vision)):
                            continue

                    reward, done = self.__step(action, snake, food)

                    next_vision = get_preprocess_vision(snake, food)
                    self.__check_vision(next_vision)

                    if self.__learn:
                        self.__update_q_table(state, next_vision, reward)

                    vision = next_vision
                    steps += 1

                # Record episode statistics
                self.__stats.record_episode(
                    snake.score(),
                    self.__q_data.exploration_rate,
                    steps
                )

                # Decay exploration rate
                if self.__learn:
                    self.__q_data.exploration_rate = max(
                        self.__q_data.min_exploration,
                        self.__q_data.exploration_rate *
                        self.__q_data.exploration_decay)

                print(f"Episode {episode + 1}/{self.__episodes} finished "
                      f"with a score of {snake.score()} - "
                      f"Exploration: {self.__q_data.exploration_rate:.4f}")

        except KeyboardInterrupt:
            print("\nTraining interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

        finally:
            if self.__visual:
                display.close()
            self.__stats.plot()
