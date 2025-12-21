# Learn2Slither

<p align="center">
  <img src="https://i.ibb.co/ccTmPP0r/Capture-d-cran-du-2025-02-27-15-02-15.png"
       alt="Screenshot"
       width="400px">
</p>

---

## **Usage**
Run the program with various command‑line options:

```bash
./snake [options]
```

### **Available Options**
| Option | Description |
|--------|-------------|
| `-visual on/off` | Enables or disables the game display (default: `on`). |
| `-episodes <int>` | Sets the number of game sessions to play (default: `1`). |
| `-load <file>` | Loads a **Q‑table** model from a file. |
| `-save <file>` | Saves the **Q‑table** model to a file. |
| `-dontlearn` | Disables learning during execution. |
| `-step-by-step` | Waits for user input between each step. |
| `-help` | Displays this help message. |

---

## **Example Execution**

```bash
./snake -visual on -load models/100sess.csvtxt -episodes 10 -dontlearn -step-by-step
```

- Enables the game display  
- Loads the Q‑table from `models/100sess.csvtxt`  
- Plays **10 sessions**  
- Disables learning  
- Waits for user input between each step  

---

## **Dependencies**
Make sure you have installed the required dependencies:

```bash
pip install -r requirements.txt
```

If you are using a virtual environment **(recommended)**:

> Note: Python 3.14 is not compatible with Pygame. Python 3.12 is recommended.

```bash
py -3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
