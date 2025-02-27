from agent import QLearning
from config import Config


if __name__ == "__main__":
    # Récuère argv et exécute la fonction correspondante
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <train|play>")
        sys.exit(1)
    if sys.argv[1] == "train":
        QLearning().train(Config.EPISODES.value, False, True), 
    elif sys.argv[1] == "play":
        QLearning("models/q_table_100000.csv").train(10, True, False)