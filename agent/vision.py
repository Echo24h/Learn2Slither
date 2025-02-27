from config import Config

def is_food_position(x, y, food_list):
    """
    Vérifier si la position est déjà utilisée par une pomme.

    Parameters:
    - x, y (int): Coordonnées de la position
    - food_list (list): Liste des pommes

    Return:
    - "G" si la pomme est verte
    - "R" si la pomme est rouge
    - False si la position est vide
    """
    for food in food_list:
        if (x, y) == food["position"]:
            if food["type"] == "green":
                return "G"
            elif food["type"] == "red":
                return "R"
    return False


def get_vision(snake, food):
    """
    Retourne la vision du serpent.

    Parameters:
    - snake (Snake): Instance du serpent
    - food (Food): Instance de la nourriture

    Return:
    - vision (dict): Dictionnaire des directions avec les éléments vis

    Vision example:

    {
        'UP': ['0', 'W'], 
        'DOWN': ['S', '0', '0', '0', '0', '0', '0', '0', 'W'], 
        'LEFT': ['0', 'W'], 
        'RIGHT': ['0', '0', '0', '0', '0', '0', '0', '0', 'W']
    }

    H: Tête du serpent
    S: Corps du serpent
    G: Pomme verte
    R: Pomme rouge
    W: Mur
    0: Espace vide
    """
    vision = {"UP": [], "DOWN": [], "LEFT": [], "RIGHT": []}

    direction = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

    head_x, head_y = snake.get_head()
    body = snake.get_body()
    food_list = food.get_food_list()

    for dir, (dx, dy) in direction.items():
        x, y = head_x, head_y
        while True:
            x += dx
            y += dy
            if x < 0 or x >= Config.GRID_WIDTH.value or y < 0 or y >= Config.GRID_HEIGHT.value:
                vision[dir].append('W')
                break
            food_type = is_food_position(x, y, food_list)
            if food_type != False:
                vision[dir].append(food_type)
            elif (x, y) in body:
                vision[dir].append('S')
            else:
                vision[dir].append('0')
    return vision


def get_preprocess_vision(snake, food):
    """
    Note: Cette fonction peut être améliorée pour obtenir une version plus rapide à l'exécution.

    Retourne la vision du serpent prétraitée.

    Parameters:
    - snake (Snake): Instance du serpent
    - food (Food): Instance de la nourriture

    Return:
    - preprocess_vision (dict): Dictionnaire des directions avec les éléments vis

    Vision example:

    {
        'UP': 'OW',
        'DOWN': 'S0W',
        'LEFT': '0W',
        'RIGHT': '00000000W'
    }
    """
    vision = get_vision(snake, food)
    preprocess_vision = {}

    for dir, values in vision.items():
        preprocess_vision[dir] = "".join(values)
    return preprocess_vision


def print_vision(snake, food):
    """
    Afficher la vision actuelle du serpent dans la console.

    Parameters:
    - snake (Snake): Instance du serpent
    - food (Food): Instance de la nourriture

    Return:
    - None

    Print example: 

    "                           W                  
                                0                  
                                0                  
      W 0 0 0 0 0 0 0 0 0 0 0 0 H S 0 0 0 0 0 0 W
                                0                  
                                0                  
                                0                  
                                0                  
                                0                  
                                0                  
                                0                  
                                W                 "

    H: Tête du serpent
    S: Corps du serpent
    G: Pomme verte
    R: Pomme rouge
    W: Mur
    0: Espace vide
    """
    x = -1
    y = -1
    x_head, y_head = snake.get_head()
    snake_body = snake.get_body()
    food_list = food.get_food_list()

    while y < Config.GRID_HEIGHT.value + 1:
        while x < Config.GRID_WIDTH.value + 1:
            if x == x_head or y == y_head:
                if x == -1 or x == Config.GRID_WIDTH.value or y == -1 or y == Config.GRID_HEIGHT.value:
                    print("W", end=" ")
                elif (x, y) == (x_head, y_head):
                    print("H", end=" ")
                elif (x, y) in snake_body:
                    print("S", end=" ")
                elif is_food_position(x, y, food_list) == "G":
                    print("G", end=" ")
                elif is_food_position(x, y, food_list) == "R":
                    print("R", end=" ")
                else:
                    print("0", end=" ")
            else:
                print(" ", end=" ")
            x += 1
        y += 1
        x = -1
        print("")
