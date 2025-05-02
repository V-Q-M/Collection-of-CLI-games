import os
import platform
import duckdb


# Clears the terminal
def clear_screen():
    system_name = platform.system()
    # pick the correct clear command
    if system_name == 'Windows':
        os.system('cls')
    elif system_name in ('Linux', 'Darwin'):
        if 'TERM' in os.environ:
            os.system('clear')
        else:
            print("\n" * 100)  # Fallback


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
running = True