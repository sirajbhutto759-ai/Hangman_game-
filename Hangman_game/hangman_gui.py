# ============================================================
#   Hangman Game — GUI Version (CodeAlpha Internship)
#   Author : Siraj
#   Date   : October 2026
#   GUI Library : tkinter (built into Python — no install needed)
# ============================================================

import random          # To randomly pick a word
import tkinter as tk   # Main GUI library (built-in)
from tkinter import font as tkfont  # For custom fonts


# ----------------------------------------------------------
# GAME DATA
# ----------------------------------------------------------
WORDS = ["python", "hangman", "keyboard", "science", "program"]
MAX_WRONG = 6  # Number of incorrect guesses allowed

# ----------------------------------------------------------
# COLOR PALETTE  (dark neon theme)
# ----------------------------------------------------------
BG         = "#0d0d1a"   # Deep navy background
PANEL      = "#12122a"   # Slightly lighter panel
ACCENT     = "#7c3aed"   # Purple accent
ACCENT2    = "#4f46e5"   # Indigo accent
CORRECT    = "#22c55e"   # Green for correct guesses
WRONG      = "#ef4444"   # Red for wrong guesses
TEXT_MAIN  = "#f1f5f9"   # Near-white text
TEXT_DIM   = "#64748b"   # Dimmed text
GOLD       = "#fbbf24"   # Gold for win message
GALLOWS    = "#94a3b8"   # Light grey gallows
BODY_COLOR = "#f97316"   # Orange neon for hangman body


# ============================================================
#   MAIN APPLICATION CLASS
# ============================================================
class HangmanApp:
    """
    The entire Hangman GUI lives inside this class.
    Each method handles one part of the interface or game logic.
    """

    def __init__(self, root):
        """Set up the main window and start the first game."""
        self.root = root
        self.root.title("Hangman — CodeAlpha")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Center the window on screen
        self.root.geometry("620x820")
        self._center_window(620, 820)

        # Build all UI widgets
        self._build_ui()

        # Start the first game
        self.new_game()

    # ----------------------------------------------------------
    # WINDOW HELPER
    # ----------------------------------------------------------
    def _center_window(self, w, h):
        """Position the window in the middle of the screen."""
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ----------------------------------------------------------
    # UI BUILDER  — creates every widget once at startup
    # ----------------------------------------------------------
    def _build_ui(self):
        """Create all frames, labels, canvas, and buttons."""

        # ── Title bar ─────────────────────────────────────────
        title_frame = tk.Frame(self.root, bg=BG)
        title_frame.pack(pady=(20, 0))

        # Glowing title — each letter gets its own colored label
        colors = [ACCENT, "#9333ea", ACCENT2, "#6366f1",
                  "#818cf8", "#a78bfa", ACCENT]
        for i, ch in enumerate("HANGMAN"):
            lbl = tk.Label(
                title_frame, text=ch,
                font=("Arial Black", 40, "bold"),
                bg=BG, fg=colors[i % len(colors)]
            )
            lbl.pack(side="left")

        # Subtitle
        tk.Label(
            self.root, text="CodeAlpha Internship Project",
            font=("Arial", 10), bg=BG, fg=TEXT_DIM
        ).pack()

        # ── Gallows canvas ────────────────────────────────────
        canvas_frame = tk.Frame(self.root, bg=PANEL,
                                highlightbackground=ACCENT,
                                highlightthickness=2)
        canvas_frame.pack(padx=30, pady=12, fill="x")

        self.canvas = tk.Canvas(
            canvas_frame, width=560, height=220,
            bg=PANEL, highlightthickness=0
        )
        self.canvas.pack()

        # ── Status message (correct / wrong feedback) ─────────
        self.status_var = tk.StringVar(value="Guess a letter to begin!")
        self.status_lbl = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Arial", 13, "italic"), bg=BG, fg=TEXT_DIM,
            height=1
        )
        self.status_lbl.pack(pady=2)

        # ── Word display (letter tiles) ───────────────────────
        self.word_frame = tk.Frame(self.root, bg=BG)
        self.word_frame.pack(pady=10)

        # Tile widgets are built dynamically in _build_word_tiles()
        self.letter_tiles = []   # List of (frame, label) per letter

        # ── Lives / hearts row ────────────────────────────────
        lives_frame = tk.Frame(self.root, bg=BG)
        lives_frame.pack(pady=4)

        tk.Label(
            lives_frame, text="Lives: ",
            font=("Arial", 13, "bold"), bg=BG, fg=TEXT_MAIN
        ).pack(side="left")

        self.heart_labels = []
        for _ in range(MAX_WRONG):
            h = tk.Label(lives_frame, text="♥",
                         font=("Arial", 18), bg=BG, fg=WRONG)
            h.pack(side="left", padx=2)
            self.heart_labels.append(h)

        # ── Alphabet buttons (A-Z in 4 rows) ──────────────────
        btn_outer = tk.Frame(self.root, bg=BG)
        btn_outer.pack(pady=10)

        tk.Label(
            btn_outer, text="Choose a letter:",
            font=("Arial", 11), bg=BG, fg=TEXT_DIM
        ).pack()

        btn_frame = tk.Frame(btn_outer, bg=BG)
        btn_frame.pack(pady=6)

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rows = ["ABCDEFG", "HIJKLMN", "OPQRSTU", "VWXYZ"]
        self.letter_buttons = {}  # letter -> Button widget

        for row_letters in rows:
            row = tk.Frame(btn_frame, bg=BG)
            row.pack(pady=3)
            for ch in row_letters:
                btn = tk.Button(
                    row, text=ch, width=3, height=1,
                    font=("Arial Black", 11),
                    bg=ACCENT2, fg=TEXT_MAIN,
                    activebackground=ACCENT, activeforeground=TEXT_MAIN,
                    relief="flat", cursor="hand2", bd=0,
                    command=lambda c=ch: self._on_letter_click(c)
                )
                btn.pack(side="left", padx=3)
                self._add_hover(btn)
                self.letter_buttons[ch] = btn

        # ── New Game button ────────────────────────────────────
        self.new_game_btn = tk.Button(
            self.root,
            text="⟳  New Game", font=("Arial", 12, "bold"),
            bg=ACCENT, fg=TEXT_MAIN,
            activebackground="#6d28d9", activeforeground=TEXT_MAIN,
            relief="flat", cursor="hand2", padx=16, pady=8,
            command=self.new_game
        )
        self.new_game_btn.pack(pady=12)
        self._add_hover(self.new_game_btn, hover_color="#6d28d9")

    # ----------------------------------------------------------
    # HOVER EFFECT HELPER
    # ----------------------------------------------------------
    def _add_hover(self, widget, hover_color=None):
        """Give a button a subtle colour shift on mouse-over."""
        original = widget.cget("bg")
        hc = hover_color or "#5b21b6"
        widget.bind("<Enter>", lambda e: widget.config(bg=hc))
        widget.bind("<Leave>", lambda e: widget.config(bg=original))

    # ----------------------------------------------------------
    # START / RESET A NEW GAME
    # ----------------------------------------------------------
    def new_game(self):
        """Reset all state and start a fresh game."""
        # Pick a random word
        self.word = random.choice(WORDS)
        self.word_letters = set(self.word)   # Unique letters to find
        self.guessed = set()                 # Letters guessed so far
        self.wrong_count = 0                 # Wrong guess counter

        # Reset status label
        self._set_status("Guess a letter to begin!", TEXT_DIM)

        # Reset all alphabet buttons to their default purple style
        for ch, btn in self.letter_buttons.items():
            btn.config(
                bg=ACCENT2, fg=TEXT_MAIN,
                state="normal", relief="flat"
            )
            # Re-apply hover so colour resets correctly after new_game
            self._add_hover(btn)

        # Rebuild word tiles for the new word
        self._build_word_tiles()

        # Reset hearts to full red
        for h in self.heart_labels:
            h.config(fg=WRONG)

        # Clear the canvas and draw an empty gallows
        self.canvas.delete("all")
        self._draw_gallows()

    # ----------------------------------------------------------
    # WORD TILE BUILDER
    # ----------------------------------------------------------
    def _build_word_tiles(self):
        """Create one styled tile per letter in the secret word."""
        # Remove old tiles
        for widget in self.word_frame.winfo_children():
            widget.destroy()
        self.letter_tiles = []

        for letter in self.word:
            # Outer card frame
            card = tk.Frame(
                self.word_frame, bg="#1e1e3a",
                highlightbackground=ACCENT2,
                highlightthickness=1,
                width=42, height=52
            )
            card.pack(side="left", padx=4)
            card.pack_propagate(False)  # Fix the size

            # Label inside the card — shows '_' or the letter
            lbl = tk.Label(
                card, text="_",
                font=("Arial Black", 22),
                bg="#1e1e3a", fg=TEXT_DIM
            )
            lbl.place(relx=0.5, rely=0.5, anchor="center")

            self.letter_tiles.append((card, lbl, letter))

    # ----------------------------------------------------------
    # REVEAL CORRECTLY GUESSED LETTERS IN THE TILES
    # ----------------------------------------------------------
    def _update_word_display(self):
        """Show guessed letters on their tiles; keep others as '_'."""
        for card, lbl, letter in self.letter_tiles:
            if letter in self.guessed:
                lbl.config(text=letter.upper(), fg=CORRECT)
                card.config(highlightbackground=CORRECT)
            else:
                lbl.config(text="_", fg=TEXT_DIM)
                card.config(highlightbackground=ACCENT2)

    # ----------------------------------------------------------
    # LETTER BUTTON CLICK HANDLER
    # ----------------------------------------------------------
    def _on_letter_click(self, letter):
        """
        Called when the player clicks a letter button.
        Handles correct / wrong guess logic and checks win/lose.
        """
        letter_lower = letter.lower()

        # Add to guessed set
        self.guessed.add(letter_lower)

        # Disable the button so it can't be clicked again
        btn = self.letter_buttons[letter]

        if letter_lower in self.word:
            # ── Correct guess ──────────────────────────────────
            btn.config(bg=CORRECT, fg="#fff",
                       state="disabled", relief="sunken")
            self._set_status(f"✓  '{letter}' is in the word!", CORRECT)
            self._update_word_display()

            # Check win condition
            if self.word_letters.issubset(self.guessed):
                self._show_win()

        else:
            # ── Wrong guess ────────────────────────────────────
            self.wrong_count += 1
            btn.config(bg="#2d2d4a", fg=TEXT_DIM,
                       state="disabled", relief="sunken")
            self._set_status(
                f"✗  '{letter}' is not in the word!  "
                f"({MAX_WRONG - self.wrong_count} left)", WRONG
            )

            # Drain one heart
            self._update_hearts()

            # Draw the next body part on the canvas
            self._draw_body_part(self.wrong_count)

            # Check lose condition
            if self.wrong_count >= MAX_WRONG:
                self._show_game_over()

    # ----------------------------------------------------------
    # STATUS LABEL HELPER
    # ----------------------------------------------------------
    def _set_status(self, msg, color):
        """Update the status message and its colour."""
        self.status_var.set(msg)
        self.status_lbl.config(fg=color)

    # ----------------------------------------------------------
    # HEARTS DISPLAY
    # ----------------------------------------------------------
    def _update_hearts(self):
        """Grey out hearts from right to left as lives are lost."""
        remaining = MAX_WRONG - self.wrong_count
        for i, h in enumerate(self.heart_labels):
            if i < remaining:
                h.config(fg=WRONG)   # Still alive — red heart
            else:
                h.config(fg="#2d2d4a")  # Lost — dark/invisible

    # ----------------------------------------------------------
    # CANVAS: DRAW THE GALLOWS STRUCTURE
    # ----------------------------------------------------------
    def _draw_gallows(self):
        """Draw the static wooden gallows (always visible)."""
        c = self.canvas
        gc = GALLOWS  # Gallows colour

        # Base beam (horizontal ground bar)
        c.create_line(40, 210, 220, 210, fill=gc, width=6)
        # Vertical pole
        c.create_line(100, 210, 100, 20, fill=gc, width=6)
        # Top horizontal beam
        c.create_line(100, 20, 240, 20, fill=gc, width=6)
        # Short drop rope
        c.create_line(240, 20, 240, 55, fill=gc, width=4)
        # Diagonal brace
        c.create_line(100, 60, 150, 20, fill=gc, width=4)

    # ----------------------------------------------------------
    # CANVAS: DRAW HANGMAN BODY PARTS ONE BY ONE
    # ----------------------------------------------------------
    def _draw_body_part(self, part_number):
        """
        Add one body part to the canvas based on wrong_count.
        part_number goes from 1 (head) to 6 (right leg).
        """
        c = self.canvas
        bc = BODY_COLOR  # Neon orange

        if part_number == 1:
            # Head — circle centred at (240, 75)
            c.create_oval(220, 55, 260, 95, outline=bc, width=4)

        elif part_number == 2:
            # Body — vertical line from neck to waist
            c.create_line(240, 95, 240, 155, fill=bc, width=4)

        elif part_number == 3:
            # Left arm — angled from shoulder to lower-left
            c.create_line(240, 110, 205, 140, fill=bc, width=4)

        elif part_number == 4:
            # Right arm — angled from shoulder to lower-right
            c.create_line(240, 110, 275, 140, fill=bc, width=4)

        elif part_number == 5:
            # Left leg — angled from waist to lower-left
            c.create_line(240, 155, 205, 195, fill=bc, width=4)

        elif part_number == 6:
            # Right leg — angled from waist to lower-right
            c.create_line(240, 155, 275, 195, fill=bc, width=4)

    # ----------------------------------------------------------
    # WIN OVERLAY
    # ----------------------------------------------------------
    def _show_win(self):
        """Display a colourful win banner on the canvas."""
        c = self.canvas

        # Semi-transparent dark overlay rectangle
        c.create_rectangle(30, 30, 530, 200,
                            fill="#0d0d1a", outline=CORRECT, width=3)

        # Big "YOU WIN!" text
        c.create_text(280, 90,
                      text="🎉  YOU WIN!",
                      font=("Arial Black", 30),
                      fill=GOLD)

        # Reveal the word
        c.create_text(280, 140,
                      text=f"The word was:  {self.word.upper()}",
                      font=("Arial", 16),
                      fill=CORRECT)

        # Confetti dots for decoration
        import math
        for i in range(20):
            angle = math.radians(i * 18)
            rx = int(240 + 200 * math.cos(angle))
            ry = int(115 + 60 * math.sin(angle))
            colors_conf = [GOLD, CORRECT, ACCENT, "#f472b6", WRONG]
            dot_color = colors_conf[i % len(colors_conf)]
            c.create_oval(rx-5, ry-5, rx+5, ry+5,
                          fill=dot_color, outline="")

        # Disable all letter buttons
        self._disable_all_buttons()
        self._set_status("Congratulations! Press 'New Game' to play again.", GOLD)

    # ----------------------------------------------------------
    # GAME OVER OVERLAY
    # ----------------------------------------------------------
    def _show_game_over(self):
        """Display a game-over banner and reveal the hidden word."""
        c = self.canvas

        # Reveal any remaining letters in tiles
        for card, lbl, letter in self.letter_tiles:
            if letter not in self.guessed:
                lbl.config(text=letter.upper(), fg=WRONG)
                card.config(highlightbackground=WRONG)

        # Dark overlay
        c.create_rectangle(30, 30, 530, 200,
                            fill="#0d0d1a", outline=WRONG, width=3)

        # "GAME OVER" text
        c.create_text(280, 80,
                      text="💀  GAME OVER",
                      font=("Arial Black", 28),
                      fill=WRONG)

        # Reveal the word
        c.create_text(280, 135,
                      text=f"The word was:  {self.word.upper()}",
                      font=("Arial", 16),
                      fill=TEXT_MAIN)

        c.create_text(280, 170,
                      text="Better luck next time!",
                      font=("Arial", 12, "italic"),
                      fill=TEXT_DIM)

        # Disable all letter buttons
        self._disable_all_buttons()
        self._set_status("Game over! Press 'New Game' to try again.", WRONG)

    # ----------------------------------------------------------
    # DISABLE ALL LETTER BUTTONS (after game ends)
    # ----------------------------------------------------------
    def _disable_all_buttons(self):
        """Prevent any more letter presses after the game ends."""
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")


# ============================================================
#   ENTRY POINT
# ============================================================
def main():
    """Create the root Tk window and launch the game."""
    root = tk.Tk()

    # Set a custom icon title (the emoji shows in taskbar on some OS)
    root.title("Hangman 🎮 — CodeAlpha")

    # Launch the app
    app = HangmanApp(root)

    # Start the tkinter event loop — this keeps the window open
    root.mainloop()


if __name__ == "__main__":
    main()
