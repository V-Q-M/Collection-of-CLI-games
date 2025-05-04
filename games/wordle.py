import random

from utils import helpers
from utils.helpers import conn
from assets import valid_word_list, answer_word_list
from assets.valid_word_list import validWords
from assets.answer_word_list import answerWords

running = True


answer = answerWords[random.randint(0, len(answerWords) - 1)]
#answer = 'pingo'
hiddenWord = list(answer)
word = [[' ', ' ', ' ', ' ', ' '],  # Row 0
        [' ', ' ', ' ', ' ', ' '],  # Row 1
        [' ', ' ', ' ', ' ', ' '],  # Row 2
        [' ', ' ', ' ', ' ', ' '],  # Row 3
        [' ', ' ', ' ', ' ', ' '],  # Row 4
        [' ', ' ', ' ', ' ', ' ']]  # Row 5


def pickWord():
    global word
    global hiddenWord
    global answer
    # The list of displayed words need to be emptied
    word = [[' ', ' ', ' ', ' ', ' '],  # Row 0
            [' ', ' ', ' ', ' ', ' '],  # Row 1
            [' ', ' ', ' ', ' ', ' '],  # Row 2
            [' ', ' ', ' ', ' ', ' '],  # Row 3
            [' ', ' ', ' ', ' ', ' '],  # Row 4
            [' ', ' ', ' ', ' ', ' ']]  # Row 5
    # Pick the word
    answer = answerWords[random.randint(0, len(answerWords) - 1)]
    #answer = 'paper'
    hiddenWord = list(answer)



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
    global running
    global hiddenWord
    i = 0
    helpers.clear_screen()
    print_box()

    while(running==True):
        userGuess = input("Enter your guess: ").strip().lower()
        if(userGuess == "return"): # Return to main menu
            running = False
            break
        elif(len(userGuess) == 5): # Checks for valid length
            if(userGuess in validWords):
                potentialGuess = list(userGuess)
                for j in range(0,5):
                    if(potentialGuess[j] == answer[j]): # Letter matches, paint it green
                        word[i][j] = f"\033[32m{potentialGuess[j].upper()}\033[0m"
                        hiddenWord[j] = '-' # Change that letter, so that nonexistent duplicates don't get flagged falsely
                    elif(potentialGuess[j] in hiddenWord): # Word contains letter, paint it yellow
                        word[i][j] = f"\033[33m{potentialGuess[j].upper()}\033[0m"
                    else: # Letters is wrong
                        word[i][j] = potentialGuess[j].upper()
                hiddenWord = list(answer) # make the hiddenWord equal to answer again
                i += 1 # Increment row
                helpers.clear_screen()
                print_box()
            else:
                helpers.clear_screen()
                print_box()
                print("Word not recognized. Try again.")
            if(userGuess == answer): # Check if player won
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
    pickWord()
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
