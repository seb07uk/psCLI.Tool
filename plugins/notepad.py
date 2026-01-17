import os
import datetime
import sys
import msvcrt  # Library for real-time key capture on Windows (no Enter required)

# Importing Color class and command decorator from the main cli.py
try:
    from cli import Color, command
except ImportError:
    class Color:
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        GRAY = '\033[90m'
        RESET = '\033[0m'
    def command(name=None, aliases=None):
        def decorator(func):
            func.is_command = True
            func.command_name = name if name else func.__name__
            func.aliases = aliases if aliases else []
            return func
        return decorator

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "notepad"
__group__ = "office"
__desc__ = "Simple Notepad PRO with AutoSave and fast navigation"

# Note storage path
TARGET_DIR = os.path.expandvars(r"%USERPROFILE%\.polsoft\psCLI\Notepad")

def ensure_directory():
    """Creates the notes folder if it doesn't exist."""
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

def get_notes_list():
    """Retrieves list of .txt files, sorted from newest."""
    if not os.path.exists(TARGET_DIR):
        return []
    files = [f for f in os.listdir(TARGET_DIR) if f.endswith(".txt")]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(TARGET_DIR, x)), reverse=True)
    return files

@command(name="notepad", aliases=["note", "n"])
def notepad_main(*args):
    """Main interactive notepad loop."""
    ensure_directory()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.BLUE}================================{Color.RESET}")
        print(f"      Simple Notepad v1.5")
        print(f"{Color.BLUE}================================{Color.RESET}")
        print(f"[1] {Color.GREEN}New Note (Auto-Save){Color.RESET}")
        print(f"[2] {Color.BLUE}Browse Notes (W/S/O/D){Color.RESET}")
        print(f"[H] {Color.YELLOW}Help / Manual{Color.RESET}")
        print(f"[A] {Color.YELLOW}About Author{Color.RESET}")
        print(f"[X] {Color.RED}Exit{Color.RESET}")
        print(f"{Color.BLUE}================================{Color.RESET}")
        
        # Capture key in the main menu
        choice = msvcrt.getch().decode('utf-8').lower()

        if choice == '1':
            create_new_note()
        elif choice == '2':
            browse_notes_menu()
        elif choice == 'h':
            display_help_manual()
        elif choice == 'a':
            display_about_info()
        elif choice in ['x', 'q']:
            break

def create_new_note():
    os.system('cls')
    print(f"{Color.GREEN}Type your note content.{Color.RESET}")
    print(f"{Color.YELLOW}(Press CTRL+Z then ENTER to save and finish){Color.RESET}")
    print("-" * 32)
    
    try:
        content = sys.stdin.read()
        if not content.strip():
            print(f"\n{Color.RED}[!] Cancelled or note is empty.{Color.RESET}")
            os.system("timeout /t 2 >nul")
            return

        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Note_{ts}.txt"
        filepath = os.path.join(TARGET_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"\n{Color.GREEN}[OK] Saved automatically as: {filename}{Color.RESET}")
        os.system("timeout /t 2 >nul")
    except EOFError:
        pass

def browse_notes_menu():
    selected_idx = 0
    while True:
        notes = get_notes_list()
        if not notes:
            os.system('cls')
            print(f"{Color.RED}[!] No notes found.{Color.RESET}")
            os.system("pause")
            return

        os.system('cls')
        print(f"{Color.BLUE}--- NOTE LIST (W/S - Navigate, O - Open, D - Delete, Q - Back) ---{Color.RESET}\n")
        
        for i, filename in enumerate(notes):
            if i == selected_idx:
                print(f" {Color.GREEN}> {filename} {Color.RESET}")
            else:
                print(f"   {filename}")
        
        print(f"\n{Color.GRAY}Notes: {len(notes)} | W=Up, S=Down, O=Open, D=Del, Q=Back{Color.RESET}")
        
        key = msvcrt.getch().decode('utf-8').lower()

        if key == 'q': 
            break
        elif key == 'w' and selected_idx > 0: 
            selected_idx -= 1
        elif key == 's' and selected_idx < len(notes) - 1: 
            selected_idx += 1
        elif key == 'o' or key == '\r': # \r is Enter key
            open_note_view(notes[selected_idx])
        elif key == 'd': 
            delete_note_file(notes[selected_idx])

def open_note_view(filename):
    os.system('cls')
    filepath = os.path.join(TARGET_DIR, filename)
    print(f"{Color.YELLOW}File: {filename}{Color.RESET}")
    print(f"{Color.BLUE}{'-'*40}{Color.RESET}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"{Color.RED}Read Error: {e}{Color.RESET}")
    print(f"{Color.BLUE}{'-'*40}{Color.RESET}")
    print("Press any key to return to the list...")
    msvcrt.getch()

def delete_note_file(filename):
    print(f"\n{Color.RED}[?] Are you sure you want to delete: {filename}? (Y/N){Color.RESET}")
    confirm = msvcrt.getch().decode('utf-8').lower()
    if confirm == 'y':
        try:
            os.remove(os.path.join(TARGET_DIR, filename))
            print(f"{Color.GREEN}[OK] File deleted.{Color.RESET}")
            os.system("timeout /t 1 >nul")
        except Exception as e:
            print(f"{Color.RED}[!] Error: {e}{Color.RESET}")
            os.system("pause")

def display_help_manual():
    os.system('cls')
    print(f"{Color.BLUE}==================================={Color.RESET}")
    print(f"            NOTEPAD CLI HELP")
    print(f"{Color.BLUE}==================================={Color.RESET}\n")
    print(f"{Color.GREEN}1. Creating Notes:{Color.RESET} Select [1], type text. Finish with {Color.YELLOW}CTRL+Z + Enter{Color.RESET}")
    print(f"{Color.GREEN}2. Browsing:{Color.RESET} Use {Color.YELLOW}W/S{Color.RESET} to move, {Color.YELLOW}O{Color.RESET} to open file.")
    print(f"{Color.GREEN}3. Storage Path:{Color.RESET} {TARGET_DIR}\n")
    print("Press any key to return...")
    msvcrt.getch()

def display_about_info():
    os.system('cls')
    print(f"{Color.BLUE}==================================={Color.RESET}")
    print(f"            ABOUT AUTHOR")
    print(f"{Color.BLUE}==================================={Color.RESET}\n")
    print(f"{Color.GREEN}Author:{Color.RESET} Sebastian Januchowski")
    print(f"{Color.GREEN}Email:{Color.RESET}  polsoft.its@fastservice.com")
    print(f"{Color.GREEN}GitHub:{Color.RESET} https://github.com/seb07uk\n")
    print(f"{Color.BLUE}==================================={Color.RESET}")
    print("\nPress any key to return to menu...")
    msvcrt.getch()

if __name__ == "__main__":
    notepad_main()