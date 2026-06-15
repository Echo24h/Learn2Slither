# Learn2Slither

A Q-learning agent that learns to play Snake using reinforcement learning.

<p align="center">
  <img src="https://i.ibb.co/ccTmPP0r/Capture-d-cran-du-2025-02-27-15-02-15.png"
       alt="Learn2Slither Screenshot"
       width="400px">
</p>

---

## **Overview**

Learn2Slither is a reinforcement learning project that implements a Q-learning algorithm to teach an AI agent to play the classic Snake game. The agent learns through trial and error, gradually improving its performance over multiple episodes.

### **Features**
- Interactive visual display with pyglet
- Q-learning algorithm implementation
- Save and load trained models
- Adjustable game speed
- Real-time performance metrics
- Two types of food (green: grow, red: shrink)

---

## **Installation**

### **Prerequisites**
- Python 3.14 or newer
- pip package manager

### **Setup**

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Learn2Slither
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## **Usage**

### **Basic Command**
```bash
./snake [options]
```

### **Available Options**
| Option | Description | Default |
|--------|-------------|---------|
| `-visual on/off` | Enable or disable game display | `on` |
| `-episodes <int>` | Number of training episodes | `1` |
| `-load <file>` | Load a pre-trained Q-table | `None` |
| `-save <file>` | Save the Q-table after training | `None` |
| `-dontlearn` | Disable learning (exploitation only) | `False` |
| `-step-by-step` | Wait for user input between steps | `False` |
| `-help` | Display help message | - |

### **Example Commands**

**Train a new agent:**
```bash
./snake -visual on -episodes 1000 -save models/my_model.csv
```

**Load and watch a trained agent:**
```bash
./snake -visual on -load models/q_table_100000.csv -episodes 10 -dontlearn
```

**Step-by-step debugging:**
```bash
./snake -visual on -load models/q_table_100000.csv -step-by-step -dontlearn
```

**Train without visual display (faster):**
```bash
./snake -visual off -episodes 10000 -save models/trained_model.csv
```

---

## **Project Structure**

```
Learn2Slither/
├── agent/
│   ├── __init__.py
│   ├── q_learning.py      # Q-learning algorithm implementation
│   ├── q_data.py          # Q-table management
│   └── vision.py          # Snake vision processing
├── config/
│   ├── __init__.py
│   └── config.py          # Game and learning parameters
├── game/
│   ├── __init__.py
│   ├── snake.py           # Snake logic
│   ├── food.py            # Food management
│   └── display.py         # pyglet visualization
├── assets/                # Sprites and images
├── models/                # Saved Q-tables
├── snake                  # Main entry point
├── requirements.txt       # Python dependencies
└── README.md
```

---

## **How It Works**

### **Q-Learning Algorithm**
The agent uses Q-learning, a model-free reinforcement learning algorithm:
- **State**: The snake's vision in 4 directions (UP, DOWN, LEFT, RIGHT)
- **Actions**: Move in one of the 4 directions
- **Rewards**:
  - Green food: +10
  - Red food: -10
  - Wall/Self collision: -20
  - Regular move: -1

### **Vision System**
The snake perceives its environment through ray-casting in 4 directions, detecting:
- Walls (W)
- Own body (S)
- Green food (G)
- Red food (R)
- Empty space (0)

### **Learning Parameters**
Configurable in [config/config.py](config/config.py):
- Learning rate
- Discount factor
- Exploration rate (decays over time)
- Exploration decay

---

## **Controls (Visual Mode)**

- **Space**: Pause/Resume
- **Left Arrow**: Decrease game speed
- **Right Arrow**: Increase game speed
- **Escape**: Quit game

In step-by-step mode:
- **Space**: Advance to next step

---

## **Development**

### **Code Quality**
The project follows Python best practices:
- Type hints for better code clarity
- Comprehensive docstrings
- PEP 8 style compliance
- Modular architecture

## **Acknowledgments**

- Pygame community for the excellent game development framework
- Q-learning algorithm based on classical reinforcement learning literature
