import os
import platform
import subprocess
import sys

try:
    import duckdb
except ImportError:
    choice = input("\nMissing required module 'duckdb'. Install it now? (y/n): ").strip().lower()
    if choice == 'y':
        subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb"])
        import duckdb
    else:
        print("Exiting. 'duckdb' is required.")
        sys.exit(1)


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
conn.execute("CREATE SEQUENCE IF NOT EXISTS inc1 START WITH 1 INCREMENT BY 1;")
# NumberGuesser table
conn.execute(""" 
            CREATE TABLE IF NOT EXISTS numberGuesserStats (
                game int PRIMARY KEY DEFAULT nextval('inc1'),
                guesses int
                ); 
            """)
# TicTacToe table
conn.execute("CREATE SEQUENCE IF NOT EXISTS inc2 START WITH 1 INCREMENT BY 1;")
conn.execute(""" 
            CREATE TABLE IF NOT EXISTS tictactoeStats (
                rounds int PRIMARY KEY DEFAULT nextval('inc2'),
                winner text NOT NULL
                ); 
            """)
# Wordle table
conn.execute("CREATE SEQUENCE IF NOT EXISTS inc3 START WITH 1 INCREMENT BY 1;")
conn.execute("""
            CREATE TABLE IF NOT EXISTS wordleStats (
                game int PRIMARY KEY DEFAULT nextval('inc3'),
                guesses text
                );
            """)
# Chess table
conn.execute("CREATE SEQUENCE IF NOT EXISTS inc4 START WITH 1 INCREMENT BY 1;")
conn.execute("""
            CREATE TABLE IF NOT EXISTS chessStats (
                game int PRIMARY KEY DEFAULT nextval('inc4'),
                turns text,
                winner text
                );
            """)
running = True