# --- PLUGIN METADATA (Read by Dispatcher._load_python_module) ---
__author__ = "Sebastian Januchowski"
__category__ = "games"
__group__ = "entertainment"
__desc__ = "Retro arcade snake game with skins, difficulty levels and high-score ranking."

import os
import time
import random
import sys
import msvcrt
import ctypes
import json

# Enable ANSI color support for TERMINAL CLI
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# System paths
GAMES_DIR = os.path.expandvars(r"%userprofile%\.polsoft\psCli\Games")
SNAKE_DATA = os.path.join(GAMES_DIR, "snake.json")

# Control sequences
ESC = "\033["
RESET, HIDE, SHOW, TOP = f"{ESC}0m", f"{ESC}?25l", f"{ESC}?25h", f"{ESC}H"
BLUE = f"{ESC}38;2;148;194;224m"
GREEN = f"{ESC}38;2;50;168;82m"
WHITE = f"{ESC}38;2;255;255;255m"
RED = f"{ESC}38;2;212;38;61m"
YELLOW = f"{ESC}38;2;235;180;52m"
DEAD_COL = f"{ESC}38;2;41;100;138m"

SKINS = {
    "1": (f"{ESC}38;2;105;78;148m▒", f"{ESC}38;2;184;20;184m▓"),
    "2": (f"{ESC}38;2;235;180;52m♣", f"{ESC}38;2;209;109;38m♥"),
    "3": (f"{ESC}38;2;212;38;61m◙", f"{ESC}38;2;222;100;116m◘")
}

difficulty = {"level": 1, "speed": 0.12, "multiplier": 1, "name": "Easy"}

def load_scores():
    if os.path.exists(SNAKE_DATA):
        try:
            with open(SNAKE_DATA, 'r', encoding='utf-8') as f: return json.load(f)
        except: return []
    return []

def save_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score, "date": time.strftime("%Y-%m-%d")})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    if not os.path.exists(GAMES_DIR): os.makedirs(GAMES_DIR)
    with open(SNAKE_DATA, 'w', encoding='utf-8') as f: json.dump(scores, f, indent=4)

def draw_logo():
    print(f"{WHITE}          Sebastian Januchowski{RESET}")
    print(f"""{GREEN}      _____ _   _2026©  _  _____ 
     /  ___| \ | |/ _ \| |/ / __|
     \ `--.|  \| | |_| | ' /| _| 
      `--. \ |\  |  _  |  < | |__ 
     \____/\_| \_|_| |_|_|\_\____|{RESET}""")

def show_options():
    global difficulty
    while True:
        os.system("cls")
        print(f"{BLUE}=== OPTIONS & SETTINGS ==={RESET}\n")
        print(f"{WHITE}Current Level: {YELLOW}{difficulty['name']}{RESET}")
        print(f"{WHITE}Score Multiplier: {YELLOW}x{difficulty['multiplier']}{RESET}\n")
        print(f"{WHITE}[1] Level 1 (Easy)   - 1 pt")
        print(f"[2] Level 2 (Normal) - 2 pts")
        print(f"[3] Level 3 (Hard)   - 3 pts")
        print(f"\n{RED}[R] RESET RANKING{RESET}")
        print(f"{BLUE}[B] Back to menu{RESET}")
        c = msvcrt.getch().decode().upper()
        if c == '1': difficulty = {"level": 1, "speed": 0.12, "multiplier": 1, "name": "Easy"}
        elif c == '2': difficulty = {"level": 2, "speed": 0.08, "multiplier": 2, "name": "Normal"}
        elif c == '3': difficulty = {"level": 3, "speed": 0.04, "multiplier": 3, "name": "Hard"}
        elif c == 'R':
            print(f"\n{RED}Are you sure you want to clear rankings? (Y/N){RESET}")
            if msvcrt.getch().decode().upper() == 'Y':
                if os.path.exists(SNAKE_DATA): os.remove(SNAKE_DATA)
                print(f"{GREEN}Rankings cleared!{RESET}")
                time.sleep(1)
        elif c == 'B': break

def show_top5():
    os.system("cls")
    print(f"{BLUE}=== TOP 5 HIGH SCORES ==={RESET}\n")
    scores = load_scores()[:5]
    if not scores: print(f"{WHITE}No scores recorded yet.{RESET}")
    for i, s in enumerate(scores, 1):
        print(f"{WHITE}{i}. {s['name']:<12} - {s['score']:03} pts{RESET}")
    print(f"\n{BLUE}Press any key...{RESET}")
    msvcrt.getch()

class SnakeGame:
    def __init__(self, w=30, h=20):
        self.w, self.h = w, h
        self.reset()
    def reset(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.dir = 'D'
        self.pellet = (random.randint(2, self.w-1), random.randint(2, self.h-1))
        self.dead = False
        self.current_score = 0
    def render(self, s1, s2):
        buf = TOP + HIDE
        for y in range(1, self.h + 1):
            row = ""
            for x in range(1, self.w + 1):
                if x == 1 or x == self.w or y == 1 or y == self.h: row += f"{BLUE}█"
                elif (x, y) == self.pellet: row += f"{GREEN}■"
                elif (x, y) in self.snake: row += s1 if self.snake.index((x,y))%2==0 else s2
                else: row += " "
            buf += row + "\n"
        buf += f"{RESET}{WHITE}Score: {self.current_score} | Lvl: {difficulty['level']} | Q: Quit{RESET}"
        sys.stdout.write(buf)
        sys.stdout.flush()
    def update(self):
        hx, hy = self.snake[0]
        if self.dir == 'W': hy -= 1
        elif self.dir == 'S': hy += 1
        elif self.dir == 'A': hx -= 1
        elif self.dir == 'D': hx += 1
        if hx <= 1 or hx >= self.w or hy <= 1 or hy >= self.h or (hx, hy) in self.snake:
            self.dead = True
            return
        self.snake.insert(0, (hx, hy))
        if (hx, hy) == self.pellet:
            self.current_score += difficulty['multiplier']
            self.pellet = (random.randint(2, self.w-1), random.randint(2, self.h-1))
        else: self.snake.pop()

def show_help():
    os.system("cls")
    print(f"{BLUE}=== SNAKE CLI: ABOUT ==={RESET}")
    print(f"{WHITE}Snake CLI is a classic arcade game")
    print("ported to the Python environment.")
    print("You play as a digital snake whose")
    print("only goal is to consume data (■).")
    print("The more you eat, the longer you get")
    print(f"and the harder it is to avoid a crash.{RESET}")
    print(f"\n{BLUE}=== INSTRUCTIONS ==={RESET}")
    print(f"{WHITE}Move:       W, A, S, D")
    print("Exit:       Q (during gameplay)")
    print(f"Scoring:    Lvl 1=1pt, 2=2pts, 3=3pts{RESET}")
    print(f"\n{BLUE}-------------------------------{RESET}")
    print(f"{WHITE}Author:  Sebastian Januchowski")
    print("Email:   polsoft.its@fastservice.com")
    print(f"GitHub:  https://github.com/seb07uk{RESET}")
    print(f"{BLUE}-------------------------------{RESET}")
    print(f"\n{WHITE}Press any key to return...{RESET}")
    msvcrt.getch()

def main_menu():
    os.system("mode con: cols=35 lines=25")
    while True:
        os.system("cls")
        sys.stdout.write(SHOW)
        print(f"{BLUE}      S N A K E   C L I{RESET}")
        print(f"{BLUE}==============================={RESET}\n")
        print(f"{WHITE}[1] NEW GAME\n[2] OPTIONS\n[3] TOP 5 RANKING\n[4] HELP\n{RED}[5] EXIT{RESET}\n")
        print(f"{BLUE}==============================={RESET}")
        c = msvcrt.getch().decode()
        if c == '1': start_game_flow()
        elif c == '2': show_options()
        elif c == '3': show_top5()
        elif c == '4': show_help()
        elif c == '5': sys.exit()

def start_game_flow():
    os.system("cls")
    sys.stdout.write(SHOW)
    name = input(f"{WHITE}Enter Name: {RESET}").strip()[:10] or "Player"
    sys.stdout.write(HIDE)
    
    while True:
        os.system("cls")
        draw_logo()
        print(f"\n{WHITE}Select your snake skin:{RESET}")
        for k, v in SKINS.items():
            print(f"[{k}] {v[0]}{v[1]}{v[0]}{RESET}")
        
        skin_choice = msvcrt.getch().decode()
        if skin_choice in SKINS:
            skin = SKINS[skin_choice]
            break
        skin = SKINS["1"]
        break
    
    game = SnakeGame()
    while True:
        game.reset()
        while not game.dead:
            if msvcrt.kbhit():
                k = msvcrt.getch().decode().upper()
                if k in "WASD":
                    opp = {"W":"S","S":"W","A":"D","D":"A"}
                    if k != opp.get(game.dir): game.dir = k
                if k == "Q": return
            game.update()
            game.render(skin[0], skin[1])
            time.sleep(difficulty['speed'])
        save_score(name, game.current_score)
        sys.stdout.write(TOP + DEAD_COL + (("X" * game.w + "\n") * game.h) + SHOW)
        print(f"\n{RED}GAME OVER!{RESET} Your Score: {game.current_score}")
        print(f"{WHITE}Do you want to play again? (Y/N){RESET}")
        if msvcrt.getch().decode().upper() != 'Y': return

def main():
    main_menu()

if __name__ == "__main__":
    main()
