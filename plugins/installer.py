import os
import sys
import re
import subprocess
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "tools"
__group__ = "menu"
__desc__ = "Installers Manager - dynamic launcher for installer tools"

HEADER = r"""
     ooooo                          .             oooo  oooo                    
     `888'                        .o8             `888  `888                    
      888  ooo. .oo.    .oooo.o .o888oo  .oooo.    888   888   .ooooo.  oooo d8b
      888  `888P"Y88b  d88(  "8   888   `P  )88b   888   888  d88' `88b `888""8P
      888   888   888  `"Y88b.    888    .oP"888   888   888  888ooo888  888    
      888   888   888  o.  )88b   888 . d8(  888   888   888  888    .o  888    
     o888o o888o o888o 8""888P'   "888" `Y888""8o o888o o888o `Y8bod8P' d888b   
"""

INSTALLERS_DIR = os.path.abspath(os.path.dirname(__file__))

def get_metadata(file_path):
    """Reads installer metadata from JSON file and Python source file."""
    meta = {"desc": "No description", "aliases": [], "group": "", "author": "", "category": ""}
    
    # Try to read metadata from JSON file
    try:
        metadata_path = file_path + ".json"
        if os.path.exists(metadata_path):
            import json
            with open(metadata_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                meta["desc"] = data.get("desc", meta["desc"])
                meta["aliases"] = data.get("aliases", meta["aliases"])
    except: pass
    
    # Try to read metadata from Python source file
    if file_path.endswith('.py'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract __group__
                match = re.search(r'__group__\s*=\s*["\']([^"\']*)["\']', content)
                if match:
                    meta["group"] = match.group(1)
                
                # Extract __desc__
                match = re.search(r'__desc__\s*=\s*["\']([^"\']*)["\']', content)
                if match:
                    meta["desc"] = match.group(1)
                
                # Extract __author__
                match = re.search(r'__author__\s*=\s*["\']([^"\']*)["\']', content)
                if match:
                    meta["author"] = match.group(1)
                
                # Extract __category__
                match = re.search(r'__category__\s*=\s*["\']([^"\']*)["\']', content)
                if match:
                    meta["category"] = match.group(1)
                
                # Extract __aliases__
                match = re.search(r'__aliases__\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if match:
                    aliases_str = match.group(1)
                    meta["aliases"] = [a.strip().strip('\'"') for a in aliases_str.split(',') if a.strip()]
        except: pass
    
    return meta

def show_help():
    """Displays help information for the Installers Manager."""
    print(f"\n{Color.BOLD}INSTALLERS MANAGER HELP{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 40}{Color.RESET}")
    print(f"{Color.GREEN}ID / Name{Color.RESET}   - Type the installer ID or name to launch it.")
    print(f"{Color.GREEN}menu{Color.RESET}        - Return to the main TERMINAL CLI menu.")
    print(f"{Color.GREEN}help / h{Color.RESET}    - Show this help message.")
    print(f"{Color.GREEN}exit / q{Color.RESET}    - Close the launcher.")
    print(f"{Color.GRAY}{'=' * 40}{Color.RESET}")
    input("\nPress Enter to continue...")

@command(name="installer", aliases=["inst", "i"])
def installer_dispatcher(*args):
    """Installer launcher for TERMINAL CLI."""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.CYAN}{HEADER}{Color.RESET}")
        
        all_files = [f for f in os.listdir(INSTALLERS_DIR) if f.endswith((".exe", ".bat", ".cmd", ".ps1", ".py", ".vbs")) and not f.startswith("__")] if os.path.exists(INSTALLERS_DIR) else []
        
        # Filter files by __group__ = "installer"
        files = []
        for filename in all_files:
            file_path = os.path.join(INSTALLERS_DIR, filename)
            meta = get_metadata(file_path)
            if meta.get("group") == "installer":
                files.append(filename)
        
        if not files:
            print(f"{Color.YELLOW}[!] No installers found in /plugins folder.{Color.RESET}")
            input("Press Enter...")
            return

        print(f"{Color.BOLD}{'ID':<2} | {'INSTALLER':<17} | {'DESCRIPTION':<45}   | {'ALIASES':<19}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 86}{Color.RESET}")

        installers_map = {}
        for idx, filename in enumerate(sorted(files), 1):
            name = os.path.splitext(filename)[0]
            meta = get_metadata(os.path.join(INSTALLERS_DIR, filename))
            installers_map[str(idx)] = (name, os.path.join(INSTALLERS_DIR, filename))
            installers_map[name.lower()] = (name, os.path.join(INSTALLERS_DIR, filename))
            aliases_str = ', '.join(meta['aliases']) if meta['aliases'] else ""
            print(f"{Color.GREEN}{idx:<2}{Color.RESET} | {Color.WHITE}{name:<17}{Color.RESET} | {meta['desc']:<45} | {aliases_str:<19}")

        while True:
            try:
                choice = input(f"\n{Color.CYAN}psINSTALLER > {Color.RESET}").strip().lower()
            except: return

            if choice in ['help', 'h', '?']:
                show_help()
                break # Refresh the main view after help

            if choice == 'menu':
                os.system('cls' if os.name == 'nt' else 'clear')
                return 

            if choice in ['q', 'exit', 'quit']:
                return

            if choice in installers_map:
                installer_name, path = installers_map[choice]
                print(f"{Color.YELLOW}[*] Running: {installer_name}...{Color.RESET}")
                ext = os.path.splitext(path)[1].lower()
                if ext == ".py":
                    subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                elif ext == ".ps1":
                    subprocess.Popen(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    subprocess.Popen(path, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                print(f"{Color.RED}[!] Unknown command: {choice}. Type 'help' for options.{Color.RESET}")

if __name__ == "__main__":
    installer_dispatcher()
