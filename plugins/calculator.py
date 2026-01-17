import os
import math
import sys
from datetime import datetime
# Importujemy dekorator i kolory bezpośrednio z Twojego pliku cli.py
from cli import command, Color

# --- PLUGIN METADATA (Read by Dispatcher._load_python_module) ---
__author__ = "Sebastian Januchowski"
__category__ = "math"
__group__ = "office"
__desc__ = "Professional scientific calculator with history logging."

# Path Configuration (Aligned with Polsoft standards)
HIST_DIR = os.path.expandvars(r"%userprofile%\.polsoft\psCli\Calculator")
HIST_FILE = os.path.join(HIST_DIR, "history.txt")

def save_history(operation, result):
    """Saves calculation logs to the specified history directory."""
    if not os.path.exists(HIST_DIR):
        try:
            os.makedirs(HIST_DIR)
        except Exception:
            return # Fail silently if path is inaccessible
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {operation} = {result}\n")
    except Exception as e:
        print(f"{Color.RED}[ERROR] Could not save history: {e}{Color.RESET}")

def get_num(prompt_text):
    """Helper to handle input and comma/dot conversion."""
    try:
        val = input(f"{Color.WHITE}{prompt_text}{Color.RESET}").replace(",", ".")
        return float(val)
    except ValueError:
        print(f"{Color.RED}Invalid numeric input.{Color.RESET}")
        return None

def show_history_log():
    """Displays the last 15 entries from the history file."""
    print(f"\n{Color.CYAN}=== CALCULATION HISTORY ==={Color.RESET}")
    print(f"{Color.GRAY}Location: {HIST_FILE}{Color.RESET}\n")
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-15:]:
                print(f" {Color.YELLOW}»{Color.RESET} {line.strip()}")
    else:
        print(f"{Color.GRAY}No records found.{Color.RESET}")
    input(f"\n{Color.GRAY}Press Enter to return...{Color.RESET}")

@command(name="calculator", aliases=["math", "calc", "kalk"])
def run_calculator(*args):
    """Interactive professional calculator module."""
    # args can be used later for direct CLI calculations (e.g., 'calc 2 + 2')
    
    while True:
        # Clear screen (Windows/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Header
        print(f" {Color.GRAY}{datetime.now().year}(c) {__author__}{Color.RESET}")
        print(f"{Color.GREEN}==============================={Color.RESET}")
        print(f"     {Color.CYAN}{Color.BOLD}Calculator Pro v1.8{Color.RESET}")
        print(f"{Color.GREEN}==============================={Color.RESET}\n")
        
        # Menu
        print(f"[1] {Color.YELLOW}Addition{Color.RESET}       [6] {Color.YELLOW}Square Root{Color.RESET}")
        print(f"[2] {Color.YELLOW}Subtraction{Color.RESET}    [7] {Color.YELLOW}Sine{Color.RESET}")
        print(f"[3] {Color.YELLOW}Multiplication{Color.RESET} [8] {Color.YELLOW}Cosine{Color.RESET}")
        print(f"[4] {Color.YELLOW}Division{Color.RESET}       [9] {Color.YELLOW}Tangent{Color.RESET}")
        print(f"[5] {Color.YELLOW}Power{Color.RESET}")
        print(f"\n[h] {Color.CYAN}History{Color.RESET}    [?] {Color.CYAN}Help{Color.RESET}    [e] {Color.RED}Exit to CLI{Color.RESET}\n")

        choice = input(f"{Color.BOLD}Selection » {Color.RESET}").lower()

        if choice in ["e", "exit", "quit"]:
            break
        elif choice == "h":
            show_history_log()
            continue
        elif choice == "?":
            print(f"\n{Color.CYAN}Info:{Color.RESET} Standard double-precision math module.")
            print(f"Trig functions expect degrees as input.")
            input("\nPress Enter...")
            continue
            
        # Mathematical Logic
        if choice in "12345":
            a = get_num("Enter first number: ")
            b = get_num("Enter second number: ")
            if a is not None and b is not None:
                if choice == '1': res, op = a + b, f"{a} + {b}"
                elif choice == '2': res, op = a - b, f"{a} - {b}"
                elif choice == '3': res, op = a * b, f"{a} * {b}"
                elif choice == '4':
                    if b == 0:
                        print(f"{Color.RED}Error: Division by zero.{Color.RESET}")
                        input()
                        continue
                    res, op = a / b, f"{a} / {b}"
                elif choice == '5': res, op = math.pow(a, b), f"{a} ^ {b}"
                
                print(f"\n{Color.GREEN}{Color.BOLD}Result: {res}{Color.RESET}")
                save_history(op, res)
                input("\nPress Enter...")

        elif choice == '6':
            a = get_num("Enter number: ")
            if a is not None:
                if a < 0:
                    print(f"{Color.RED}Error: Cannot root negative number.{Color.RESET}")
                else:
                    res = math.sqrt(a)
                    print(f"\n{Color.GREEN}{Color.BOLD}Result: {res}{Color.RESET}")
                    save_history(f"sqrt({a})", res)
                input("\nPress Enter...")

        elif choice in "789":
            deg = get_num("Enter angle (degrees): ")
            if deg is not None:
                rad = math.radians(deg)
                if choice == '7': res, fn = math.sin(rad), "sin"
                elif choice == '8': res, fn = math.cos(rad), "cos"
                elif choice == '9': res, fn = math.tan(rad), "tan"
                
                print(f"\n{Color.GREEN}{Color.BOLD}{fn}({deg}) = {res}{Color.RESET}")
                save_history(f"{fn}({deg})", res)
                input("\nPress Enter...")