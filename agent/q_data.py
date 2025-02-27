import csv
from config import Config

class QData:

    def __init__(self, model_file_path=None):

        self.q_table = {}
        self.step = 0
        self.learning_rate = Config.LEARNING_RATE.value
        self.discount_factor = Config.DISCOUNT_FACTOR.value
        self.exploration_rate = Config.EXPLORATION_RATE.value
        self.exploration_decay = Config.EXPLORATION_DECAY.value
        self.min_exploration = Config.MIN_EXPLORATION.value

        if model_file_path:
            self.__load_q_data(model_file_path)

    
        # Charger les données
    def __load_q_data(self, model_file_path="models/q_table.csv"):
        try:
            with open(model_file_path, "r") as file:

                reader = csv.reader(file)
                next(reader)  # Ignorer l'entête

                # Lecture des paramètres
                params = next(reader)
                self.step = int(params[0])
                self.learning_rate = float(params[1])
                self.discount_factor = float(params[2])
                self.exploration_rate = float(params[3])
                self.exploration_decay = float(params[4])
                self.min_exploration = float(params[5])

                next(reader)  # Ignorer l'entête

                # Lecture des états et valeurs
                for row in reader:
                    self.q_table[row[0]] = float(row[1])

            print(f"Table Q chargée depuis {model_file_path}")

        except Exception as e:
            print(f"Erreur lors du chargement de la table Q : {e}")


    # Sauvegarder les données
    def save_q_data(self, model_file_path="models/q_table.csv", q_learning_data = {}):

        try :
            with open(model_file_path, "w") as file:
                writer = csv.writer(file)

                # En-tête pour les paramètres
                writer.writerow(["step", "learning_rate", "discount_factor", "exploration", "exploration_decay", "min_exploration"])

                # Écriture des paramètres
                writer.writerow([
                    self.step,
                    self.learning_rate,
                    self.discount_factor,
                    self.exploration_rate,
                    self.exploration_decay,
                    self.min_exploration
                ])

                # En-tête pour les états
                writer.writerow(["state", "value"])

                # Écriture des états et valeurs
                for key, value in self.q_table.items():
                    writer.writerow([key, value])

            print(f"Table Q sauvegardée dans {model_file_path}")

        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la table Q : {e}")