import copy
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

xCord = 0
yCord = 0

translate = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}  # map letters to numbers


# Converts the 0 initialized to 1.
def x(cord):
    return cord - 1

# Flips the y-axis
def y(cord):
    return 8 - cord

# Builds the board
square = [[emptySquare] * 8 for _ in range(8)]

def print_square(square):
    for row in square:
        print(" ".join(str(item) for item in row))

def startPosition():
    global fakeSquare
    # White side
    square[x(1)][y(1)] = wrook
    square[x(2)][y(1)] = wknight
    square[x(3)][y(1)] = wbishop
    square[x(4)][y(1)] = wqueen
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

    fakeSquare = copy.deepcopy(square)

fakeSquare = copy.deepcopy(square)


# Board layout
def print_board():
    global square
    global playerTurn
    helpers.clear_screen()
    if (playerTurn == 'white'):
        print("            \033[47m\033[30m WHITE TURN \033[0m")
    else:
        print("            \033[40m\033[97m BLACK TURN \033[0m")

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

def unhighlight_board(board):

    for i in range(8):
        for j in range(8):
            board[i][j] = unhighlight(board[i][j])

# Stores all valid moves
validMoveStorage = []

# Checks which moves are valid and colours the corresponding squares
def checkValidMoves(xCord,yCord, boardInput):
    global emptySquare
    # Defines movement
    def verticalPawn(n):
        global validMoveStorage
        if boardInput[x(xCord)][y(yCord)] in whitePieces:
            for i in range(1, n):
                if (yCord + i <= 8):
                    if boardInput[x(xCord)][y(yCord + i)] == emptySquare: # move forward
                        boardInput[x(xCord)][y(yCord + i)] = highlight_red(boardInput[x(xCord)][y(yCord + i)])
                        validMoveStorage += [[xCord, yCord + i]]
                    else:
                        break

            for dx in [-1, 1]:
                if 0 <= xCord + dx < 8 and yCord + 1 <= 8:
                    if boardInput[x(xCord + dx)][y(yCord + 1)] in blackPieces:
                        boardInput[x(xCord + dx)][y(yCord + 1)] = highlight_red(boardInput[x(xCord + dx)][y(yCord + 1)])
                        validMoveStorage += [[xCord + dx, yCord + 1]]

        elif boardInput[x(xCord)][y(yCord)] in blackPieces:
            for i in range(1, n):
                if yCord - i > 0:
                    if boardInput[x(xCord)][y(yCord - i)] == emptySquare: # move forward
                        boardInput[x(xCord)][y(yCord - i)] = highlight_red(boardInput[x(xCord)][y(yCord - i)])
                        validMoveStorage += [[xCord, yCord - i]]
                    else:
                        break
            # Diagonal captures
            for dx in [-1, 1]:
                if 0 <= xCord + dx < 8 and yCord - 1 > 0:
                    if boardInput[x(xCord + dx)][y(yCord - 1)] in whitePieces:
                        boardInput[x(xCord + dx)][y(yCord - 1)] = highlight_red(boardInput[x(xCord + dx)][y(yCord - 1)])
                        validMoveStorage += [[xCord + dx, yCord - 1]]

    def vertical(n):
        global validMoveStorage
        for i in range(1, n):  # start at 1 to skip the current square
            if yCord + i <= 8:
                if boardInput[x(xCord)][y(yCord + i)] != emptySquare: # Collision
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord)][y(yCord + i)] in blackPieces: # add to targets
                        boardInput[x(xCord)][y(yCord + i)] = highlight_red(boardInput[x(xCord)][y(yCord + i)])
                        validMoveStorage += [[xCord,yCord + i]] # add this move
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord)][y(yCord + i)] in whitePieces: # add to targets
                        boardInput[x(xCord)][y(yCord + i)] = highlight_red(boardInput[x(xCord)][y(yCord + i)])
                        validMoveStorage += [[xCord,yCord + i]]
                    break
                boardInput[x(xCord)][y(yCord + i)] = highlight_red(boardInput[x(xCord)][y(yCord + i)])
                validMoveStorage += [[xCord, yCord + i]]

        for i in range(1, n):
            if yCord - i > 0:
                if boardInput[x(xCord)][y(yCord - i)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord)][y(yCord - i)] in blackPieces:
                        boardInput[x(xCord)][y(yCord - i)] = highlight_red(boardInput[x(xCord)][y(yCord - i)])
                        validMoveStorage += [[xCord,yCord - i]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord)][y(yCord - i)] in whitePieces:
                        boardInput[x(xCord)][y(yCord - i)] = highlight_red(boardInput[x(xCord)][y(yCord - i)])
                        validMoveStorage += [[xCord,yCord - i]]
                    break
                boardInput[x(xCord)][y(yCord - i)] = highlight_red(square[x(xCord)][y(yCord - i)])
                validMoveStorage += [[xCord, yCord - i]]

    def horizontal(n):
        global validMoveStorage
        for i in range(1, n):
            if xCord + i <= 8:
                if boardInput[x(xCord + i)][y(yCord)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord + i)][y(yCord)] in blackPieces:
                        boardInput[x(xCord + i)][y(yCord)] = highlight_red(boardInput[x(xCord + i)][y(yCord)])
                        validMoveStorage += [[xCord + i,yCord]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord + i)][y(yCord)] in whitePieces:
                        boardInput[x(xCord + i)][y(yCord)] = highlight_red(boardInput[x(xCord + i)][y(yCord)])
                        validMoveStorage += [[xCord + i,yCord]]
                    break
                boardInput[x(xCord + i)][y(yCord)] = highlight_red(boardInput[x(xCord + i)][y(yCord)])
                validMoveStorage += [[xCord + i, yCord]]

        for i in range(1, n):
            if xCord - i > 0:
                if boardInput[x(xCord - i)][y(yCord)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord - i)][y(yCord)] in blackPieces:
                        boardInput[x(xCord - i)][y(yCord)] = highlight_red(boardInput[x(xCord - i)][y(yCord)])
                        validMoveStorage += [[xCord - i,yCord]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord - i)][y(yCord)] in whitePieces:
                        boardInput[x(xCord - i)][y(yCord)] = highlight_red(boardInput[x(xCord - i)][y(yCord)])
                        validMoveStorage += [[xCord - i,yCord]]
                    break
                boardInput[x(xCord - i)][y(yCord)] = highlight_red(boardInput[x(xCord - i)][y(yCord)])
                validMoveStorage += [[xCord - i, yCord]]

    def diagonal(n):
        global validMoveStorage
        # Bottom-right ↘
        for i in range(1, n):
            if (xCord + i <= 8 and yCord + i <= 8):
                if boardInput[x(xCord + i)][y(yCord + i)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord + i)][y(yCord + i)] in blackPieces:
                        boardInput[x(xCord + i)][y(yCord + i)] = highlight_red(boardInput[x(xCord + i)][y(yCord + i)])
                        validMoveStorage += [[xCord + i,yCord + i]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord + i)][y(yCord + i)] in whitePieces:
                        boardInput[x(xCord + i)][y(yCord + i)] = highlight_red(boardInput[x(xCord + i)][y(yCord + i)])
                        validMoveStorage += [[xCord + i,yCord + i]]
                    break
                boardInput[x(xCord + i)][y(yCord + i)] = highlight_red(boardInput[x(xCord + i)][y(yCord + i)])
                validMoveStorage += [[xCord + i,yCord + i]]

        # Top-left ↖
        for i in range(1, n):
            if (xCord - i > 0 and yCord - i > 0):
                if boardInput[x(xCord - i)][y(yCord - i)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord - i)][y(yCord - i)] in blackPieces:
                        boardInput[x(xCord - i)][y(yCord - i)] = highlight_red(boardInput[x(xCord - i)][y(yCord - i)])
                        validMoveStorage += [[xCord - i,yCord - i]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord - i)][y(yCord - i)] in whitePieces:
                        boardInput[x(xCord - i)][y(yCord - i)] = highlight_red(boardInput[x(xCord - i)][y(yCord - i)])
                        validMoveStorage += [[xCord - i,yCord - i]]
                    break
                boardInput[x(xCord - i)][y(yCord - i)] = highlight_red(boardInput[x(xCord - i)][y(yCord - i)])
                validMoveStorage += [[xCord - i, yCord - i]]

        # Bottom-left ↙
        for i in range(1, n):
            if (xCord - i > 0 and yCord + i <= 8):
                if boardInput[x(xCord - i)][y(yCord + i)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord - i)][y(yCord + i)] in blackPieces:
                        boardInput[x(xCord - i)][y(yCord + i)] = highlight_red(boardInput[x(xCord - i)][y(yCord + i)])
                        validMoveStorage += [[xCord - i,yCord + i]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord - i)][y(yCord + i)] in whitePieces:
                        boardInput[x(xCord - i)][y(yCord + i)] = highlight_red(boardInput[x(xCord - i)][y(yCord + i)])
                        validMoveStorage += [[xCord - i,yCord + i]]
                    break
                boardInput[x(xCord - i)][y(yCord + i)] = highlight_red(boardInput[x(xCord - i)][y(yCord + i)])
                validMoveStorage += [[xCord - i, yCord + i]]

        # Top-right ↗
        for i in range(1, n):
            if (xCord + i <= 8 and yCord - i > 0):
                if boardInput[x(xCord + i)][y(yCord - i)] != emptySquare:
                    if boardInput[x(xCord)][y(yCord)] in whitePieces and boardInput[x(xCord + i)][y(yCord - i)] in blackPieces:
                        boardInput[x(xCord + i)][y(yCord - i)] = highlight_red(boardInput[x(xCord + i)][y(yCord - i)])
                        validMoveStorage += [[xCord + i,yCord - i]]
                    elif boardInput[x(xCord)][y(yCord)] in blackPieces and boardInput[x(xCord + i)][y(yCord - i)] in whitePieces:
                        boardInput[x(xCord + i)][y(yCord - i)] = highlight_red(boardInput[x(xCord + i)][y(yCord - i)])
                        validMoveStorage += [[xCord + i,yCord - i]]
                    break
                boardInput[x(xCord + i)][y(yCord - i)] = highlight_red(squboardInputare[x(xCord + i)][y(yCord - i)])
                validMoveStorage += [[xCord + i,yCord - i]]

    def knightPattern():
        global validMoveStorage
        knight_moves = [
            (-1, 2), (1, 2),
            (-1, -2), (1, -2),
            (2, 1), (2, -1),
            (-2, 1), (-2, -1)
        ]

        for dx, dy in knight_moves:
            nx, ny = xCord + dx, yCord + dy
            if 0 < nx <= 8 and 0 < ny <= 8:
                target = boardInput[x(nx)][y(ny)]
                current = boardInput[x(xCord)][y(yCord)]

                # Knight capture
                if current in whitePieces and target in blackPieces:
                    boardInput[x(nx)][y(ny)] = highlight_red(target)
                    validMoveStorage += [[nx, ny]]
                elif current in blackPieces and target in whitePieces:
                    boardInput[x(nx)][y(ny)] = highlight_red(target)
                    validMoveStorage += [[nx, ny]]
                # Knight move to empty square
                elif target == emptySquare:
                    boardInput[x(nx)][y(ny)] = highlight_red(target)
                    validMoveStorage += [[nx, ny]]

    # L pattern

    selectedPiece = boardInput[x(xCord)][y(yCord)]
    # Check which piece is selected to show the correct movement rules
    if (selectedPiece == bqueen or selectedPiece == wqueen):  # Queen can move all directions
        #print("found queen")
        vertical(8)
        horizontal(8)
        diagonal(8)
    elif (selectedPiece == brook or selectedPiece == wrook):
        #print("found rook")
        vertical(8)
        horizontal(8)
    elif (selectedPiece == bbishop or selectedPiece == wbishop):
        #print("found bishop")
        diagonal(8)
    elif (selectedPiece == bking or selectedPiece == wking):
        #print("found king")
        vertical(2)
        horizontal(2)
        diagonal(2)
    elif (selectedPiece == bpawn or selectedPiece == wpawn):
        #print("found pawn")
        if(yCord == 2 and selectedPiece == wpawn): # Start boost
            verticalPawn(3)
        elif(yCord == 7 and selectedPiece == bpawn):
            verticalPawn(3)
        else:
            verticalPawn(2)
    elif (selectedPiece == bknight or selectedPiece == wknight):
        #print("found knight")
        knightPattern()


# Piece selection by terminal input
def selectPiece():
    global translate
    global xCord, yCord
    global validMoveStorage
    piece = input("Which piece do you want to move?: ")
    selection = list(piece)
    if (selection[0] in translate and selection[1].isdigit()):
        xCord = translate[selection[0]]
        yCord = int(selection[1])
        if (square[x(xCord)][y(yCord)] != emptySquare):
            if (playerTurn == 'white' and square[x(xCord)][y(yCord)] in whitePieces)or(playerTurn == 'black' and square[x(xCord)][y(yCord)] in blackPieces):
                validMoveStorage = []
                checkValidMoves(xCord, yCord, square)  # Shows the possible moves in red
                square[x(xCord)][y(yCord)] = highlight_blue(unhighlight(square[x(xCord)][y(yCord)]))  # Selected piece is blue
                print_board()
                print(xCord)
                print(yCord)
                print(validMoveStorage)
            else:
                helpers.clear_screen()
                print_board()
                print("Not your piece...")
                selectPiece()
        else:
            helpers.clear_screen()
            print_board()
            print("Nothing here...")
            selectPiece()


def riscChecker():
    global validMoveStorage
    buffer = []
    result = []

    # Loop through each row of fakeSquare
    for y, row in enumerate(fakeSquare):  # y is the index of the row (0 to 7)
        # Loop through each item (square or piece) in the current row
        for x, item in enumerate(row):  # x is the index of the item (0 to 7)
            if (fakeSquare[y - 1][x - 1] in blackPieces):
                validMoveStorage = []  # Reset validMoveStorage for each item
                unhighlight_board(fakeSquare)  # Assuming this unhighlights all squares
                checkValidMoves(x + 1, y + 1, fakeSquare)  # Pass the coordinates and item to the function

            # Add the valid moves to the buffer (valid positions as (xPos, yPos) tuples)
            buffer += validMoveStorage  # validMoveStorage should be populated by checkValidMoves

    # Now populate the result with valid Unicode characters from square
    for move in buffer:
        xPos, yPos = move  # Get the coordinates of the valid move
        # Append the Unicode character from square[yPos][xPos] to result
        result.append(fakeSquare[yPos - 1][xPos - 1])  # Adjust for 0-based indexing
    return result



# Main loop
def gameLoop():
    gameOver = False
    global running
    global validMoveStorage
    global emptySquare
    global playerTurn
    global translate
    global xCord, yCord

    i = 0
    helpers.clear_screen()
    print_board()

    while(running==True):
        # Select piece
        selectPiece()


        # Select target
        move = input("Enter target square: ")
        target = list(move)
        if(move == "unselect"): # unselect
            validMoveStorage = []
            unhighlight_board(square)
            print_board()
        elif (target[0] in translate and target[1].isdigit()): # if input is valid
            xCordTarget = translate[target[0]]
            yCordTarget = int(target[1])
            proposedMove = [xCordTarget, yCordTarget]
            if (proposedMove in validMoveStorage):
                # If move is valid, we need to check if it would risk a mate
                # TODO add mate prevention
                if(square[x(xCord)][y(yCord)] == highlight_blue(bpawn) and yCordTarget == 1): # promote pawn
                    square[x(xCord)][y(yCord)] = bqueen
                elif(square[x(xCord)][y(yCord)] == highlight_blue(wpawn) and yCordTarget == 8):
                    square[x(xCord)][y(yCord)] = wqueen

                fakeSquare[x(xCordTarget)][y(yCordTarget)] = fakeSquare[x(xCord)][y(yCord)]
                fakeSquare[x(xCord)][y(yCord)] = emptySquare
                square[x(xCordTarget)][y(yCordTarget)] = square[x(xCord)][y(yCord)]
                square[x(xCord)][y(yCord)] = emptySquare
                # Reset
                validMoveStorage = []
                if (playerTurn == 'white'):
                    playerTurn = 'black'
                else:
                    playerTurn = 'white'
                unhighlight_board(square)
                unhighlight_board(fakeSquare)
                print_board()

                print_square(square)
                print_square(fakeSquare)
                print(riscChecker())


            else:
                validMoveStorage = []
                unhighlight_board(square)
                print_board()
                print("Illegal move.")




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