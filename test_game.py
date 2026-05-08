#!/usr/bin/env python3
"""
Test suite for Wordle game logic.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_logic import (
    get_random_solution,
    is_valid_word,
    evaluate_guess,
    format_guess_with_colors,
    get_max_attempts
)


def test_get_random_solution():
    """Test that get_random_solution returns a valid word."""
    solution = get_random_solution()
    assert is_valid_word(solution), f"Solution '{solution}' not in word list"
    assert len(solution) == 5, f"Solution '{solution}' is not 5 letters"
    print("✓ test_get_random_solution passed")


def test_is_valid_word():
    """Test the is_valid_word function."""
    assert is_valid_word("apple") == True, "apple should be valid"
    assert is_valid_word("APPLE") == False, "APPLE (uppercase) should be invalid"
    assert is_valid_word("xyz") == False, "xyz should be invalid (not 5 letters)"
    assert is_valid_word("zzzzz") == False, "zzzzz should be invalid (not in word list)"
    print("✓ test_is_valid_word passed")


def test_evaluate_guess_exact_match():
    """Test evaluation when guess matches exactly."""
    guess = "apple"
    solution = "apple"
    result = evaluate_guess(guess, solution)
    expected = ['G'] * 5
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_evaluate_guess_exact_match passed")


def test_evaluate_guess_no_matches():
    """Test evaluation when there are no matching letters."""
    guess = "zzzzz"
    solution = "apple"
    result = evaluate_guess(guess, solution)
    expected = ['X'] * 5
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ test_evaluate_guess_no_matches passed")


def test_evaluate_guess_some_matches():
    """Test evaluation with some correct positions."""
    # Use "grape" vs "apple": g!=a, r!=p, a!=p, p==l? no, e==e
    # That doesn't work either. Let's use "shalt" vs "apple"
    # s!=a, h!=p, a!=p, l==l, t!=e -> X X X G X
    # Hmm that only has one green. Let's use a word where positions 2,3,4 match "pple"
    # We need a word like "_ _ p l e" where first two don't match
    # "siple" -> s!=a, i!=p, p==p, l==l, e==e -> X X G G G
    guess = "siple"
    solution = "apple"
    result = evaluate_guess(guess, solution)
    # 's' at position 0: X (not in solution)
    # 'i' at position 1: X (not in solution)
    # 'p' at position 2: G (exact match with solution[2])
    # 'l' at position 3: G (exact match with solution[3])
    # 'e' at position 4: G (exact match with solution[4])
    assert result[0] == 'X', f"Position 0 should be X (grey), got {result[0]}"
    assert result[1] == 'X', f"Position 1 should be X (grey), got {result[1]}"
    assert result[2] == 'G', f"Position 2 should be G (green), got {result[2]}"
    assert result[3] == 'G', f"Position 3 should be G (green), got {result[3]}"
    assert result[4] == 'G', f"Position 4 should be G (green), got {result[4]}"
    print("✓ test_evaluate_guess_some_matches passed")


def test_evaluate_guess_duplicate_letters():
    """Test evaluation with duplicate letters in guess and solution."""
    guess = "abate"
    solution = "apple"
    result = evaluate_guess(guess, solution)
    # 'a' at 0: G (exact match)
    # 'b' at 1: X (not in solution)
    # 'a' at 2: X (only one 'a' in solution, already matched)
    # 't' at 3: X (not in solution)
    # 'e' at 4: G (exact match, both words end with 'e')
    assert result[0] == 'G', f"Position 0 should be G, got {result[0]}"
    assert result[1] == 'X', f"Position 1 should be X, got {result[1]}"
    assert result[2] == 'X', f"Position 2 should be X, got {result[2]}"
    assert result[3] == 'X', f"Position 3 should be X, got {result[3]}"
    assert result[4] == 'G', f"Position 4 should be G, got {result[4]}"
    print("✓ test_evaluate_guess_duplicate_letters passed")


def test_evaluate_guess_wrong_position():
    """Test evaluation with correct letter in wrong position."""
    guess = "plate"
    solution = "apple"
    result = evaluate_guess(guess, solution)
    # 'p' at 0: Y (in solution but not at position 0)
    # 'l' at 1: Y (in solution but not at position 1)
    # 'a' at 2: Y (in solution but not at position 2)
    # 't' at 3: X (not in solution)
    # 'e' at 4: G (exact match, both words end with 'e')
    assert result[0] == 'Y', f"Position 0 should be Y, got {result[0]}"
    assert result[1] == 'Y', f"Position 1 should be Y, got {result[1]}"
    assert result[2] == 'Y', f"Position 2 should be Y, got {result[2]}"
    assert result[3] == 'X', f"Position 3 should be X, got {result[3]}"
    assert result[4] == 'G', f"Position 4 should be G, got {result[4]}"
    print("✓ test_evaluate_guess_wrong_position passed")


def test_format_guess_with_colors():
    """Test that format_guess_with_colors returns colored output."""
    guess = "apple"
    solution = "apple"
    colored = format_guess_with_colors(guess, solution)
    # Should contain green color codes
    assert '\033[92m' in colored, "Should contain green color code"
    # Check that the word contains the letters A, P, P, L, E in order (with ANSI codes between)
    # Each letter should be wrapped in green color code
    for letter in ['A', 'P', 'P', 'L', 'E']:
        assert letter in colored, f"Should contain uppercase letter {letter}"
    print("✓ test_format_guess_with_colors passed")


def test_get_max_attempts():
    """Test that maximum attempts is 6."""
    assert get_max_attempts() == 6, "Should have 6 attempts"
    print("✓ test_get_max_attempts passed")


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 50)
    print("Running Wordle Game Tests")
    print("=" * 50)
    print()
    
    tests = [
        test_get_random_solution,
        test_is_valid_word,
        test_evaluate_guess_exact_match,
        test_evaluate_guess_no_matches,
        test_evaluate_guess_some_matches,
        test_evaluate_guess_duplicate_letters,
        test_evaluate_guess_wrong_position,
        test_format_guess_with_colors,
        test_get_max_attempts,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
