"""
Game logic for Wordle - handles solution generation, guess validation, and feedback.
"""

import random
try:
    from .word_list import WORD_LIST
except ImportError:
    from word_list import WORD_LIST


def get_random_solution():
    """Select a random 5-letter word as the solution."""
    return random.choice(WORD_LIST)


def is_valid_word(word):
    """Check if a word is in the valid word list (case-sensitive, matches WORD_LIST format)."""
    # WORD_LIST contains lowercase words only
    # So "apple" is valid, but "APPLE" is not (case-sensitive check)
    return word in WORD_LIST


def evaluate_guess(guess, solution):
    """
    Evaluate a guess against the solution.
    
    Returns a list of color codes for each letter:
    - 'G' for Green: correct letter in correct position
    - 'Y' for Yellow: correct letter in wrong position
    - 'X' for Grey: letter not in solution or already matched
    
    Args:
        guess: The 5-letter guess
        solution: The 5-letter solution word
    
    Returns:
        A list of 5 color codes ('G', 'Y', or 'X')
    """
    guess = guess.lower()
    solution = solution.lower()
    
    if len(guess) != 5:
        raise ValueError("Guess must be exactly 5 letters")
    
    if len(solution) != 5:
        raise ValueError("Solution must be exactly 5 letters")
    
    # Initialize result with 'X' (grey) for all positions
    result = ['X'] * 5
    
    # Count letter frequencies in solution (for yellow check)
    solution_letter_counts = {}
    for letter in solution:
        solution_letter_counts[letter] = solution_letter_counts.get(letter, 0) + 1
    
    # First pass: Find exact matches (Green)
    for i in range(5):
        if guess[i] == solution[i]:
            result[i] = 'G'
            solution_letter_counts[guess[i]] -= 1
    
    # Second pass: Find partial matches (Yellow)
    for i in range(5):
        if result[i] != 'G':
            letter = guess[i]
            if solution_letter_counts.get(letter, 0) > 0:
                result[i] = 'Y'
                solution_letter_counts[letter] -= 1
    
    return result


def color_letter(letter, color_code):
    """Apply ANSI color codes to a letter."""
    colors = {
        'G': '\033[92m',  # Green
        'Y': '\033[93m',  # Yellow
        'X': '\033[90m'   # Grey
    }
    reset = '\033[0m'
    color = colors.get(color_code, '')
    return f"{color}{letter.upper()}{reset}"


def format_guess_with_colors(guess, solution):
    """
    Format a guess with colored letters for display.
    
    Args:
        guess: The 5-letter guess
        solution: The 5-letter solution word
    
    Returns:
        A formatted string with colored letters (uppercase)
    """
    colors = evaluate_guess(guess.upper(), solution)
    return ''.join(color_letter(guess[i], colors[i]) for i in range(5))


def get_max_attempts():
    """Return the maximum number of attempts allowed."""
    return 6
