import random
import time

from utils import helpers
from utils.helpers import conn


# Set hiddenword
# Split word into letters
# Request input
# Split input into letters
# Check which letters match
# Color them
# If all letters match, you win

def print_box():
    print("----------")
    print("|x|x|x|x|x|")
    print("|x|x|x|x|x|")
    print("|x|x|x|x|x|")
    print("|x|x|x|x|x|")
    print("|x|x|x|x|x|")
    print("|x|x|x|x|x|")
    print("----------")


def gameLoop():
    gameOver = False
    while (gameOver == False):
        helpers.clear_screen()
        print_box()
        hiddenWord = input("Enter your guess: ")



def startGame():
    global running
    running = True
    gameLoop()
    # Menu loop
    while running:
        continuePrompt = input("Play again? (yes/no) Or view stats? (stats): ")
        if continuePrompt == 'no':
            running = False
        elif continuePrompt == 'yes':
            gameLoop()
        elif continuePrompt == 'stats':
            # Print header with Unicode box-drawing characters
            print("Stats:")
            print("╔═════════╦═════════╗")
            print("║  Games  ║ Guesses ║")
            print("╠═════════╬═════════╣")
            gamesPlayed = conn.execute("SELECT game FROM wordleStats;").fetchall()
            guessesTaken = conn.execute("SELECT guesses FROM wordleStats;").fetchall()
            for i in range(len(gamesPlayed)):
                game = gamesPlayed[i][0]
                guesses = guessesTaken[i][0]
                print(f"║ {game:^7} ║ {guesses:^7} ║")
            print("╚═════════╩═════════╝")
        else:
            helpers.clear_screen()
            print("Please enter something valid...")



# For testing
# startGame()
