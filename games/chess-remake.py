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

whitePieces = [wking, wqueen, wbishop, wknight, wrook, wpawn]
blackPieces = [bking, bqueen, bbishop, bknight, brook, bpawn]

emptySquare = " "
playerTurn = 'white'
translate = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}  # map letters to numbers

# tracks the positions of the pieces
board_square = [
    [brook,  bknight,  bbishop,  bqueen,  bking,  bbishop,  bknight,  brook],
    [bpawn,  bpawn,  bpawn,  bpawn,  bpawn,  bpawn,  bpawn,  bpawn],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [wpawn,  wpawn,  wpawn,  wpawn,  wpawn,  wpawn,  wpawn,  wpawn],
    [wrook,  wknight,  wbishop,  wqueen,  wking,  wbishop,  wknight,  wrook],
]

# Does the visuals
emptySquare = ""

position_matrix = [
    [wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook],
    [wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
    [brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],

]



def print_board(board):
    global playerTurn
    helpers.clear_screen()

    # Display turn information
    if playerTurn == 'white':
        print("            \033[47m\033[30m WHITE TURN \033[0m")
    else:
        print("            \033[40m\033[97m BLACK TURN \033[0m")

    print("  ┌" + "───┬" * 7 + "───┐")

    for i in range(8):
        row = "│"
        for j in range(8):
            piece = board[i][j] if board[i][j] != "" else "   "
            row += f" {piece} │"

        print(f"{8 - i} " + row)
        if i != 7:
            print("  ├" + "───┼" * 7 + "───┤")

    print("  └" + "───┴" * 7 + "───┘")

    # Print letter row (a-h)
    finalRow = "   ".join([chr(ord('a') + j) for j in range(8)])  # Prints the letter row
    print("    " + finalRow)


# Visuals
def highlight_red(text):
    return f"\033[41m{text}\033[0m"

def highlight_blue(text):
    return f"\033[44m{text}\033[0m"

def unhighlight(text):
    return re.sub(r'\033\[[0-9;]*m', '', text)

def unhighlight_board(board):
    for i in range(8):
        for j in range(8):
            board[i][j] = unhighlight(board[i][j])

# Board
def startPosition():
    print()



# takes input converts it into usable format
def select_start(board):
    global translate
    selection_prompt = input("Which piece do you want to move?: ")
    start = list(selection_prompt)
    yaxis = translate[start[0]]
    xaxis = int(start[1])
    print(board[xaxis-1][yaxis - 1])


def select_target(board):
    global translate
    target_prompt = input("Enter target square: ")
    target = list(target_prompt)
    yaxis = translate[target[0]]
    xaxis = int(target[1])


def gameLoop():
    global running
    global board_square
    global position_matrix

    helpers.clear_screen()
    print_board(board_square)
    while(running==True):
        select_start(position_matrix)

        select_target(position_matrix)

























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