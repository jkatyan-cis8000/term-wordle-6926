#!/usr/bin/env python3
"""
Interactive Wordle Game - A terminal-based Wordle clone.

Players guess a daily 5-letter English word in 6 attempts.
Feedback colors:
  - Green: Correct letter in correct position
  - Yellow: Correct letter in wrong position
  - Grey: Invalid letter (not in solution)
"""

import os
import sys
from game_logic import (
    get_random_solution,
    is_valid_word,
    format_guess_with_colors,
    evaluate_guess,
    get_max_attempts
)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_game_header():
    """Display the game header and instructions."""
    print("\n" + "=" * 50)
    print(" " * 15 + "W O R D L E")
    print("=" * 50)
    print("\nGuess the 5-letter word in 6 attempts!")
    print("After each guess, the color of the letters will change")
    print("to show how close your guess was to the word.")
    print("\n  \033[92mG\033[0m = Correct letter, correct position")
    print("  \033[93mY\033[0m = Correct letter, wrong position")
    print("  \033[90mX\033[0m = Letter not in word")
    print("-" * 50 + "\n")


def get_user_guess(attempt, previous_guesses):
    """
    Get a valid guess from the user.
    
    Args:
        attempt: Current attempt number (1-6)
        previous_guesses: List of previously guessed words
    
    Returns:
        A valid 5-letter word in lowercase, or None if quit
    """
    while True:
        try:
            guess = input(f"Attempt {attempt}/{get_max_attempts()} - Enter your 5-letter guess: ").strip().lower()
            
            # Check if quit command
            if guess in ['quit', 'q', 'exit']:
                return None
            
            # Validate length
            if len(guess) != 5:
                print("  ⚠️  Please enter exactly 5 letters.")
                continue
            
            # Validate it's all letters
            if not guess.isalpha():
                print("  ⚠️  Please enter only letters (no numbers or symbols).")
                continue
            
            # Validate it's in the word list
            if not is_valid_word(guess):
                print("  ⚠️  Not a valid word. Try again.")
                continue
            
            # Check for duplicate guesses
            if guess in previous_guesses:
                print("  ⚠️  You already guessed that word. Try a different one.")
                continue
            
            return guess
            
        except KeyboardInterrupt:
            return None
        except EOFError:
            return None


def display_board(guesses, solution):
    """
    Display the current game board with all guesses.
    
    Args:
        guesses: List of guessed words
        solution: The solution word (revealed at the end)
    """
    clear_screen()
    display_game_header()
    
    print("BOARD:")
    print("-" * 50)
    
    for guess in guesses:
        colored_guess = format_guess_with_colors(guess, solution)
        print(f"  {colored_guess}")
    
    # Show empty rows for remaining attempts
    remaining = get_max_attempts() - len(guesses)
    for _ in range(remaining):
        print("  _ _ _ _ _")
    
    print("-" * 50)


def play_round():
    """
    Play a single round of Wordle.
    
    Returns:
        True if player won, False if player lost, None if game was quit
    """
    solution = get_random_solution()
    guesses = []
    
    while len(guesses) < get_max_attempts():
        display_board(guesses, solution)
        
        guess = get_user_guess(len(guesses) + 1, guesses)
        
        if guess is None:
            return None
        
        guesses.append(guess)
        
        # Check if guessed correctly
        if guess == solution:
            display_board(guesses, solution)
            print(f"\n\033[92m🎉 Congratulations! You guessed the word in {len(guesses)} attempt(s)!\033[0m")
            return True
    
    # Player ran out of attempts
    display_board(guesses, solution)
    print(f"\n\033[90m💀 Game Over! The word was: {solution.upper()}\033[0m")
    return False


def play_game():
    """Main game loop."""
    try:
        while True:
            clear_screen()
            display_game_header()
            
            result = play_round()
            
            if result is None:
                print("\n\nGame quit. Thanks for playing!")
                break
            
            # Ask to play again
            if result:
                play_again = input("\n🎉 Great job! Play again? (y/n): ").strip().lower()
            else:
                play_again = input("\n💀 Want to try again? (y/n): ").strip().lower()
            
            if play_again not in ['y', 'yes', '']:
                break
            
    except KeyboardInterrupt:
        print("\n\nThanks for playing Wordle!")
    except EOFError:
        print("\n\nThanks for playing Wordle!")


if __name__ == "__main__":
    print("\nStarting Wordle...")
    play_game()
    print("\nGoodbye! 👋\n")
