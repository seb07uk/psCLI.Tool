import os
import json
import ctypes
import sys
from datetime import datetime
from cli import command

# --- METADATA & SETTINGS ---
__metadata__ = {
    "module_id": "core",
    "name": "SuperUser DO",
    "version": "1.4.0",
    "permissions": ["execute", "write_logs", "view_help"],
    "home_dir": r"C:\Users\%userprofile%\.polsoft\psCLI\\",
    "cli_name": "TERMINAL CLI"
}

__author__ = "Sebastian Januchowski"
__category__ = "system"
__group__ = "core"
__desc__ = "Execute programs with administrator privileges"

SETTINGS_FILE = os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings\terminal.json")

def show_help():
    """Wyświetla dokumentację modułu sudo."""
    help_text = f"""
{__metadata__['cli_name']} - MODUŁ SUDO (v{__metadata__['version']})
--------------------------------------------------
OPIS:
    Moduł służy do eskalacji uprawnień dla aplikacji i skryptów.
    Wszystkie operacje są logowane do terminal.json.

SKŁADNIA:
    sudo <command> [args]
    sudo help

PRZYKŁADY:
    sudo calc          # Uruchamia kalkulator jako administrator
    sudo notepad.exe   # Uruchamia notatnik z uprawnieniami admina
    sudo help          # Wyświetla tę pomoc

UPRAWNIENIA:
    - {', '.join(__metadata__['permissions'])}

LOGI:
    {SETTINGS_FILE}
--------------------------------------------------
    """
    print(help_text)

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except: return False

def log_action(action_type, target):
    log_path = os.path.expandvars(SETTINGS_FILE)
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "target": target,
        "status": "elevated_execution"
    }
    try:
        data = {}
        if os.path.exists(log_path):
            with open(log_path, "r") as f: data = json.load(f)
        if "execution_logs" not in data: data["execution_logs"] = []
        data["execution_logs"].append(entry)
        with open(log_path, "w") as f: json.dump(data, f, indent=4)
    except: pass

def execute(command, args=None):
    if args is None: args = []
    
    # Obsługa komendy help
    if command.lower() == "help":
        show_help()
        return

    # Logika execute
    target = "calc.exe" if command.lower() == "calc" else command
    
    if is_admin():
        os.system(f"start {target} {' '.join(args)}")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", target, " ".join(args), None, 1)
        log_action("execute_elevated", target)

@command(name="sudo", aliases=["admin", "elevate"])
def sudo(*args):
    """Execute command with administrator privileges"""
    if not args:
        print("Usage: sudo <command> [args]")
        return
    execute(args[0], list(args[1:]))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute(sys.argv[1], sys.argv[2:])
    else:
        print(f"TERMINAL CLI: Wpisz 'sudo help', aby uzyskać listę komend.")
