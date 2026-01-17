import os
import time
import msvcrt
import winsound
import importlib.util
from datetime import datetime

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "entertainment"
__group__ = "games"
__desc__ = "Tic-Tac-Toe PRO with History Logging and Sound Effects"

# Paths aligned with your settings
HISTORY_DIR = os.path.expandvars(r"%userprofile%\.polsoft\psCli\History\Games")
LOG_FILE = os.path.join(HISTORY_DIR, "game_history.txt")

# ANSI Colors
RESET = "\033[0m"
RED = "\033[91m"
BLUE = "\033[94m"
GRAY = "\033[90m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Added 'r' before the string to treat backslashes literally
LOGO = fr"""{RED}
 ______                 ______                        ______                  
/\__  _\__             /\__  _\                      /\__  _\                 
\/_/\ \/\_\    ___     \/_/\ \/    __      ___       \/_/\ \/    ___      __   
   \ \ \/\ \  /'___\       \ \ \  /'__`\   /'___\       \ \ \  / __`\  /'__`\\
    \ \ \ \ \/\ \__/        \ \ \/\ \L\.\_/\ \__/        \ \ \/\ \L\ \/\  __/ 
     \ \_\ \_\ \____\        \ \_\ \__/.\_\ \____\        \ \_\ \____/\ \____\\
      \/_/\/_/\/____/         \/_/\/__/\/_/\/____/      {GRAY}by{RESET}{RED} \/_/\/___/  \/____/
                                                          {GRAY}Sebastian Januchowski{RESET}"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_sound(event):
    if event == "error":
        winsound.Beep(400, 200)
    elif event == "win":
        winsound.Beep(523, 150); winsound.Beep(659, 150); winsound.Beep(784, 150)
    elif event == "draw":
        winsound.Beep(300, 500)

def log_result(winner):
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        result_text = f"Winner: {winner}" if winner != "Draw" else "Draw"
        f.write(f"[{timestamp}] TicTacToe - {result_text}\n")

def show_recent_history():
    if os.path.exists(LOG_FILE):
        print(f"{GRAY}Recent 5 games:{RESET}")
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-5:]:
                    print(f" {DIM}• {line.strip()}{RESET}")
        except Exception:
            pass
        print("-" * 30)

def print_board(board):
    print("") 
    for r in range(3):
        cols = []
        for c in range(3):
            cell = board[r][c]
            num = r * 3 + c + 1
            if cell == "X": cols.append(f"{RED}{BOLD}X{RESET}")
            elif cell == "O": cols.append(f"{BLUE}{BOLD}O{RESET}")
            else: cols.append(f"{DIM}{num}{RESET}")
        print(f"  {cols[0]}  {GRAY}|{RESET}  {cols[1]}  {GRAY}|{RESET}  {cols[2]}  ")
        if r < 2: print(f"{GRAY}-----------------{RESET}")
    print("")

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ": return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ": return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ": return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ": return board[0][2]
    return None

def start_match():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    while True:
        clear_screen()
        print(f"{BOLD}Tic Tac Toe Game{RESET}")
        show_recent_history()
        print_board(board)
        color = RED if current_player == "X" else BLUE
        print(f"Player {color}{current_player}{RESET} (select 1-9): ", end="", flush=True)
        try:
            char_b = msvcrt.getch()
            char = char_b.decode('utf-8')
            idx = int(char) - 1
            if idx < 0 or idx > 8: raise ValueError
            r, c = divmod(idx, 3)
            if board[r][c] != " ":
                play_sound("error"); continue
        except:
            play_sound("error"); continue

        board[r][c] = current_player
        winner = check_winner(board)
        if winner or all(cell != " " for row in board for cell in row):
            clear_screen()
            print(f"{BOLD}Tic Tac Toe Game{RESET}")
            print_board(board)
            result = winner if winner else "Draw"
            color_res = RED if result == "X" else (BLUE if result == "O" else GRAY)
            print(f"{BOLD}Game Over! Result: {color_res}{result}{RESET}")
            if winner: play_sound("win")
            else: play_sound("draw")
            log_result(result)
            return
        current_player = "O" if current_player == "X" else "X"

def main():
    """Główny punkt wejścia dla gry."""
    clear_screen()
    print(LOGO)
    time.sleep(2)
    while True:
        start_match()
        print(f"\nStart a new game? ({BOLD}y{RESET}/n)")
        try:
            key_b = msvcrt.getch()
            key = key_b.decode('utf-8').lower()
        except:
            key = 'n'
            
        if key != 'y':
            print("Thanks for playing!"); time.sleep(1); break

if __name__ == "__main__":
    main()