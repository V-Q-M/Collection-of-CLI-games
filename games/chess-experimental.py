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
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [wpawn,  wpawn,  wpawn,  wpawn,  wpawn,  wpawn,  wpawn,  wpawn],
    [wrook,  wknight,  wbishop,  wqueen,  wking,  wbishop,  wknight,  wrook],
]

# Does the visuals
emptySquare = ' '

position_matrix = [
    [wrook, wknight, wbishop, wqueen, wking, wbishop, wknight, wrook],
    [wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn, wpawn],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare, emptySquare],
    [bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn, bpawn],
    [brook, bknight, bbishop, bqueen, bking, bbishop, bknight, brook],

]



def print_board(board):
    global playerTurn
    #helpers.clear_screen()

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
    global board_square
    selection_prompt = input("Which piece do you want to move?: ")
    start = list(selection_prompt)
    starty = translate[start[0]]
    startx = int(start[1])
    print(board[startx-1][starty - 1])
    board_square[8 - startx][starty -1 ] = highlight_blue(board_square[8 - startx][starty - 1])
    print_board(board_square)

    # Next step pick target
    select_target(startx, starty, position_matrix)


def select_target(startx, starty, board):
    global translate
    target_prompt = input("Enter target square: ")
    target = list(target_prompt)
    yaxis = translate[target[0]]
    xaxis = int(target[1])
    print(xaxis, yaxis)

    # Check move
    query(board)
    # Get valid moves and attacks for selected piece
    potentialMoves, potentialAttacks = checkValidity(startx - 1, starty - 1, board[startx - 1][starty - 1], board)

    # If the target position is a legal move
    if (xaxis - 1, yaxis - 1) in potentialMoves:
        # Update internal board state
        board[xaxis - 1][yaxis - 1] = board[startx - 1][starty - 1]
        board[startx - 1][starty - 1] = " "

        # Update visual board (Y flipped for display)
        board_square[8 - xaxis][yaxis - 1] = board_square[8 - startx][starty - 1]
        board_square[8 - startx][starty - 1] = " "

        print_board(board_square)


def query(board):
    buffer = []
    result = []

    white_pieces = {wking, wqueen, wbishop, wknight, wrook, wpawn}
    black_pieces = {bking, bqueen, bbishop, bknight, brook, bpawn}

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece not in white_pieces:
                continue  # skip non-white pieces

            valid_moves, valid_attacks = checkValidity(i, j, piece, board)

            for x, y in valid_attacks:
                if 0 <= x < 8 and 0 <= y < 8:
                    target = board[x][y]
                    if target in black_pieces:
                        result.append((piece, (i, j), "attacks", target, (x, y)))

    for entry in result:
        print(entry)




def checkValidity(xpos, ypos, piece, board):
    valid_moves = []
    valid_attacks = []

    is_white = piece in {wking, wqueen, wbishop, wknight, wrook, wpawn}
    is_black = piece in {bking, bqueen, bbishop, bknight, brook, bpawn}

    def is_enemy(x, y):
        if not (0 <= x < 8 and 0 <= y < 8):
            return False
        target = board[x][y]
        if target == " ":
            return False
        return (is_white and target in {bking, bqueen, bbishop, bknight, brook, bpawn}) or \
               (is_black and target in {wking, wqueen, wbishop, wknight, wrook, wpawn})

    def vertical(range_limit):
        for dy in [1, -1]:  # up, down
            for step in range(1, range_limit):
                y = ypos + dy * step
                if not (0 <= y < 8):
                    break
                target = board[xpos][y]
                if target == " ":
                    valid_moves.append((xpos, y))
                elif is_enemy(xpos, y):
                    valid_attacks.append((xpos, y))
                    break
                else:
                    break

    def horizontal(range_limit):
        for dx in [1, -1]:  # right, left
            for step in range(1, range_limit):
                x = xpos + dx * step
                if not (0 <= x < 8):
                    break
                target = board[x][ypos]
                if target == " ":
                    valid_moves.append((x, ypos))
                elif is_enemy(x, ypos):
                    valid_attacks.append((x, ypos))
                    break
                else:
                    break

    def diagonal(range_limit):
        for dx, dy in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            for step in range(1, range_limit):
                x = xpos + dx * step
                y = ypos + dy * step
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                target = board[x][y]
                if target == " ":
                    valid_moves.append((x, y))
                elif is_enemy(x, y):
                    valid_attacks.append((x, y))
                    break
                else:
                    break

    def pawnPattern():
        direction = 1 if piece == wpawn else -1
        start_row = 1 if piece == bpawn else 6

        # Forward one
        forward_one = ypos + direction
        if 0 <= forward_one < 8 and board[xpos][forward_one] == " ":
            valid_moves.append((xpos, forward_one))

            # Forward two from starting rank
            forward_two = ypos + 2 * direction
            if ypos == start_row and board[xpos][forward_two] == " ":
                valid_moves.append((xpos, forward_two))

        # Diagonal attacks
        for dx in [-1, 1]:
            x = xpos + dx
            y = ypos + direction
            if 0 <= x < 8 and 0 <= y < 8:
                if is_enemy(x, y):
                    valid_attacks.append((x, y))

    def knightPattern():
        jumps = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]
        for dx, dy in jumps:
            x = xpos + dx
            y = ypos + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if board[x][y] == " ":
                    valid_moves.append((x, y))
                elif is_enemy(x, y):
                    valid_attacks.append((x, y))

    # Apply movement rules
    if piece in [wqueen, bqueen]:
        vertical(8)
        horizontal(8)
        diagonal(8)
    elif piece in [wrook, brook]:
        vertical(8)
        horizontal(8)
    elif piece in [wbishop, bbishop]:
        diagonal(8)
    elif piece in [wking, bking]:
        vertical(2)
        horizontal(2)
        diagonal(2)
    elif piece in [wpawn, bpawn]:
        pawnPattern()
    elif piece in [wknight, bknight]:
        knightPattern()

    return valid_moves, valid_attacks



def gameLoop():
    global running
    global board_square
    global position_matrix

    #helpers.clear_screen()
    print_board(board_square)
    while(running==True):
        select_start(position_matrix)


























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

#startGame()