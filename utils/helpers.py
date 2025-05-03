import os
import platform
import duckdb


# Clears the terminal
def clear_screen():
    system_name = platform.system()
    if system_name == 'Windows':
        os.system('cls')
    elif system_name in ('Linux', 'Darwin'):
        if os.getenv('TERM'):
            os.system('clear')
        else:
            print("\n" * 100)  # Fallback for non-interactive terminals
    else:
        print("\n" * 100)  # Generic fallback



# Activate Database
conn = duckdb.connect("CLI-GAMES-DATABASE.duckdb")
# Increment sequence
conn.execute("CREATE SEQUENCE IF NOT EXISTS inc START WITH 1 INCREMENT BY 1;")
# NumberGuesser table
conn.execute(""" 
            CREATE TABLE IF NOT EXISTS numberGuesserStats (
                game int PRIMARY KEY DEFAULT nextval('inc'),
                guesses int
                ); 
            """)
# TicTacToe table
conn.execute(""" 
            CREATE TABLE IF NOT EXISTS tictactoeStats (
                rounds int PRIMARY KEY DEFAULT nextval('inc'),
                winner text NOT NULL
                ); 
            """)
# Wordle table
conn.execute("""
            CREATE TABLE IF NOT EXISTS wordleStats (
                game int PRIMARY KEY DEFAULT nextval('inc'),
                guesses text
                );
            """)
running = True