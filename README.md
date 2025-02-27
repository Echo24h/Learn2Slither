# Learn2Slither - Work in Progress 🚀

<p align="center">
  <img src="https://i.ibb.co/ccTmPP0r/Capture-d-cran-du-2025-02-27-15-02-15.png" 
       alt="Capture d'écran"
       width="400px">
</p>

## **Description**
Ce programme permet de jouer à Snake avec une intelligence artificielle basée sur une **Q-table**. Il propose plusieurs options pour personnaliser l'expérience, y compris l'affichage du jeu, le chargement et la sauvegarde d'un modèle, ainsi que le contrôle du processus d'apprentissage.

---

## **Utilisation**
Lancer le programme avec différentes options en ligne de commande :

```bash
./snake [options]
```

### **Options disponibles**
| Option | Description |
|--------|-------------|
| `-visual on/off` | Active ou désactive l'affichage du jeu (défaut : `on`). |
| `-sessions <int>` | Définit le nombre de parties à jouer (défaut : `1`). |
| `-load <file>` | Charge un modèle de **Q-table** depuis un fichier. |
| `-save <file>` | Sauvegarde le modèle de **Q-table** dans un fichier. |
| `-dontlearn` | Désactive l'apprentissage pendant l'exécution. |
| `-step-by-step` | Attend une entrée utilisateur entre chaque étape. |
| `-help` | Affiche ce message d'aide. |

---

## **Exemple d'exécution**

```bash
./snake -visual on -load models/100sess.csvtxt -sessions 10 -dontlearn -step-by-step
```

- Active l'affichage du jeu.
- Charge la Q-table depuis `models/100sess.csvtxt`.
- Joue **10 sessions**.
- Désactive l'apprentissage.
- Attend une entrée utilisateur entre chaque étape.

---

## **Dépendances**
Assurez-vous d'avoir installé les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

Si vous utilisez un environnement virtuel **(recommandé)** :

```bash
python3 -m venv venv
source venv/bin/activate  # (Windows : venv\Scripts\activate)
pip install -r requirements.txt
```

---

## **Contact & Support**
Si vous avez des questions ou des suggestions, n'hésitez pas à ouvrir une issue sur le dépôt du projet ! 🚀

