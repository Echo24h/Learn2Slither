import csv
from config import Config


class QData:
    """
    Class to manage Q-learning data, including the Q-table and learning
    parameters. It provides methods to load and save the Q-table from/to a CSV
    file.
    """

    def __init__(self, model_file_path: str = None):

        self.q_table = {}
        self.step = 0
        self.learning_rate = Config.LEARNING_RATE.value
        self.discount_factor = Config.DISCOUNT_FACTOR.value
        self.exploration_rate = Config.EXPLORATION_RATE.value
        self.exploration_decay = Config.EXPLORATION_DECAY.value
        self.min_exploration = Config.MIN_EXPLORATION.value

        if model_file_path:
            self.__load_q_data(model_file_path)

    def __load_q_data(self, model_file_path: str) -> None:
        """Load Q-table data from a CSV file."""
        try:
            with open(model_file_path, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header

                # Read parameters
                params = next(reader)
                self.step = int(params[0])
                self.learning_rate = float(params[1])
                self.discount_factor = float(params[2])
                self.exploration_rate = float(params[3])
                self.exploration_decay = float(params[4])
                self.min_exploration = float(params[5])

                next(reader)  # Skip header

                # Read states and values
                for row in reader:
                    if len(row) == 2:
                        self.q_table[row[0]] = float(row[1])

            print(f"Q-table loaded from {model_file_path}")

        except FileNotFoundError:
            print(f"Error: File {model_file_path} not found")
        except Exception as e:
            print(f"Error loading Q-table: {e}")

    def save_q_data(self, model_file_path: str) -> None:
        """Save Q-table data to a CSV file."""
        try:
            with open(model_file_path, "w", newline='') as file:
                writer = csv.writer(file)

                # Header for parameters
                writer.writerow([
                    "step", "learning_rate", "discount_factor",
                    "exploration", "exploration_decay", "min_exploration"
                ])

                # Write parameters
                writer.writerow([
                    self.step,
                    self.learning_rate,
                    self.discount_factor,
                    self.exploration_rate,
                    self.exploration_decay,
                    self.min_exploration
                ])

                # Header for states and values
                writer.writerow(["state", "value"])

                # Write states and values
                for key, value in self.q_table.items():
                    writer.writerow([key, value])

            print(f"Q-table saved to {model_file_path}")
        except Exception as e:
            print(f"Error saving Q-table: {e}")
