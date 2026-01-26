import sys
import time
import os
import hashlib
import importlib
import json
import getpass
from pathlib import Path
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "security"
__group__ = "system"
__desc__ = "Password management and running protected modules"
# Kolory ANSI
RESET    = "\033[0m"
RED_BG   = "\033[41m"
GREEN_BG = "\033[42m"
BLACK    = "\033[30m"
CYAN     = "\033[36m"
YELLOW   = "\033[33m"
MAGENTA  = "\033[35m"
BOLD     = "\033[1m"

# Hasło domyślne
DOMYSLNE_HASLO = "polsoft"
HASLO = None

MAX_PROBY = 3
is_admin = False

# Ścieżka do pliku hasła
SCIEZKA = Path(os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings"))
PLIK_HASLA = SCIEZKA / "haslo.txt"
PROTECTED_FILE = SCIEZKA / "protected.json"


# ==========================================
#  SZYFROWANIE I ZAPIS / ODCZYT HASŁA
# ==========================================

def szyfruj_haslo(haslo):
    return hashlib.sha256(haslo.encode("utf-8")).hexdigest()


def wczytaj_haslo():
    global HASLO
    SCIEZKA.mkdir(parents=True, exist_ok=True)

    if PLIK_HASLA.exists():
        with open(PLIK_HASLA, "r", encoding="utf-8") as f:
            HASLO = f.read().strip()
    else:
        HASLO = szyfruj_haslo(DOMYSLNE_HASLO)
        zapisz_haslo()


def zapisz_haslo():
    with open(PLIK_HASLA, "w", encoding="utf-8") as f:
        f.write(HASLO)

def _load_protected():
    try:
        if PROTECTED_FILE.exists():
            with open(PROTECTED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                lst = data.get("commands", [])
                if isinstance(lst, list):
                    return set([str(x).lower() for x in lst])
    except:
        pass
    return set()

def _save_protected(names):
    try:
        SCIEZKA.mkdir(parents=True, exist_ok=True)
        base = {}
        if PROTECTED_FILE.exists():
            try:
                with open(PROTECTED_FILE, "r", encoding="utf-8") as rf:
                    base = json.load(rf)
            except:
                base = {}
        base["commands"] = sorted(list(names))
        with open(PROTECTED_FILE, "w", encoding="utf-8") as f:
            json.dump(base, f, ensure_ascii=False, indent=2)
    except:
        pass

def _load_protected_modules():
    try:
        if PROTECTED_FILE.exists():
            with open(PROTECTED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                lst = data.get("modules", [])
                if isinstance(lst, list):
                    return set([str(x).lower() for x in lst])
    except:
        pass
    return set()

def _save_protected_modules(names):
    try:
        SCIEZKA.mkdir(parents=True, exist_ok=True)
        base = {}
        if PROTECTED_FILE.exists():
            try:
                with open(PROTECTED_FILE, "r", encoding="utf-8") as rf:
                    base = json.load(rf)
            except:
                base = {}
        base["modules"] = sorted(list(names))
        with open(PROTECTED_FILE, "w", encoding="utf-8") as f:
            json.dump(base, f, ensure_ascii=False, indent=2)
    except:
        pass

def verify_once():
    wczytaj_haslo()
    try:
        proba = getpass.getpass("Hasło: ")
    except:
        proba = input("Podaj hasło: ")
    return szyfruj_haslo(proba) == HASLO


# ==========================================
#  FUNKCJE WSPÓLNE
# ==========================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ekran_kolorowy(kolor, tekst):
    clear_screen()
    wysokosc = 30
    szerokosc = 120

    print(kolor, end="")
    for _ in range(wysokosc):
        print(" " * szerokosc)
    print(RESET, end="")

    print(f"{kolor}{BLACK}{BOLD}{tekst.center(szerokosc)}{RESET}")

    time.sleep(1)
    clear_screen()


# ==========================================
#  AUTOMATYCZNE WYKRYWANIE MODUŁÓW
# ==========================================

def znajdz_moduly():
    katalog = Path("modules")
    lista = []

    if not katalog.exists():
        return lista

    for plik in katalog.rglob("*.py"):
        if plik.name == "__init__.py":
            continue

        rel = plik.relative_to(katalog)
        modul = ".".join(rel.with_suffix("").parts)
        lista.append(modul)

    return lista


# ==========================================
#  URUCHAMIANIE MODUŁU
# ==========================================

def uruchom_modul(modul):
    global HASLO

    print(f"{CYAN}{BOLD}=== RUN MODULE: {modul} ==={RESET}")

    potrzeba = modul.lower() in _load_protected_modules()
    if potrzeba:
        proba = input("Enter password: ")
        if szyfruj_haslo(proba) != HASLO:
            ekran_kolorowy(RED_BG, "WRONG PASSWORD — MODULE BLOCKED")
            return

    try:
        pakiet = importlib.import_module(f"modules.{modul}")
        ekran_kolorowy(GREEN_BG, f"MODULE {modul.upper()} STARTED")
        pakiet.run()
    except Exception as e:
        ekran_kolorowy(RED_BG, f"MODULE ERROR: {e}")


# ==========================================
#  LOGOWANIE
# ==========================================

def logowanie():
    global is_admin, HASLO

    print(f"{BOLD}{CYAN}=== Protected access: polsoft.ITS™ London ==={RESET}")
    proby = 0

    while proby < MAX_PROBY:
        try:
            proba = input(f"{YELLOW}Enter password: {RESET}")
        except KeyboardInterrupt:
            print(f"\n{RED_BG}{BLACK}Interrupted by user. Closing...{RESET}")
            sys.exit(1)

        if szyfruj_haslo(proba) == HASLO:
            is_admin = True
            ekran_kolorowy(GREEN_BG, "ACCESS GRANTED — ADMIN PRIVILEGES")
            return True
        else:
            proby += 1
            if proby < MAX_PROBY:
                ekran_kolorowy(RED_BG, f"WRONG PASSWORD — {MAX_PROBY - proby} TRIES LEFT")
            else:
                ekran_kolorowy(RED_BG, "ACCESS DENIED — LIMIT REACHED")
                return False


# ==========================================
#  OPCJE ADMINISTRATORA
# ==========================================

def zmiana_hasla():
    global HASLO

    print(f"{CYAN}{BOLD}=== CHANGE PASSWORD ==={RESET}")

    proby = 0
    MAX_PROBY_ZMIANY = 3

    while proby < MAX_PROBY_ZMIANY:
        stare = input("Enter current password: ")

        if szyfruj_haslo(stare) == HASLO:
            nowe = input("Enter new password: ")
            potwierdz = input("Confirm new password: ")

            if nowe != potwierdz:
                ekran_kolorowy(RED_BG, "PASSWORDS DO NOT MATCH")
                return

            HASLO = szyfruj_haslo(nowe)
            zapisz_haslo()
            ekran_kolorowy(GREEN_BG, "PASSWORD CHANGED")
            return

        else:
            proby += 1
            pozostalo = MAX_PROBY_ZMIANY - proby

            if pozostalo > 0:
                ekran_kolorowy(RED_BG, f"WRONG CURRENT PASSWORD — {pozostalo} TRIES LEFT")
            else:
                ekran_kolorowy(RED_BG, "WRONG PASSWORD — CHANGE BLOCKED")
                return


def reset_hasla():
    global HASLO
    HASLO = szyfruj_haslo(DOMYSLNE_HASLO)
    zapisz_haslo()
    ekran_kolorowy(GREEN_BG, "PASSWORD RESET TO DEFAULT")


def pomoc():
    clear_screen()
    print(f"{BOLD}{CYAN}=== HELP ==={RESET}")
    print("""
Available options:
1 – Change password
2 – Reset password
3 – Help
4 – Run module
5 – Exit
6 – Protect commands (protect <name...>)
7 – Unprotect commands (unprotect <name...>)
8 – List protected (list)
9 – Clear protected (clear)

Modules are located under 'modules/' directory and subfolders.
Each module must have a run() function.
""")
    input(f"{YELLOW}Press ENTER to return...{RESET}")
    clear_screen()


# ==========================================
#  MENU GŁÓWNE
# ==========================================

def menu():
    clear_screen()
    print(f"{BOLD}{MAGENTA}=== MAIN MENU ==={RESET}")

    if is_admin:
        print(f"{GREEN_BG}{BLACK}{BOLD}  ADMIN MODE ACTIVE  {RESET}\n")

    while True:
        print(f"{CYAN}1{RESET}. Change")
        print(f"{CYAN}2{RESET}. Reset")
        print(f"{CYAN}3{RESET}. Help")
        print(f"{CYAN}4{RESET}. Run module")
        print(f"{CYAN}5{RESET}. Exit")

        wybor = input(f"{YELLOW}Choose option: {RESET}")

        if wybor == "1":
            zmiana_hasla()
        elif wybor == "2":
            reset_hasla()
        elif wybor == "3":
            pomoc()
        elif wybor == "4":
            lista = znajdz_moduly()

            if not lista:
                try:
                    from cli import Dispatcher
                    disp = Dispatcher()
                    disp.load_plugins()
                    komendy = sorted([n for n, f in disp.commands.items() if str(f.meta.get("group","")).lower() != "menu"])
                    if not komendy:
                        ekran_kolorowy(RED_BG, "BRAK MODUŁÓW / KOMEND")
                        continue
                    print(f"{CYAN}=== AVAILABLE CLI COMMANDS ==={RESET}")
                    for i, n in enumerate(komendy, 1):
                        print(f"{i}. {n}")
                    try:
                        nr = int(input("Choose command: "))
                        if nr < 1 or nr > len(komendy):
                            ekran_kolorowy(RED_BG, "INVALID CHOICE")
                            continue
                    except:
                        ekran_kolorowy(RED_BG, "INVALID FORMAT")
                        continue
                    wybrana = komendy[nr-1]
                    pc = _load_protected()
                    print(f"{CYAN}Action: [R] run | [A] protect | [U] unprotect{RESET}")
                    akcja = input("Choose action (R/A/U): ").strip().lower()
                    if akcja in ["a", "add"]:
                        pc.add(wybrana.lower())
                        _save_protected(pc)
                        ekran_kolorowy(GREEN_BG, "COMMAND PROTECTED")
                    elif akcja in ["u", "unprotect", "remove"]:
                        pc.discard(wybrana.lower())
                        _save_protected(pc)
                        ekran_kolorowy(GREEN_BG, "COMMAND UNPROTECTED")
                    else:
                        # wywołanie komendy przez Dispatcher (bramka w cli.py zadziała)
                        try:
                            disp.execute(wybrana)
                        except Exception as e:
                            ekran_kolorowy(RED_BG, f"COMMAND ERROR: {e}")
                    continue
                except Exception as e:
                    ekran_kolorowy(RED_BG, f"CLI COMMAND LOAD ERROR: {e}")
                    continue

            print(f"{CYAN}=== AVAILABLE MODULES ==={RESET}")
            for i, m in enumerate(lista, 1):
                print(f"{i}. {m}")

            try:
                nr = int(input("Choose module: "))
                if nr < 1 or nr > len(lista):
                    ekran_kolorowy(RED_BG, "INVALID CHOICE")
                    continue
            except:
                ekran_kolorowy(RED_BG, "INVALID FORMAT")
                continue

            wybrany = lista[nr - 1]
            pm = _load_protected_modules()
            print(f"{CYAN}Action: [R] run | [A] protect | [U] unprotect{RESET}")
            akcja = input("Choose action (R/A/U): ").strip().lower()
            if akcja in ["a", "add"]:
                pm.add(wybrany.lower())
                _save_protected_modules(pm)
                ekran_kolorowy(GREEN_BG, "MODULE PROTECTED")
            elif akcja in ["u", "unprotect", "remove"]:
                pm.discard(wybrany.lower())
                _save_protected_modules(pm)
                ekran_kolorowy(GREEN_BG, "MODULE UNPROTECTED")
            else:
                uruchom_modul(wybrany)
        elif wybor == "5":
            print("Closing...")
            break
        else:
            ekran_kolorowy(RED_BG, "INVALID CHOICE")

# ==========================================
#  TRYB C — MENU LUB MODUŁ
# ==========================================

if __name__ == "__main__":
    wczytaj_haslo()

    # Tryb modułu
    if len(sys.argv) > 1:
        modul = sys.argv[1]
        uruchom_modul(modul)
        sys.exit(0)

    # Tryb menu
    if logowanie():
        menu()
    else:
        sys.exit(1)

@command(name="passwd", aliases=["password", "pass"])
def run(*args):
    wczytaj_haslo()
    if args:
        a = args[0].lower()
        if a in ["help", "h", "?"]:
            pomoc()
            return
        if a in ["reset", "default"]:
            reset_hasla()
            return
        if a in ["change", "set"]:
            zmiana_hasla()
            return
        if a in ["mod", "module"] and len(args) > 1:
            uruchom_modul(args[1])
            return
        if a in ["protect", "link"] and len(args) > 1:
            current = _load_protected()
            to_add = [x.lower() for x in args[1:]]
            current.update(to_add)
            _save_protected(current)
            ekran_kolorowy(GREEN_BG, "PODŁĄCZONO MODUŁY DO OCHRONY")
            return
        if a in ["unprotect", "unlink"] and len(args) > 1:
            current = _load_protected()
            for x in args[1:]:
                current.discard(x.lower())
            _save_protected(current)
            ekran_kolorowy(GREEN_BG, "ODŁĄCZONO MODUŁY Z OCHRONY")
            return
        if a in ["list"]:
            lst = sorted(list(_load_protected()))
            print(f"{CYAN}Podłączone komendy:{RESET}")
            if not lst:
                print(f"{YELLOW}(brak){RESET}")
            else:
                for n in lst:
                    print(f"- {n}")
            return
        if a in ["clear"]:
            _save_protected(set())
            ekran_kolorowy(GREEN_BG, "WYCZYSZCZONO LISTĘ OCHRONY")
            return
    if logowanie():
        menu()
