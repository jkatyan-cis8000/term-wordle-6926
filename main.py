#!/usr/bin/env python3
"""
Main entry point for the Wordle game.

This module ties together all components and provides a simple way to run the game.
"""

import sys
from wordle_game import play_game


def main():
    """Entry point for the Wordle game."""
    print("=" * 50)
    print("  Welcome to Terminal Wordle!")
    print("=" * 50)
    print("\nPress Enter to start playing...")
    input()
    play_game()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nThanks for playing!")
        sys.exit(0)
