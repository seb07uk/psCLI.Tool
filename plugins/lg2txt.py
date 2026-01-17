# --- METADATA (Read by cli.py dispatcher) ---
__author__ = "Sebastian Januchowski"
__category__ = "file list"
__group__ = "system"
__desc__ = "Terminal file list generator with global settings sync."
# ---------------------------------------------

import os
import datetime
import msvcrt
import json
from cli import command

# ============================================
#  PATH CONFIGURATION (TERMINAL CLI)
# ============================================
USER_PROFILE = os.environ["USERPROFILE"]
GLOBAL_SETTINGS_FILE = os.path.join(USER_PROFILE, ".polsoft", "psCli", "settings", "terminal.json")
HOME_DIR = os.path.join(USER_PROFILE, ".polsoft", "psCLI")
LOG_DIR = os.path.join(HOME_DIR, "Log")
LOG_FILE = os.path.join(LOG_DIR, "List.log")

# System folders initialization
for d in [LOG_DIR, os.path.dirname(GLOBAL_SETTINGS_FILE)]:
    if not os.path.exists(d):
        os.makedirs(d)

# ANSI Colors
GREEN, YELLOW, RED, BLUE, CYAN, RESET = "\033[92m", "\033[93m", "\033[91m", "\033[94m", "\033[96m", "\033[0m"

# ============================================
#  GLOBAL SETTINGS SYNC
# ============================================
def load_settings():
    default = {
        "last_src": os.getcwd(),
        "last_output": os.path.join(USER_PROFILE, "Desktop", "list.txt")
    }
    if os.path.exists(GLOBAL_SETTINGS_FILE):
        try:
            with open(GLOBAL_SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "filelist_config" not in data:
                    data["filelist_config"] = default
                return data["filelist_config"]
        except:
            return default
    return default

def save_settings(filelist_data):
    try:
        full_settings = {}
        if os.path.exists(GLOBAL_SETTINGS_FILE):
            with open(GLOBAL_SETTINGS_FILE, "r", encoding="utf-8") as f:
                full_settings = json.load(f)
        full_settings["filelist_config"] = filelist_data
        with open(GLOBAL_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(full_settings, f, indent=4)
    except Exception as e:
        print(f"{RED}✖ Error updating terminal.json: {e}{RESET}")

state = load_settings()

def log_event(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================
#  HELP SYSTEM
# ============================================
def display_help():
    clear()
    log_event("Help displayed")
    print(f"{CYAN}============================================{RESET}")
    print(f"{GREEN}             FILE LIST GENERATOR - HELP{RESET}")
    print(f"{CYAN}============================================{RESET}\n")
    print(f"{YELLOW}DESCRIPTION:{RESET}")
    print(" This tool scans the selected directory and saves the list")
    print(" of items to a text file for further analysis.\n")
    print(f"{YELLOW}COMMANDS:{RESET}")
    print(f" {BLUE}[S]{RESET} - Set Source: Choose folder to scan.")
    print(f" {BLUE}[O]{RESET} - Set Output: Choose where to save the .txt file.")
    print(f" {BLUE}[1]{RESET} - Generate Full: Scans everything (files & subdirs).")
    print(f" {BLUE}[2]{RESET} - Generate Files: Scans only files in root folder.")
    print(f" {BLUE}[4]{RESET} - Ext. Filter: Find specific types (e.g., .log, .exe).")
    print(f" {BLUE}[H]{RESET} - Show this help screen.")
    print(f" {BLUE}[0]{RESET} - Exit the module.\n")
    print(f"{YELLOW}LOGS:{RESET} {LOG_FILE}")
    print(f"{YELLOW}SYNC:{RESET} Global settings are saved in terminal.json.\n")
    print(f"{CYAN}--------------------------------------------{RESET}")
    print("Press any key to return to menu...")
    msvcrt.getch()

# ============================================
#  MAIN OPERATIONS
# ============================================
def generate_list(mode, ext=""):
    try:
        src = state["last_src"]
        output_path = state["last_output"]
        if mode == "1":
            items = os.listdir(src)
            desc = "files and folders"
        elif mode == "2":
            items = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
            desc = "files only"
        elif mode == "4":
            items = [f for f in os.listdir(src) if f.lower().endswith(f".{ext.lower()}")]
            desc = f"filter *.{ext}"
        
        with open(output_path, "w", encoding="utf-8") as f:
            for item in items:
                f.write(f"{item}\n")
        
        log_event(f"Generated list ({desc}) to {output_path}")
        clear()
        print(f"{GREEN}✔ Success: {desc}{RESET}\n")
        print(f"{CYAN}--- FILE CONTENT PREVIEW ---{RESET}")
        with open(output_path, "r", encoding="utf-8") as f:
            print(f.read())
        print(f"{CYAN}----------------------------{RESET}\nPress any key to return...")
        msvcrt.getch()
    except Exception as e:
        print(f"{RED}✖ Operation error: {e}{RESET}")
        os.system("pause")

# ============================================
#  USER INTERFACE
# ============================================
def main():
    log_event("FileList module started via cli.py")
    while True:
        clear()
        print(f"{CYAN}============================================{RESET}")
        print(f"{GREEN}          LG2TXT - LIST GENERATOR{RESET}")
        print(f"{CYAN}============================================{RESET}\n")
        print(f"Source Directory: {YELLOW}{state['last_src']}{RESET}")
        print(f"Output File:      {YELLOW}{state['last_output']}{RESET}\n")
        print(f" {BLUE}[S]{RESET} Change Source   {BLUE}[O]{RESET} Change Output")
        print(f" {BLUE}[1]{RESET} Files+Folders   {BLUE}[2]{RESET} Files Only")
        print(f" {BLUE}[4]{RESET} Ext. Filter     {BLUE}[H]{RESET} Help")
        print(f" {BLUE}[0]{RESET} Exit\n")
        
        key = msvcrt.getch().decode().lower()
        
        if key == 's':
            path = input("► Enter new source path: ")
            if os.path.exists(path):
                state["last_src"] = path
                save_settings(state)
            else:
                print(f"{RED}Error: Path does not exist!{RESET}")
                msvcrt.getch()
        elif key == 'o':
            print("\n[D] Desktop | [S] Source | [C] Custom path")
            opt = msvcrt.getch().decode().lower()
            if opt == 'd': state["last_output"] = os.path.join(USER_PROFILE, "Desktop", "list.txt")
            elif opt == 's': state["last_output"] = os.path.join(state["last_src"], "list.txt")
            elif opt == 'c': state["last_output"] = input("► Full path with filename: ")
            save_settings(state)
        elif key == '1': generate_list("1")
        elif key == '2': generate_list("2")
        elif key == '4':
            ext = input("► Enter extension (e.g., py): ")
            generate_list("4", ext)
        elif key == 'h':
            display_help()
        elif key == '0':
            break

@command(name="lg2txt", aliases=["lg", "listgen"])
def run_list_gen():
    main()

if __name__ == "__main__":
    main()