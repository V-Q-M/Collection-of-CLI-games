import random
import time

from utils import helpers
from utils.helpers import conn

running = True
xIcon = "x"
oIcon = "O"
starIcon = "✓"
# winning combinations
win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Cols
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]


# Prints the game board
def print_board(fields):
    print(f"""
            ╔═════╦═════╦═════╗
            ║  {fields[0]}  ║  {fields[1]}  ║  {fields[2]}  ║
            ╠═════╬═════╬═════╣
            ║  {fields[3]}  ║  {fields[4]}  ║  {fields[5]}  ║
            ╠═════╬═════╬═════╣
            ║  {fields[6]}  ║  {fields[7]}  ║  {fields[8]}  ║
            ╚═════╩═════╩═════╝
            """)

#    # Subscripted version
#    print(f"""
#                    ╔═════╦═════╦═════╗
#                    ║  {fields[0]}₁ ║  {fields[1]}₂ ║  {fields[2]}₃ ║
#                    ╠═════╬═════╬═════╣
#                    ║  {fields[3]}₄ ║  {fields[4]}₅ ║  {fields[5]}₆ ║
#                    ╠═════╬═════╬═════╣
#                    ║  {fields[6]}₇ ║  {fields[7]}₈ ║  {fields[8]}₉ ║
#                    ╚═════╩═════╩═════╝
#                    """)

# game logic happens here
def gameLoop():
    helpers.clear_screen()
    print("Ready? Try to beat me!")
    print("or type \"return\" to return to the main menu\n")

    # Variables
    global running
    gameOver = False
    fields = [" "," "," "," "," "," "," "," "," "]
    #fields = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # GameLoop
    while (gameOver == False and running):
        print_board(fields)
        # Players move
        if (userInput(fields) == False):
            break
        print_board(fields)
        gameOver = checkWin(fields)
        # Computers turn
        if(gameOver == False):
            print("Computer is thinking...")
            time.sleep(2)
            helpers.clear_screen()
            computerMove(fields)
            # print_board(fields)
            gameOver = checkWin(fields)
        # loops back

# Checks if any line has won already, the rest is visuals
# Also inserts the outcome into the database
def checkWin(fields):
    global win_lines
    for line in win_lines:
        a, b, c = line
        if ([fields[a], fields[b], fields[c]] == [xIcon, xIcon, xIcon]):
            [fields[a], fields[b], fields[c]] = [starIcon, starIcon, starIcon]
            helpers.clear_screen()
            print_board(fields)
            print("Player won!")
            conn.execute("""
                         INSERT INTO tictactoeStats(winner) VALUES
                         ('Player')    
                         """)
            return True
        elif ([fields[a], fields[b], fields[c]] == [oIcon, oIcon, oIcon]):
            [fields[a], fields[b], fields[c]] = [starIcon, starIcon, starIcon]
            helpers.clear_screen()
            print_board(fields)
            print("Computer won!")
            conn.execute("""
                         INSERT INTO tictactoeStats(winner)
                         VALUES ('Computer')
                         """)
            return True
    if " " not in fields:
        helpers.clear_screen()
        print_board(fields)
        print("It's a draw!")
        conn.execute("""
                     INSERT INTO tictactoeStats(winner)
                     VALUES ('Draw')
                     """)
        return True
    return False
# Player function
def userInput(fields):
    field = input("Enter a number from 1 to 9: ")
    if (field == "return"):
        global running
        running = False
        return False
    elif(not field.isdigit() or int(field) < 1 or int(field) > 9):
        helpers.clear_screen()
        print_board(fields)
        print("Invalid Input. Try again.")
        return userInput(fields)

    field = int(field) - 1
    if fields[field] == " ":
        helpers.clear_screen()
        fields[field] = xIcon
    else:
        helpers.clear_screen()
        print_board(fields)
        print("Space already taken. Try again.")
        return userInput(fields)


# Computer function
def computerMove(fields):
    global win_lines
    # Checks if it has a winning line
    # If two Chars are his and one is empty, go ahead and win

    for lines in win_lines:
        chars_present = 0  # remembers how many of his chars are in this line
        target = None  # Sets the potential winning field

        for index in lines:
            if (fields[index] == oIcon):  # If 'O' was found, remember that
                chars_present += 1
            elif fields[index] == " ":  # Potential winning field
                target = index

        if (chars_present == 2 and target is not None):  # If the line is  winnable and the target is clear
            fields[target] = oIcon
            return

    # Checks if the player is about to win
    # If two player Chars are filled and he is about to win, go ahead and block him

    for lines in win_lines:
        chars_present = 0
        target = None

        for index in lines:
            if (fields[index] == xIcon):  # If 'x' was found, remember that
                chars_present += 1
            elif fields[index] == " ":  # Potential winning field
                target = index

        if (chars_present == 2 and target is not None):  # If the line is winnable and the target is clear
            fields[target] = oIcon
            return

    # Grab the center edit:
    if (fields[4] == " "):
        fields[4] = oIcon
        return

    # Take the corners
    elif (fields[4] == xIcon):
        for i in [0, 2, 6, 8]:
            if (fields[i] == " "):
                fields[i] = oIcon
                return

    # Fallback to any empty
    for i in range(9):
        if fields[i] == " ":
            fields[i] = oIcon
            return


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
            print("╔══════════╦══════════╗")
            print("║  Rounds  ║  Winner  ║")
            print("╠══════════╬══════════╣")
            roundsPlayed = conn.execute("SELECT rounds from tictactoeStats").fetchall()
            winners      = conn.execute("SELECT winner from tictactoeStats").fetchall()
            for i in range(len(roundsPlayed)):
                rounds = str(roundsPlayed[i][0]).zfill(2)
                winner = winners[i][0]
                print(f"║ {rounds:^8} ║ {winner:^8} ║")
            print("╚══════════╩══════════╝")
        else:
            helpers.clear_screen()
            print("Please enter something valid...")

# For testing
# startGame()