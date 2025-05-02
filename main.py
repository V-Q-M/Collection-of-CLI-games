import random
import time
import duckdb

from utils import helpers
from utils.helpers import conn
from games import number_guesser, tic_tac_toe


# Controls the gamestate
running = True

# Main loop
while running:
    helpers.clear_screen()
    print("What game would you like to play?")
    print("1. Guess the number")
    print("2. Tic Tac Toe")
    print("3. IN PROGRESS")
    print("4. IN PROGRESS")
    print("5. Exit")
    answer = input("Enter your choice: ")
    if (answer == "1"): # Number guesser
        print("Starting \"Guess the number\"")
        time.sleep(2)
        number_guesser.startGame()
    elif(answer == "2"): # Tic tac toe
        print("Starting \"Tic Tac Toe \"")
        time.sleep(2)
        tic_tac_toe.startGame()
    elif(answer == "3"): #
        continue
    elif(answer == "4"): #
        continue
    elif(answer == "5" or answer == "exit"): # Exit application
        running = False;
    else:
        helpers.clear_screen()
        print("Please enter the number.")


conn.close()
