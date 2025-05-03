import os
import random
import sys

from utils import helpers
from utils.helpers import conn

running = True

# print("\033[31mThis is red text\033[0m")
# print("\033[32mThis is green text\033[0m")
# print("\033[33mThis is yellow text\033[0m")
# print("\033[34mThis is blue text\033[0m")
# print("\033[35mThis is magenta text\033[0m")
# print("\033[36mThis is cyan text\033[0m")

def resource_path(relative_path):
    # Get absolute path to resource
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

with open(resource_path("assets/word_list.txt"), "r") as file:
    word_list = [line.strip() for line in file if line.strip()]

word = [[' ', ' ', ' ', ' ', ' '],  # Row 0
        [' ', ' ', ' ', ' ', ' '],  # Row 1
        [' ', ' ', ' ', ' ', ' '],  # Row 2
        [' ', ' ', ' ', ' ', ' '],  # Row 3
        [' ', ' ', ' ', ' ', ' '],  # Row 4
        [' ', ' ', ' ', ' ', ' ']]  # Row 5


def pickWord():
    global word_list
    global word
    with open(resource_path("assets/word_list.txt"), "r") as file:
        word_list = [line.strip() for line in file if line.strip()]

    word = [[' ', ' ', ' ', ' ', ' '],  # Row 0
            [' ', ' ', ' ', ' ', ' '],  # Row 1
            [' ', ' ', ' ', ' ', ' '],  # Row 2
            [' ', ' ', ' ', ' ', ' '],  # Row 3
            [' ', ' ', ' ', ' ', ' '],  # Row 4
            [' ', ' ', ' ', ' ', ' ']]  # Row 5


hiddenWord = word_list[random.randint(0, len(word_list) - 1)]



def print_box():
    print("┌─────┬─────┬─────┬─────┬─────┐")
    for i in range(len(word)):
        print(f"│  {word[i][0]}  │  {word[i][1]}  │  {word[i][2]}  │  {word[i][3]}  │  {word[i][4]}  │")
        if i < len(word) - 1:
            print("├─────┼─────┼─────┼─────┼─────┤")
    print("└─────┴─────┴─────┴─────┴─────┘")

# Main loop
def gameLoop():
    gameOver = False
    global word_list
    global running
    i = 0
    helpers.clear_screen()
    print_box()

    while(running==True):
        userGuess = input("Enter your guess: ").strip().lower()
        if(userGuess == "return"): # Return to main menu
            running = False
            break
        elif(len(userGuess) == 5): # Checks for valid length
            if(userGuess in word_list):
                potentialGuess = list(userGuess)
                for j in range(0,5):
                    if(potentialGuess[j] == hiddenWord[j]): # Letter matches, paint it green
                        word[i][j] = f"\033[32m{potentialGuess[j].upper()}\033[0m"
                    elif(potentialGuess[j] in hiddenWord): # Word contains letter, paint it yellow
                        word[i][j] = f"\033[33m{potentialGuess[j].upper()}\033[0m"
                    else: # Letters is wrong
                        word[i][j] = potentialGuess[j].upper()
                i += 1 # Increment row
                helpers.clear_screen()
                print_box()
            else:
                helpers.clear_screen()
                print_box()
                print("Word not recognized. Try again.")
            if(userGuess == hiddenWord): # Check if player won
                print("You won! Congratulations!")
                i = 0
                conn.execute("INSERT INTO wordleStats (guesses) VALUES (?);", (i,))
                break
            elif(i == 6):
                print("Whoops. You lost!")
                print("The word was: " + f"\033[31m{hiddenWord}\033[0m")
                i = 0
                conn.execute("INSERT INTO wordleStats (guesses) VALUES (?);", ("lost",))
                break
        else:
            helpers.clear_screen()
            print_box()
            print("Invalid Input. Try again.")


# If letter is correct, make it green
# If word contains the letter, make it yellow



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
            pickWord()
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
#startGame()
