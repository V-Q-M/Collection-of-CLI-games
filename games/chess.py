import re

from utils import helpers
from utils.helpers import conn

running = True

# Define pieces

bking   = "♔"
bqueen  = "♕"
bbishop = "♗"
bknight = "♘"
brook   = "♖"
bpawn   = "♙"

wking   = "♚"
wqueen  = "♛"
wbishop = "♝"
wknight = "♞"
wrook   = "♜"
wpawn   = "♟"

emptySquare = "-"

# Converts the 0 initialized to 1.
def x(cord):
    return cord - 1

# Flips the y-axis
def y(cord):
    return 8 - cord

# Builds the board
square = [[emptySquare] * 8 for _ in range(8)]

def startPosition():
    # White side
    square[x(1)][y(1)] = wrook
    square[x(2)][y(1)] = wknight
    square[x(3)][y(1)] = wbishop
    square[x(4)][y(5)] = wqueen
    square[x(5)][y(1)] = wking
    square[x(6)][y(1)] = wbishop
    square[x(7)][y(1)] = wknight
    square[x(8)][y(1)] = wrook
    for i in range(1,9):
        square[x(i)][y(2)] = wpawn

    # Black side
    square[x(1)][y(8)] = brook
    square[x(2)][y(8)] = bknight
    square[x(3)][y(8)] = bbishop
    square[x(4)][y(8)] = bqueen
    square[x(5)][y(8)] = bking
    square[x(6)][y(8)] = bbishop
    square[x(7)][y(8)] = bknight
    square[x(8)][y(8)] = brook
    for i in range(1,9):
        square[x(i)][y(7)] = bpawn

# Board layout
def print_board():
    global square
    helpers.clear_screen()
    print("  ┌" + "───┬" * 7 + "───┐")
    for i in range(8):
        row = "│"
        for j in range(8):
            row += f" {square[j][i]} │"# adds square to a row
        print(f"{8-i} " + row) # prints the row with the number prefix
        if(i != 7):
            print("  ├" + "───┼" * 7 + "───┤") # middle part
    print("  └" + "───┴" * 7 + "───┘")
    finalRow = "   ".join([chr(ord('a') + j) for j in range(8)]) # prints the letter row
    print("    " + finalRow)

def highlight_red(text):
    return f"\033[41m{text}\033[0m"

def highlight_blue(text):
    return f"\033[44m{text}\033[0m"

def unhighlight(text):
    return re.sub(r'\033\[[0-9;]*m', '', text)

def unhighlight_board():
    global square
    for i in range(8):
        for j in range(8):
            square[i][j] = unhighlight(square[i][j])

# Checks which moves are valid and colours the corresponding squares
def checkValidMoves(xCord,yCord):
    global square
    global emptySquare
    # Defines movement
    def vertical():
        for i in range(1, 8):  # start at 1 to skip the current square
            if yCord + i <= 8:
                if square[x(xCord)][y(yCord + i)] != emptySquare:
                    square[x(xCord)][y(yCord + i)] = highlight_red(square[x(xCord)][y(yCord + i)])
                    break
                square[x(xCord)][y(yCord + i)] = highlight_red(square[x(xCord)][y(yCord + i)])
        for i in range(1, 8):
            if yCord - i > 0:
                if square[x(xCord)][y(yCord - i)] != emptySquare:
                    square[x(xCord)][y(yCord - i)] = highlight_red(square[x(xCord)][y(yCord - i)])
                    break
                square[x(xCord)][y(yCord - i)] = highlight_red(square[x(xCord)][y(yCord - i)])

    def horizontal():
        for i in range(1, 8):
            if xCord + i <= 8:
                if square[x(xCord + i)][y(yCord)] != emptySquare:
                    square[x(xCord + i)][y(yCord)] = highlight_red(square[x(xCord + i)][y(yCord)])
                    break
                square[x(xCord + i)][y(yCord)] = highlight_red(square[x(xCord + i)][y(yCord)])

        for i in range(1, 8):
            if xCord - i > 0:
                if square[x(xCord - i)][y(yCord)] != emptySquare:
                    square[x(xCord - i)][y(yCord)] = highlight_red(square[x(xCord - i)][y(yCord)])
                    break
                square[x(xCord - i)][y(yCord)] = highlight_red(square[x(xCord - i)][y(yCord)])

    def diagonal():
        # Bottom-right ↘
        for i in range(1, 8):
            if (xCord + i <= 8 and yCord + i <= 8):
                if square[x(xCord + i)][y(yCord + i)] != emptySquare:
                    square[x(xCord + i)][y(yCord + i)] = highlight_red(square[x(xCord + i)][y(yCord + i)])
                    break
                square[x(xCord + i)][y(yCord + i)] = highlight_red(square[x(xCord + i)][y(yCord + i)])

        # Top-left ↖
        for i in range(1, 8):
            if (xCord - i > 0 and yCord - i > 0):
                if square[x(xCord - i)][y(yCord - i)] != emptySquare:
                    square[x(xCord - i)][y(yCord - i)] = highlight_red(square[x(xCord - i)][y(yCord - i)])
                    break
                square[x(xCord - i)][y(yCord - i)] = highlight_red(square[x(xCord - i)][y(yCord - i)])

        # Bottom-left ↙
        for i in range(1, 8):
            if (xCord - i > 0 and yCord + i <= 8):
                if square[x(xCord - i)][y(yCord + i)] != emptySquare:
                    square[x(xCord - i)][y(yCord + i)] = highlight_red(square[x(xCord - i)][y(yCord + i)])
                    break
                square[x(xCord - i)][y(yCord + i)] = highlight_red(square[x(xCord - i)][y(yCord + i)])

        # Top-right ↗
        for i in range(1, 8):
            if (xCord + i <= 8 and yCord - i > 0):
                if square[x(xCord + i)][y(yCord - i)] != emptySquare:
                    square[x(xCord + i)][y(yCord - i)] = highlight_red(square[x(xCord + i)][y(yCord - i)])
                    break
                square[x(xCord + i)][y(yCord - i)] = highlight_red(square[x(xCord + i)][y(yCord - i)])

    selectedPiece = square[x(xCord)][y(yCord)]
    # Check which piece is selected to show the correct movement rules
    if (selectedPiece == bqueen or selectedPiece == wqueen):  # Queen can move all directions
        print("found queen")
        vertical()
        horizontal()
        diagonal()
    elif (selectedPiece == brook or selectedPiece == wrook):
        print("found rook")
        vertical()
        horizontal()
    elif (selectedPiece == bbishop or selectedPiece == wbishop):
        print("found bishop")
        diagonal()

def gameLoop():
    gameOver = False
    global running
    i = 0
    helpers.clear_screen()
    print_board()
    translate = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8} # map letters to numbers

    while(running==True):
        # Select piece
        piece = input("Which piece do you want to move?: ")
        selection = list(piece)
        if (selection[0] in translate and selection[1].isdigit()):
            xCord = translate[selection[0]]
            yCord = int(selection[1])
            #selectPiece = square[x(xCord)][y(yCord)]
            checkValidMoves(xCord,yCord)
            square[x(xCord)][y(yCord)] = highlight_blue(unhighlight(square[x(xCord)][y(yCord)])) # Selected piece is blue
            print_board()
            print(xCord)
            print(yCord)


        # Select target
        move = input("Enter target square: ")
        target = list(move)
        if(move == "unselect"):
            unhighlight_board()
            print_board()
        elif (target[0] in translate and target[1].isdigit()):
            xCord = translate[target[0]]
            yCord = int(target[1])
            square[x(xCord)][y(yCord)] = highlight_red(square[x(xCord)][y(yCord)])
            print_board()
            print(xCord)
            print(yCord)
            print("You selected" + square[x(xCord)][y(yCord)])
        #print_board()


def startGame():
    global running
    running = True
    startPosition()
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
            print("╔═════════╦═════════╦═════════╗")
            print("║  Games  ║  Turns  ║  Winner ║")
            print("╠═════════╬═════════╬═════════╣")
            gamesPlayed = conn.execute("SELECT game FROM wordleStats;").fetchall()
            turnsTaken = conn.execute("SELECT turns FROM wordleStats;").fetchall()
            winnersChosen = conn.execute("SELECT winner FROM wordleStats;").fetchall()
            for i in range(len(gamesPlayed)):
                game = gamesPlayed[i][0]
                turns = turnsTaken[i][0]
                winner = winnersChosen[i][0]
                print(f"║ {game:^7} ║ {turns:^7} ║ {winner:^7} ║")
            print("╚═════════╩═════════╝")
        else:
            helpers.clear_screen()
            print("Please enter something valid...")

startGame()