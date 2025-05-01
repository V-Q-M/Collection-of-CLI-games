import random
import duckdb



# Activate Database
conn = duckdb.connect("numberGuesser.duckdb")
conn.execute("CREATE SEQUENCE IF NOT EXISTS inc START WITH 1 INCREMENT BY 1;")
conn.execute("""
            CREATE TABLE IF NOT EXISTS numberGuesserStats (
                game int PRIMARY KEY DEFAULT nextval('inc'),
                guesses int
                ); 
""")

running = True


# Game loop
def gameLoop(hiddenNumber):
    # Variables
    global running
    tries = 0
    guess = 0

    while guess != hiddenNumber:
        guess = input("Guess a number: ")
        tries += 1
        if (guess == "exit"):
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

# Iniate game
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


conn.close()