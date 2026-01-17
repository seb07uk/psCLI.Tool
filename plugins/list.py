# --- METADATA (Read by cli.py dispatcher) ---
__author__ = "Sebastian Januchowski"
__category__ = "file list"
__group__ = "system"
__desc__ = "Terminal file list generator."
# ---------------------------------------------

import os
import datetime
import msvcrt
import json
from cli import command

# ============================================
#  KONFIGURACJA ŚCIEŻEK (TERMINAL CLI)
# ============================================
USER_PROFILE = os.environ["USERPROFILE"]
HOME_DIR = r"C:\Users\%userprofile%\.polsoft\psCLI".replace("%userprofile%", os.environ["USERNAME"])
LOG_DIR = os.path.join(HOME_DIR, "Log")
LOG_FILE = os.path.join(LOG_DIR, "List.log")

# Ścieżka ustawień
SETTINGS_DIR = os.path.join(HOME_DIR, "settings")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "FileList.json")

# Inicjalizacja folderów systemowych
for d in [LOG_DIR, SETTINGS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# Kolory ANSI
GREEN, YELLOW, RED, BLUE, CYAN, RESET = "\033[92m", "\033[93m", "\033[91m", "\033[94m", "\033[96m", "\033[0m"

# ============================================
#  ZARZĄDZANIE USTAWIENIAMI
# ============================================
def load_settings():
    default = {
        "src": os.getcwd(),
        "output": os.path.join(USER_PROFILE, "Desktop", "list.txt")
    }
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"{RED}✖ Błąd zapisu w settings/FileList.json: {e}{RESET}")

# Ładowanie bieżącego stanu
state = load_settings()

def log_event(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================
#  GŁÓWNE OPERACJE
# ============================================
def generate_list(mode, ext=""):
    try:
        src = state["src"]
        if mode == "1":
            items = os.listdir(src)
            desc = "pliki i foldery"
        elif mode == "2":
            items = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
            desc = "tylko pliki"
        elif mode == "4":
            items = [f for f in os.listdir(src) if f.lower().endswith(f".{ext.lower()}")]
            desc = f"filtr *.{ext}"
        
        with open(state["output"], "w", encoding="utf-8") as f:
            for item in items:
                f.write(f"{item}\n")
        
        log_event(f"Wygenerowano listę ({desc}) do {state['output']}")
        
        # Podgląd (odpowiednik komendy type)
        clear()
        print(f"{GREEN}✔ Gotowe: {desc}{RESET}\n")
        print(f"{CYAN}--- TREŚĆ PLIKU ---{RESET}")
        with open(state["output"], "r", encoding="utf-8") as f:
            print(f.read())
        print(f"{CYAN}-------------------{RESET}\nNaciśnij dowolny klawisz...")
        msvcrt.getch()
    except Exception as e:
        print(f"{RED}✖ Błąd operacji: {e}{RESET}")
        os.system("pause")

# ============================================
#  INTERFEJS UŻYTKOWNIKA
# ============================================
def main():
    log_event("Uruchomiono moduł FileList")
    while True:
        clear()
        print(f"{CYAN}============================================{RESET}")
        print(f"{GREEN}       TERMINAL CLI - GENERATOR LISTY{RESET}")
        print(f"{CYAN}============================================{RESET}\n")
        print(f"Katalog źródłowy: {YELLOW}{state['src']}{RESET}")
        print(f"Plik wynikowy:    {YELLOW}{state['output']}{RESET}\n")
        print(f" {BLUE}[Z]{RESET} Zmień źródło   {BLUE}[L]{RESET} Zmień zapis")
        print(f" {BLUE}[1]{RESET} Pliki+Foldery  {BLUE}[2]{RESET} Tylko pliki")
        print(f" {BLUE}[4]{RESET} Filtr rozszerz. {BLUE}[0]{RESET} Wyjście\n")
        
        key = msvcrt.getch().decode().lower()
        
        if key == 'z':
            path = input("► Podaj nową ścieżkę źródłową: ")
            if os.path.exists(path):
                state["src"] = path
                save_settings(state)
            else:
                print(f"{RED}Błąd: Ścieżka nie istnieje!{RESET}")
                msvcrt.getch()
        elif key == 'l':
            print("\n[D] Pulpit | [S] Źródło | [C] Inna ścieżka")
            opt = msvcrt.getch().decode().lower()
            if opt == 'd': state["output"] = os.path.join(USER_PROFILE, "Desktop", "list.txt")
            elif opt == 's': state["output"] = os.path.join(state["src"], "list.txt")
            elif opt == 'c': state["output"] = input("► Pełna ścieżka z nazwą: ")
            save_settings(state)
        elif key == '1': generate_list("1")
        elif key == '2': generate_list("2")
        elif key == '4':
            ext = input("► Podaj rozszerzenie (np. py): ")
            generate_list("4", ext)
        elif key == '0':
            break

@command(name="list", aliases=["lg", "listgen"])
def run_list_gen():
    main()

if __name__ == "__main__":
    main()
