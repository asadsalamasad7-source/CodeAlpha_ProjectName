import random

WORDS = ["python", "keyboard", "hangman", "variable", "function"]

HANGMAN_STAGES = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========
    """,
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========
    """,
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
    """,
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
    """,
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
    """,
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
    """,
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
    """
]

def display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def play_hangman():
    word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = 6

    print("\n==============================")
    print("   Welcome to Hangman!")
    print("==============================")

    while wrong_guesses < max_wrong:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"Word: {display_word(word, guessed_letters)}")
        print(f"Wrong guesses: {wrong_guesses}/{max_wrong}")
        if guessed_letters:
            print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")

        # Check win condition
        if all(letter in guessed_letters for letter in word):
            print(f"\n🎉 You won! The word was: {word}")
            break

        # Get player input
        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(f"✓ '{guess}' is in the word!")
        else:
            wrong_guesses += 1
            print(f"✗ '{guess}' is not in the word.")
    else:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"\nGame over! The word was: {word}")

    play_again = input("\nPlay again? (y/n): ").strip().lower()
    if play_again == "y":
        play_hangman()
    else:
        print("Thanks for playing. Goodbye!")

if __name__ == "__main__":
    play_hangman()