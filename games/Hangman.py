import random
import os
import getpass  # Used to hide the entered password

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "entertainment"
__group__ = "games"
__desc__ = "A word game for 1-2 players, one thinks of a word and the other tries to guess it."

# Paths
BASE_DIR = os.path.expandvars(r'%userprofile%\.polsoft\games')
SCORE_FILE = os.path.join(BASE_DIR, "hiscores.txt")


def inicjalizuj():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)


def wyczysc_ekran():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_hangman_art(index):
    stages = [
        """
           +-------+
           |       |
                   |
                   |
                   |
                   |
        ==============
        """,
        """
           +-------+
           |       |
           O       |
                   |
                   |
                   |
        ==============
        """,
        """
           +-------+
           |       |
           O       |
           |       |
                   |
                   |
        ==============
        """,
        """
           +-------+
           |       |
           O       |
          /|       |
                   |
                   |
        ==============
        """,
        """
           +-------+
           |       |
           O       |
          /|\\      |
                   |
                   |
        ==============
        """,
        """
           +-------+
           |       |
           O       |
          /|\\      |
          /        |
                   |
        ==============
        """,
        """
           +-------+
           |       |
           O       |
          /|\\      |
          / \\      |
                   |
        ==============
        """
    ]
    return stages[index]


def logo():
    return """
    _    _                                         
   | |  | |                                        
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
   |  __  |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\ 
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
                        __/ |                      
                       |___/                       
    """


def zapisz_i_sortuj_wynik(nick, punkty):
    scores = []
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            for line in f.readlines()[1:]:
                if ":" in line:
                    try:
                        name_part = line.split(". ")[1]
                        name = name_part.split(":")[0].strip()
                        score = int(name_part.split(":")[1].replace(" pts", "").strip())
                        scores.append((name, score))
                    except:
                        continue

    scores.append((nick, punkty))
    scores.sort(key=lambda x: x[1], reverse=True)

    with open(SCORE_FILE, "w") as f:
        f.write("--- TOP 10 HIGH SCORES ---\n")
        for i, (n, p) in enumerate(scores[:10], 1):
            f.write(f"{i}. {n}: {p} pts\n")


def pokaz_hiscore():
    wyczysc_ekran()
    print("\033[93m" + "╔════════════════════════════════════╗")
    print("║            HIGH SCORE TABLE        ║")
    print("╚════════════════════════════════════╝\033[0m")

    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            print(f.read())
    else:
        print("No saved scores.")

    input("\nPress Enter...")


def help_section():
    wyczysc_ekran()

    print("\033[96m" + "═══════════════════════════════════════════════")
    print("                     H E L P")
    print("═══════════════════════════════════════════════\033[0m\n")

    # GAME OBJECTIVE
    print("\033[93m▶ GAME OBJECTIVE\033[0m")
    print("Your goal is to guess the hidden word before the error counter reaches its maximum.\n")

    # GAME MODES
    print("\033[92m▶ GAME MODES\033[0m")
    print("\033[92m1. Single Player (VS CPU)\033[0m")
    print("   • The game selects a random word.")
    print("   • You earn points for each correct letter.")
    print("   • You receive a bonus for remaining lives.\n")

    print("\033[92m2. Two Players (VS Player)\033[0m")
    print("   • Player 1 enters a hidden word.")
    print("   • Player 2 tries to guess it.\n")

    # SCORING
    print("\033[95m▶ SCORING\033[0m")
    print("   • \033[92m+10 points\033[0m for each correct letter.")
    print("   • \033[96mBonus:\033[0m (6 – number of mistakes) × 25 points.")
    print("   • Results are saved in the TOP 10 high score table.\n")

    # RULES
    print("\033[94m▶ RULES\033[0m")
    print("   • Enter one letter at a time.")
    print("   • Only alphabetic characters are allowed.")
    print("   • Letters already used cannot be repeated.\n")

    # HIGH SCORE
    print("\033[91m▶ HIGH SCORE TABLE\033[0m")
    print("   • Saved in: \033[93m%userprofile%\\.polsoft\\games\\hiscores.txt\033[0m")
    print("   • Automatically sorted by score.\n")

    # GAME END
    print("\033[90m▶ GAME END\033[0m")
    print("   • Win: You guess the entire word.")
    print("   • Lose: You reach 6 mistakes.\n")

    # CONTROLS
    print("\033[96m▶ CONTROLS\033[0m")
    print("   • Select menu options by entering their number.")
    print("   • During the game, type letters and press Enter.\n")

    # FOOTER
    print("\033[90m" + "─" * 55 + "\033[0m")
    print("\033[97m" + " " * 15 + "Sebastian Januchowski")
    print(" " * 15 + "polsoft.its@fastservice.com")
    print(" " * 15 + "https://github.com/seb07uk")
    print(" " * 15 + "2026© polsoft.ITS London\033[0m")
    print("\033[90m" + "─" * 55 + "\033[0m\n")

    input("Press Enter...")


def silnik_gry(word, tryb_2_graczy=False):
    guessed = []
    errors = 0
    max_errors = 6
    letter_points = 0

    while errors < max_errors:
        wyczysc_ekran()
        print("\033[96m" + logo() + "\033[0m")

        if tryb_2_graczy:
            print("         [ 2 PLAYER MODE ]")

        print(get_hangman_art(errors))

        state = "".join([f" {l} " if l in guessed else " _ " for l in word])
        print(f"\n   WORD: {state}")
        print(f"\n   ERRORS: {errors}/{max_errors}  |  POINTS: {letter_points}")
        print(f"   USED: {', '.join(guessed)}")
        print("   " + "─" * 40)

        if "_" not in state:
            total = letter_points + (max_errors - errors) * 25
            print(f"\n\033[92m   VICTORY! FINAL SCORE: {total}\033[0m")
            nick = input("   Enter the winner's nickname: ")
            zapisz_i_sortuj_wynik(nick, total)
            return

        guess = input("\n   Enter a letter > ").upper()
        if len(guess) != 1 or not guess.isalpha() or guess in guessed:
            continue

        guessed.append(guess)

        if guess in word:
            letter_points += word.count(guess) * 10
        else:
            errors += 1

    wyczysc_ekran()
    print(get_hangman_art(6))
    print(f"\033[91m   GAME OVER. THE WORD WAS: {word}\033[0m")
    nick = input("   Enter your nickname (even though you lost): ")
    zapisz_i_sortuj_wynik(nick, letter_points)


def menu():
    inicjalizuj()
    while True:
        wyczysc_ekran()
        print("\033[95m" + logo() + "\033[0m")
        print("       [1] NEW GAME (VS CPU)")
        print("       [2] 2 PLAYERS (VS PLAYER)")
        print("       [3] HIGH SCORES")
        print("       [4] HELP")
        print("       [5] EXIT")
        print("\n" + "       " + "═" * 25)

        choice = input("\n       SELECT: ")

        if choice == "1":
            words = ["PYTHON", "TERMINAL", "SCRIPT", "CODING", "INTERFACE", "SYSTEM"]
            silnik_gry(random.choice(words))

        elif choice == "2":
            wyczysc_ekran()
            print("\033[93m" + "=== 2 PLAYER MODE ===\033[0m")
            print("Player 1, enter the secret word (input will be hidden):")
            secret = getpass.getpass("Word: ").upper()

            if secret.isalpha() and len(secret) > 0:
                silnik_gry(secret, tryb_2_graczy=True)
            else:
                print("Invalid word! It must contain letters only.")
                input("Press Enter...")

        elif choice == "3":
            pokaz_hiscore()

        elif choice == "4":
            help_section()

        elif choice == "5":
            break


if __name__ == "__main__":
    menu()