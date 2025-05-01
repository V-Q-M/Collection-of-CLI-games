import random
import duckdb

from utils import helpers
from utils.helpers import conn

running = True
# Game loop
def gameLoop(hiddenNumber):
    # Clear the screen
    helpers.clear_screen()
    print("Got a number! Try to guess it!")
    print("or type \"return\" to return to the main menu\n")

    # Variables
    global running
    tries = 0
    guess = 0

    while guess != hiddenNumber:
        guess = input("Guess the number: ")
        tries += 1
        if (guess == "return"):
            tries-= 1
            running = False
            break
        elif (int(guess) == hiddenNumber or (int(guess)) == 0):
            print("Correct guess! Great job!")
            # Save into the database
            conn.execute("""
                         INSERT INTO numberGuesserStats (guesses)
                         VALUES (?);
                         """, (tries,))
            break
        elif (int(guess) > hiddenNumber):
            print("Try lower!")
        elif (int(guess) < hiddenNumber):
            print("Try higher!")
        elif (guess == "exit"):
            running = False
        else:
            print("Somethings off. Hmm maybe bug?")

def startGame():
    global running
    gameLoop(random.randint(1, 100))
    # Main loop
    while running:
        continuePrompt = input("Play again? (yes/no) Or view stats? (stats): ")
        if continuePrompt == 'no':
            running = False
        elif continuePrompt == 'yes':
            gameLoop(random.randint(1, 100))
        elif continuePrompt == 'stats':
            # Print header with Unicode box-drawing characters
            print("Stats:")
            print("╔═════════╦═════════╗")
            print("║  Games  ║ Guesses ║")
            print("╠═════════╬═════════╣")
            gamesPlayed = conn.execute("SELECT game FROM numberGuesserStats;").fetchall()
            guessesTaken = conn.execute("SELECT guesses FROM numberGuesserStats;").fetchall()
            for i in range(len(gamesPlayed)):
                game = gamesPlayed[i][0]
                guesses = guessesTaken[i][0]
                print(f"║ {game:^7} ║ {guesses:^7} ║")
            print("╚═════════╩═════════╝")
        else:
            print("Please enter something valid...")


