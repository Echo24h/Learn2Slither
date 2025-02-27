import random
import numpy
from config import Config
from game import Snake, Food, Display
from .q_data import QData
from .vision import get_preprocess_vision


class QLearning:

    def __init__(self, visual: bool = True, episodes: int = Config.EPISODES.value, step_by_step: bool = False, learn: bool = True) -> None:

        # Charger les données Q
        self.__q_data = QData()
        self.__episodes = episodes
        self.__visual = visual
        self.__step_by_step = step_by_step
        self.__learn = learn
        if not learn:
            self.__q_data.exploration_rate = 0


    
    def __check_vision(self, vision: dict[str, str]) -> None:
        for direction, state in vision.items():
            if state not in self.__q_data.q_table:
                self.__q_data.q_table[state] = 0

    
    def __get_coefs(self, vision: dict[str, str]) -> dict[str, float]:
        return {direction: self.__q_data.q_table[state] for direction, state in vision.items()}


    def __chose_action(self, vision: dict[str, str]) -> str:
        self.__check_vision(vision)
        
        if self.__learn and random.random() < self.__q_data.exploration_rate:
            return Config.ACTIONS.value[random.choice(range(Config.NUM_ACTIONS.value))]
        else:
            max_value = numpy.argmax([self.__q_data.q_table[value] for _, value in vision.items()])
            return Config.ACTIONS.value[max_value]
        
    
    def __is_eat(self, snake: Snake, food: Food) -> int:
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
        
    
    def __step(self, action: str, snake: Snake, food: Food) -> tuple[dict[str, str], int, bool]:
        reward = 0
        done = False

        snake.change_direction(action)
        snake.move()

        if snake.is_dead():
            reward = Config.REWARDS.value["DEAD"]
            done = True
        else:
            reward = self.__is_eat(snake, food)

        return reward, done
    

    def __update_q_table(self, state: str, next_vision: dict[str, str], reward: int) -> None:

        gamma = self.__q_data.discount_factor
        alpha = self.__q_data.learning_rate
        max_next_Q = numpy.max([self.__q_data.q_table[value] for _, value in next_vision.items()])

        self.__q_data.q_table[state] = self.__q_data.q_table[state] + alpha * (reward + gamma * (max_next_Q - self.__q_data.q_table[state]))


    def load_model(self, model_file_path: str = None) -> None:
        if model_file_path:
            self.__q_data = QData(model_file_path)
            if not self.__learn:
                self.__q_data.exploration_rate = 0


    def save_model(self, model_file_path: str = None) -> None:
        if model_file_path:
            self.__q_data.save_q_data(model_file_path)


    def run(self) -> None:
        
        if self.__visual: 
            display = Display(self.__step_by_step)

        for episode in range(self.__episodes):
            snake = Snake()
            food = Food(snake.get_body())
            vision = get_preprocess_vision(snake, food)

            done = False

            while not done:

                action = self.__chose_action(vision)
                state = vision[action]

                if self.__visual: 
                    # Met à jour l'affichage et vérifie si le jeu est en pause
                    while display.update_display(snake, food, self.__get_coefs(vision)):
                        continue

                reward, done = self.__step(action, snake, food)

                next_vision = get_preprocess_vision(snake, food)
                self.__check_vision(next_vision)

                self.__update_q_table(state, next_vision, reward)

                vision = next_vision

            self.__q_data.exploration_rate = max(self.__q_data.min_exploration, self.__q_data.exploration_rate * self.__q_data.exploration_decay)
            
            print(f"Episode {episode + 1}/{self.__episodes} terminé avec un score de {snake.score()} - Exploration : {self.__q_data.exploration_rate}")
        
        if self.__visual: 
            display.close()

        print("Apprentissage terminé !")