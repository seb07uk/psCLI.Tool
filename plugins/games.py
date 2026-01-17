import os
import sys
import re
import subprocess
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "entertainme."
__group__ = "menu"
__desc__ = "Games Center - dynamic launcher for console games"

HEADER = r"""
          ,o888888o.            .8.                    ,8.        ,8.            8 8888888888          d888888o.
         8888     `88.         .888.                  ,888.      ,888.           8 8888             .`8888:' `88.
      ,8 8888       `8.       :88888.                .`8888.    .`8888.          8 8888             8.`8888.    Y8
      88 8888                . `88888.              ,8.`8888. ,8. `8888.         8 8888             `8.`8888.
      88 8888               .8. `88888.            ,8'8.`8888,8^ 8.`8888.        8 888888888888     `8.`8888.
      88 8888              .8`8. `88888.          ,8' `8.`8888'  `8.`8888.       8 8888              `8.`8888.
      88 8888   8888888   .8' `8. `88888.        ,8'   `8.`88'    `8.`8888.      8 8888               `8.`8888.
      `8 8888       .8'  .8'   `8. `88888.      ,8'     `8.`'      `8.`8888.     8 8888           8b   `8.`8888.
         8888     ,88'  .888888888. `88888.    ,8'          `       `8.`8888.    8 8888           `8b.  ;8.`8888
          `8888888P'   .8'       `8. `88888.  ,8'                    `8.`8888.   8 888888888888    `Y8888P8P88P'
"""

GAMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "games"))

def get_metadata(file_path):
    """Reads game description without importing the file."""
    meta = {"desc": "No description"}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            desc_match = re.search(r'__desc__\s*=\s*["\'](.*?)["\']', content)
            if desc_match: meta["desc"] = desc_match.group(1)
    except: pass
    return meta

def show_help():
    """Displays help information for the Games Center."""
    print(f"\n{Color.BOLD}GAMES CENTER HELP{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 30}{Color.RESET}")
    print(f"{Color.GREEN}ID / Name{Color.RESET}   - Type the game ID or name to launch it.")
    print(f"{Color.GREEN}menu{Color.RESET}        - Return to the main TERMINAL CLI menu.")
    print(f"{Color.GREEN}help / h{Color.RESET}    - Show this help message.")
    print(f"{Color.GREEN}exit / q{Color.RESET}    - Close the launcher.")
    print(f"{Color.GRAY}{'=' * 30}{Color.RESET}")
    input("\nPress Enter to continue...")

@command(name="games", aliases=["play", "g"])
def games_dispatcher(*args):
    """Game launcher for TERMINAL CLI."""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.CYAN}{HEADER}{Color.RESET}")
        
        files = [f for f in os.listdir(GAMES_DIR) if f.endswith(".py") and f != "__init__.py"] if os.path.exists(GAMES_DIR) else []
        
        if not files:
            print(f"{Color.YELLOW}[!] No games found in /games folder.{Color.RESET}")
            input("Press Enter...")
            return

        print(f"{Color.BOLD}{'ID':<3} | {'GAME':<20} | {'DESCRIPTION'}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 80}{Color.RESET}")

        games_map = {}
        for idx, filename in enumerate(sorted(files), 1):
            name = filename[:-3]
            meta = get_metadata(os.path.join(GAMES_DIR, filename))
            games_map[str(idx)] = (name, os.path.join(GAMES_DIR, filename))
            games_map[name.lower()] = (name, os.path.join(GAMES_DIR, filename))
            print(f"{Color.GREEN}{idx:<3}{Color.RESET} | {Color.WHITE}{name:<20}{Color.RESET} | {meta['desc']}")

        while True:
            try:
                choice = input(f"\n{Color.CYAN}psGAMES > {Color.RESET}").strip().lower()
            except: return

            if choice in ['help', 'h', '?']:
                show_help()
                break # Refresh the main view after help

            if choice == 'menu':
                os.system('cls' if os.name == 'nt' else 'clear')
                return 

            if choice in ['q', 'exit', 'quit']:
                return

            if choice in games_map:
                game_name, path = games_map[choice]
                print(f"{Color.YELLOW}[*] Starting: {game_name}...{Color.RESET}")
                subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                print(f"{Color.RED}[!] Unknown command: {choice}. Type 'help' for options.{Color.RESET}")

if __name__ == "__main__":
    games_dispatcher()