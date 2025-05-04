import random
import time
# import duckdb

from utils import helpers
from utils.helpers import conn
from games import number_guesser, tic_tac_toe, wordle, chess


# Controls the gamestate
running = True

# Main loop
while running:
    helpers.clear_screen()
    print("What game would you like to play?")
    print("1. Guess the number")
    print("2. Tic Tac Toe")
    print("3. Wordle")
    print("4. Chess")
    print("5. Exit")
    answer = input("Enter your choice: ")
    if (answer == "1" or answer == "Guess the number"): # Number guesser
        print("\nStarting \"Guess the number\"")
        time.sleep(2)
        number_guesser.startGame()
    elif(answer == "2" or answer == "Tic Tac Toe"): # Tic tac toe
        print("\nStarting \"Tic Tac Toe\"")
        time.sleep(2)
        tic_tac_toe.startGame()
    elif(answer == "3" or answer == "Wordle"): # Wordle
        print("\nStarting \"Wordle\"")
        time.sleep(2)
        wordle.startGame()
    elif(answer == "4"): # Chess
        print("\nStarting \"Chess\"")
        time.sleep(2)
        chess.startGame()
    elif(answer == "5" or answer == "exit"): # Exit application
        running = False
    else:
        helpers.clear_screen()
        print("\nPlease enter the number.")


conn.close()
