# ============================================================
#   Hangman Game — CodeAlpha Internship Project
#   Author : Siraj
#   Date   : October 2026
#   Description: A console-based Hangman game using basic
#                Python concepts: lists, strings, loops,
#                if-else, functions, and the random module.
# ============================================================

import random  # Used to randomly pick a word from the list


# ----------------------------------------------------------
# STEP 1: Define the word list
# ----------------------------------------------------------
# Exactly 5 predefined words the player might have to guess.
WORDS = ["python", "hangman", "keyboard", "science", "program"]


# ----------------------------------------------------------
# STEP 2: ASCII art stages for the hangman figure
# ----------------------------------------------------------
# Each entry in the list represents a drawing stage.
# Index 0 = no wrong guesses (empty gallows).
# Index 6 = all body parts drawn (game over).
HANGMAN_STAGES = [
    # Stage 0 — empty gallows
    """
   -----
   |   |
       |
       |
       |
       |
=========
    """,
    # Stage 1 — head appears
    """
   -----
   |   |
   O   |
       |
       |
       |
=========
    """,
    # Stage 2 — head + body
    """
   -----
   |   |
   O   |
   |   |
       |
       |
=========
    """,
    # Stage 3 — head + body + left arm
    """
   -----
   |   |
   O   |
  /|   |
       |
       |
=========
    """,
    # Stage 4 — head + body + both arms
    r"""
   -----
   |   |
   O   |
  /|\  |
       |
       |
=========
    """,
    # Stage 5 — head + body + both arms + left leg
    r"""
   -----
   |   |
   O   |
  /|\  |
  /    |
       |
=========
    """,
    # Stage 6 — full hangman (game over)
    r"""
   -----
   |   |
   O   |
  /|\  |
  / \  |
       |
=========
    """,
]


# ----------------------------------------------------------
# STEP 3: Draw the current hangman stage
# ----------------------------------------------------------
def draw_hangman(wrong_guesses):
    """
    Prints the hangman ASCII art for the given number of
    wrong guesses (0 through 6).
    """
    print(HANGMAN_STAGES[wrong_guesses])


# ----------------------------------------------------------
# STEP 4: Show the word with blanks for unguessed letters
# ----------------------------------------------------------
def display_word(word, guessed_letters):
    """
    Builds and returns a string showing the word progress.
    Correctly guessed letters are shown; others show as '_'.

    Example:
        word = "python", guessed = {'p', 'y'}
        returns  "p y _ _ _ _"
    """
    display = ""  # Start with an empty string

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "  # Reveal this letter
        else:
            display += "_ "          # Hide this letter with an underscore

    return display.strip()  # Remove the trailing space


# ----------------------------------------------------------
# STEP 5: Get a valid single-letter guess from the player
# ----------------------------------------------------------
def get_player_guess(guessed_letters):
    """
    Repeatedly prompts the player until they enter a valid,
    new single letter (a-z). Returns the letter in lowercase.
    """
    while True:
        guess = input("  Enter a letter: ").strip().lower()

        # Check: must be exactly one character
        if len(guess) != 1:
            print("  [!] Please enter exactly ONE letter.\n")

        # Check: must be an alphabetic character
        elif not guess.isalpha():
            print("  [!] Please enter a letter (a-z).\n")

        # Check: must not have been guessed already
        elif guess in guessed_letters:
            print(f"  [!] You already guessed '{guess}'. Try a different letter.\n")

        else:
            return guess  # Passed all checks — return the valid guess


# ----------------------------------------------------------
# STEP 6: Main game function
# ----------------------------------------------------------
def play_hangman():
    """
    Runs one complete game of Hangman from start to finish.
    """
    # Welcome banner
    print("=" * 50)
    print("        Welcome to HANGMAN!")
    print("        CodeAlpha Internship Project")
    print("=" * 50)
    print()

    # Randomly pick one word from the predefined list
    word = random.choice(WORDS)

    # A set of all unique letters in the word (used to check win condition)
    word_letters = set(word)

    # A set of letters the player has guessed so far (starts empty)
    guessed_letters = set()

    # Track how many times the player has guessed wrong
    wrong_guesses = 0

    # The player loses after this many wrong guesses
    max_wrong = 6

    print(f"  I'm thinking of a word with {len(word)} letters.")
    print(f"  You have {max_wrong} incorrect guesses allowed.\n")

    # ----------------------------------------------------------
    # STEP 7: Game loop — keep going until win or lose
    # ----------------------------------------------------------
    while wrong_guesses < max_wrong:

        # Show the current hangman drawing
        draw_hangman(wrong_guesses)

        # Show the word with blanks
        print(f"  Word  :  {display_word(word, guessed_letters)}")
        print()

        # Show all letters guessed so far
        if guessed_letters:
            sorted_guesses = ", ".join(sorted(guessed_letters))
            print(f"  Guessed letters  :  {sorted_guesses}")
        else:
            print("  Guessed letters  :  none yet")

        # Show how many wrong guesses remain
        remaining = max_wrong - wrong_guesses
        print(f"  Incorrect attempts remaining  :  {remaining}")
        print()

        # ----------------------------------------------------------
        # STEP 8: Check for a win before asking for the next guess
        # ----------------------------------------------------------
        # issubset() returns True if every letter in word_letters
        # is already present in guessed_letters.
        if word_letters.issubset(guessed_letters):
            print("=" * 50)
            print("  *** Congratulations! You won! ***")
            print(f"  You guessed the word: '{word.upper()}'")
            print("=" * 50)
            return  # End this game

        # Ask the player for their next letter
        guess = get_player_guess(guessed_letters)

        # Add the guess to our set of guessed letters
        guessed_letters.add(guess)

        # ----------------------------------------------------------
        # STEP 9: Check whether the guess was correct or wrong
        # ----------------------------------------------------------
        if guess in word:
            print(f"\n  [+] Nice! '{guess}' is in the word!\n")
        else:
            wrong_guesses += 1  # One more wrong guess
            print(f"\n  [-] Oops! '{guess}' is NOT in the word.\n")

    # ----------------------------------------------------------
    # STEP 10: Game over — show the completed hangman and the word
    # ----------------------------------------------------------
    draw_hangman(wrong_guesses)  # Stage 6 — full hangman
    print("=" * 50)
    print("  *** Game Over! The hangman is complete. ***")
    print(f"  The word was: '{word.upper()}'")
    print("  Better luck next time!")
    print("=" * 50)


# ----------------------------------------------------------
# STEP 11: Play-again loop
# ----------------------------------------------------------
def main():
    """
    Program entry point.
    Starts a game and asks the player if they want to replay.
    """
    while True:
        play_hangman()  # Play one full game

        print()
        again = input("  Play again? (yes / no): ").strip().lower()

        if again in ("yes", "y"):
            print("\n" + "=" * 50 + "\n")
            continue   # Loop back and start a new game
        else:
            print("\n  Thanks for playing! Goodbye!")
            break      # Exit the while loop — program ends here


# ----------------------------------------------------------
# Entry point guard
# ----------------------------------------------------------
# This ensures main() is only called when the script is
# run directly (not when imported as a module).
if __name__ == "__main__":
    main()
