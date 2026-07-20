# Hangman Game

A command-line **Hangman Game** developed in **Python**. The project features multiple game modes, configurable settings, and a hint system while demonstrating file handling, command-line argument parsing, and clean program structure.

## Features

- Random word selection from an external word list
- Classic and Hard game modes
- Configurable number of lives
- Optional hint system
- ASCII Hangman visualization
- Input validation and error handling
- Deterministic word selection using random seed
- Command-line configuration with `argparse`

## Game Modes

### Classic Mode
- Each incorrect guess costs **1 life**.

### Hard Mode
- Each incorrect guess costs **1 life**.
- Incorrect vowel guesses (`A, E, I, O, U`) cost an **additional life**.

## Hint System

When hints are enabled, entering `?`:

- Reveals the first unrevealed letter.
- Costs **1 life**.
- Can be used until all letters are revealed.

## Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `--words` | Path to the word list file (required) |
| `--lives` | Number of lives (3–10, default: 6) |
| `--mode` | Game mode (`classic` or `hard`) |
| `--seed` | Random seed for reproducible word selection |
| `--hint` | Enable or disable hints (`on` / `off`) |

## Technologies

- Python 3
- argparse
- random
- File Handling
- Object-Oriented Programming Concepts
- Command-Line Interface (CLI)

## Project Structure

```
.
├── hangman.py
├── words.txt
└── README.md
```

## Getting Started

Clone the repository:

```bash
git clone https://github.com/yourusername/hangman-game.git
```

Run the game:

```bash
python hangman.py --words words.txt
```

Example:

```bash
python hangman.py --words words.txt --lives 6 --mode hard --hint on --seed 42
```

## Learning Objectives

This project was developed to practice:

- Python programming fundamentals
- File processing
- Command-line applications
- Input validation
- Randomization
- Modular programming
- Error handling

## Notes

- The word list must contain alphabetic words with a minimum length of five characters.
- The game is played entirely in the terminal.
- Invalid inputs are handled gracefully with informative error messages.
