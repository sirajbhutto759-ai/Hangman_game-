# 🎮 Hangman Game (CLI & GUI)

A classic word-guessing **Hangman** game developed in Python featuring both an interactive **Terminal / CLI mode** and a sleek, modern **Tkinter Desktop GUI**.

> **Project:** CodeAlpha Python Programming Internship  
> **Author:** Siraj  
> **Language:** Python 3.x  
> **Dependencies:** None (Pure Python Standard Library)

---

## 📸 Overview & Features

### 1. 🖥️ Desktop GUI Version (`hangman_gui.py`)
- **Modern Neon Dark UI:** Designed with a dark neon palette (`#0d0d1a`), custom typography, and vibrant accents.
- **Dynamic Gallows & Figure:** Tkinter canvas drawings for gallows and step-by-step rendering of the hangman figure across 6 stages.
- **Interactive On-Screen Keyboard:** Full A–Z touch/click buttons with hover animations, automatic state disablement, and color-coded feedback (green for correct, dim grey for incorrect).
- **Letter Cards / Tiles:** Stylish animated card tiles displaying blanks (`_`) and revealing letters as you guess.
- **Lives Indicator:** Visual heart system (`♥♥♥♥♥♥`) tracking remaining attempts.
- **Win & Game Over Overlays:** Celebration banner with decorative confetti upon winning, and revelation of the secret word upon defeat.
- **Instant Restart:** "⟳ New Game" button to quickly reset state and play another round.

### 2. ⌨️ Terminal / CLI Version (`hangman.py`)
- **ASCII Art Gallows:** Step-by-step visual feedback rendered directly in the terminal (7 stages: 0 to 6).
- **Robust Input Validation:**
  - Prevents non-alphabetical inputs.
  - Rejects multi-character entries.
  - Warns against already-guessed letters without penalizing lives.
- **Status Dashboard:** Shows secret word progress, letters already guessed, and attempts remaining.
- **Continuous Play Loop:** Prompts to play again after victory or defeat without needing to restart the script.

---

## 📂 Project Structure

```text
Hangman_game/
│
├── hangman.py          # Terminal (CLI) version with ASCII art
├── hangman_gui.py      # Desktop GUI version built using Tkinter
└── README.md           # Project documentation and guide
```

---

## ⚙️ Requirements & Installation

This project requires **Python 3.7+**. No third-party packages or `pip install` commands are needed because both versions utilize Python's standard library (`random`, `tkinter`).

To verify Python is installed on your system:
```bash
python --version
```

---

## 🚀 How to Run

Navigate to the project directory:
```bash
cd path/to/Hangman_game
```

### Launch the Desktop GUI Game:
```bash
python hangman_gui.py
```

### Launch the Console / CLI Game:
```bash
python hangman.py
```

---

## 🕹️ Game Rules

1. The game randomly selects a secret word from the predefined word pool (`WORDS`).
2. You have a maximum of **6 incorrect guesses** before the hangman is complete.
3. Guess one letter at a time:
   - **Correct Guess:** All occurrences of that letter are revealed in the word tiles.
   - **Incorrect Guess:** One life / heart is lost, and the next part of the hangman figure is drawn.
4. **Win Condition:** Reveal all letters in the word before running out of lives.
5. **Lose Condition:** Accumulate 6 wrong guesses. The full word will be revealed at the end.

---

## 🛠️ Customization

Want to add your own words or expand the vocabulary?

Open `hangman.py` or `hangman_gui.py` and modify the `WORDS` list near the top of the file:

```python
WORDS = ["python", "hangman", "keyboard", "science", "program", "developer", "challenge"]
```

---

## 📄 License
Developed for educational purposes as part of the CodeAlpha Internship Program. Feel free to modify and expand!
