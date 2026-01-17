# --- PLUGIN METADATA (Read by Dispatcher._load_python_module) ---
__author__ = "Sebastian Januchowski"
__category__ = "games"
__group__ = "entertainment"
__desc__ = "Professional Rock-Paper-Scissors engine with persistent stats and contact info."

import os
import random
import sys
import msvcrt
import ctypes
import json

# Inicjalizacja kolorów ANSI dla TERMINAL CLI
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Ścieżki i ustawienia
SAVE_PATH = os.path.expandvars(r"%userprofile%\.polsoft\psCli\Games\rock-paper-scissors.json")
GAMES_DIR = os.path.dirname(SAVE_PATH)

# Sekwencje sterujące
ESC = "\033["
RESET, DIM, CYAN = f"{ESC}0m", f"{ESC}2m", f"{ESC}1;3;36m"
YELLOW, GREEN, RED, MAGENTA = f"{ESC}33m", f"{ESC}1;5;32m", f"{ESC}1;5;31m", f"{ESC}1;5;35m"
WHITE = f"{ESC}38;2;255;255;255m"

class RPSGame:
    def __init__(self):
        self.lang = None
        self.width = 30
        self.stats = self.load_stats()

    def load_stats(self):
        if os.path.exists(SAVE_PATH):
            try:
                with open(SAVE_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return {"wins": 0, "losses": 0, "draws": 0}

    def save_stats(self):
        if not os.path.exists(GAMES_DIR):
            os.makedirs(GAMES_DIR)
        with open(SAVE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=4)

    def draw_header(self, title):
        os.system("cls")
        author, brand = "2026 Sebastian Januchowski", "polsoft.ITS London"
        border = "=" * self.width
        print(f"{DIM}{author.center(self.width)}{RESET}")
        print(f"{CYAN}{border}{RESET}")
        print(f"{CYAN}{title.center(self.width).upper()}{RESET}")
        print(f"{CYAN}{border}{RESET}")
        print(f"{DIM}{brand.center(self.width)}{RESET}\n")

    def show_help(self):
        h_title = "POMOC / INFO" if self.lang == 'PL' else "HELP / ABOUT"
        self.draw_header(h_title)
        
        if self.lang == 'PL':
            print(f"{WHITE}O GRZE:{RESET}")
            print("Klasyczny symulator teorii gier.")
            print("Rywalizuj z algorytmem losowym.")
            print(f"\n{WHITE}ZASADY:{RESET}")
            print("- Kamień tępi Nożyce")
            print("- Nożyce tną Papier")
            print("- Papier owija Kamień")
        else:
            print(f"{WHITE}ABOUT:{RESET}")
            print("Classic game theory simulator.")
            print("Compete against a random logic.")
            print(f"\n{WHITE}RULES:{RESET}")
            print("- Rock blunts Scissors")
            print("- Scissors cut Paper")
            print("- Paper wraps Rock")

        print(f"\n{CYAN}------------------------------{RESET}")
        print(f"{WHITE}Autor:   Sebastian Januchowski")
        print("Email:   polsoft.its@fastservice.com")
        print(f"GitHub:  https://github.com/seb07uk{RESET}")
        print(f"{CYAN}------------------------------{RESET}")
            
        print(f"\n{DIM}{'Powrót / Back...'.center(self.width)}{RESET}")
        msvcrt.getch()

    def select_language(self):
        self.draw_header("SELECT LANGUAGE")
        print(f"{YELLOW}[1] Polski")
        print(f"[2] English{RESET}\n")
        print(f"{DIM}Choice (Press key):{RESET}")
        while True:
            c = msvcrt.getch().decode()
            if c == '1': self.lang = 'PL'; break
            if c == '2': self.lang = 'EN'; break

    def play(self):
        texts = {
            'PL': {
                'title': "KAMIEN - PAPIER - NOZYCE",
                'choose': "Wybierz ruch:",
                'moves': ["Kamien", "Papier", "Nozyce"],
                'help': "Pomoc", 'exit': "Zakoncz",
                'you': "Ty:", 'comp': "PC:",
                'draw': "Remis!", 'win': "Wygrales!", 'lose': "Przegrales!",
                'cont': "Dowolny klawisz...",
                'stat_line': "W: {wins} | P: {losses} | R: {draws}"
            },
            'EN': {
                'title': "ROCK - PAPER - SCISSORS",
                'choose': "Choose your move:",
                'moves': ["Rock", "Paper", "Scissors"],
                'help': "Help", 'exit': "Exit",
                'you': "You:", 'comp': "PC:",
                'draw': "Draw!", 'win': "You win!", 'lose': "You lose!",
                'cont': "Press any key...",
                'stat_line': "W: {wins} | L: {losses} | D: {draws}"
            }
        }

        t = texts[self.lang]
        while True:
            self.draw_header(t['title'])
            stat_str = t['stat_line'].format(**self.stats)
            print(f"{DIM}{stat_str.center(self.width)}{RESET}\n")
            
            print(f"{CYAN}{t['choose'].center(self.width)}{RESET}\n")
            for i, move in enumerate(t['moves'], 1):
                print(f"{YELLOW}  [{i}] {move}{RESET}")
            print(f"{YELLOW}  [H] {t['help']}{RESET}")
            print(f"{YELLOW}  [Q] {t['exit']}{RESET}\n")

            choice = msvcrt.getch().decode().upper()
            if choice == 'Q': break
            if choice == 'H': self.show_help(); continue
            if choice not in ['1', '2', '3']: continue

            p_idx = int(choice) - 1
            c_idx = random.randint(0, 2)
            
            self.draw_header(t['title'])
            print(f"{YELLOW}{t['you']:<10}{RESET} {t['moves'][p_idx]}")
            print(f"{YELLOW}{t['comp']:<10}{RESET} {t['moves'][c_idx]}\n")

            if p_idx == c_idx:
                print(f"{MAGENTA}{t['draw'].center(self.width)}{RESET}")
                self.stats["draws"] += 1
            elif (p_idx == 0 and c_idx == 2) or (p_idx == 1 and c_idx == 0) or (p_idx == 2 and c_idx == 1):
                print(f"{GREEN}{t['win'].center(self.width)}{RESET}")
                self.stats["wins"] += 1
            else:
                print(f"{RED}{t['lose'].center(self.width)}{RESET}")
                self.stats["losses"] += 1

            self.save_stats()
            print(f"\n{DIM}{t['cont'].center(self.width)}{RESET}")
            msvcrt.getch()

if __name__ == "__main__":
    os.system("mode con: cols=35 lines=25")
    game = RPSGame()
    game.select_language()
    game.play()