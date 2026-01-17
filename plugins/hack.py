import os
import sys
import re
import subprocess
import time
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "hacking"
__group__ = "menu"
__desc__ = "Hacking Tools - Avoid the limits"

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
METADATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "metadata"))

HEADER = r"""
 888    888           .d8888b.  888      8888888           .d8888b. 
 888    888          d88P  Y88b 888        888            d88P  Y88b
 888    888          888    888 888        888            888    888
 8888888888  8888b.  888        888  888   888   88888b.  888       
 888    888     "88b 888        888 .88P   888   888 "88b 888  88888
 888    888 .d888888 888    888 888888K    888   888  888 888    888
 888    888 888  888 Y88b  d88P 888 "88b   888   888  888 Y88b  d88P
 888    888 "Y888888  "Y8888P"  888  888 8888888 888  888  "Y8888P88
"""

def get_metadata(filename):
    """Pobiera metadane z katalogu /metadata/ lub z zawartości pliku."""
    meta = {"desc": "Brak opisu", "author": "Unknown", "category": "tool", "group": "tools"}
    
    # Próbuj załadować z JSON'a w metadata
    json_path = os.path.join(METADATA_DIR, f"{filename}.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    meta.update(data)
                    return meta
        except:
            pass
    
    # Fallback: czytaj z zawartości pliku
    file_path = os.path.join(TOOLS_DIR, filename)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            desc_match = re.search(r'__desc__\s*=\s*["\'](.*?)["\']', content)
            if desc_match: 
                meta["desc"] = desc_match.group(1)
    except: 
        pass
    
    return meta

@command(name="hack", aliases=["tools", "hacking"])
def hack_dispatcher(*args):
    """Hacking Tools - Avoid the limits."""
    
    SUPPORTED_EXTENSIONS = (".py", ".bat", ".cmd", ".ps1", ".exe", ".vbs")
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.GREEN}{HEADER}{Color.RESET}")
        
        # Tworzenie katalogu tools, jeśli nie istnieje
        if not os.path.exists(TOOLS_DIR):
            os.makedirs(TOOLS_DIR)

        # Pobieranie listy obsługiwanych plików z /tools/
        files = [f for f in os.listdir(TOOLS_DIR) if f.endswith(SUPPORTED_EXTENSIONS) and f != "__init__.py"]
        
        if not files:
            print(f"{Color.RED}[!] Folder /tools/ jest pusty.{Color.RESET}")
            print(f"{Color.GRAY}Dodaj skrypty narzędzi do: {TOOLS_DIR}{Color.RESET}")
            input("\nNaciśnij Enter, aby wrócić...")
            break

        w = {"id": 4, "name": 12, "desc": 45, "group": 12, "aliases": 15}
        header = f"{'ID':<{w['id']}} | {'TOOL NAME':<{w['name']}} | {'DESCRIPTION':<{w['desc']}} | {'GROUP':<{w['group']}} | {'ALIASES':<{w['aliases']}}"
        sep_width = sum(w.values()) + 15
        
        print(f"{Color.BOLD}{header}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * sep_width}{Color.RESET}")

        tools_map = {}
        for idx, filename in enumerate(sorted(files), 1):
            name = filename.rsplit('.', 1)[0]
            path = os.path.join(TOOLS_DIR, filename)
            meta = get_metadata(filename)
            
            tools_map[str(idx)] = (name, path)
            tools_map[name.lower()] = (name, path)
            
            group = meta.get('group', 'tools')
            aliases = ", ".join(meta.get('aliases', []))
            desc = (meta['desc'] or "")[:w['desc']]
            aliases_str = aliases[:w['aliases']] if aliases else "-"
            print(f"{Color.GREEN}{idx:<{w['id']}}{Color.RESET} | {Color.WHITE}{name:<{w['name']}}{Color.RESET} | {desc:<{w['desc']}} | {Color.CYAN}{group:<{w['group']}}{Color.RESET} | {Color.YELLOW}{aliases_str:<{w['aliases']}}{Color.RESET}")

        try:
            choice = input(f"\n{Color.CYAN}psCLI/hack > {Color.RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if not choice: continue
        if choice in ['menu', 'exit', 'q', 'quit']: break

        if choice in tools_map:
            tool_name, path = tools_map[choice]
            ext = os.path.splitext(path)[1].lower()
            
            print(f"{Color.YELLOW}[*] Uruchamianie {tool_name}...{Color.RESET}")
            
            try:
                if ext == ".py":
                    subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                elif ext == ".ps1":
                    subprocess.Popen(["powershell", "-NoExit", "-File", path], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                elif ext in [".bat", ".cmd"]:
                    subprocess.Popen([path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                elif ext == ".vbs":
                    subprocess.Popen(["cscript.exe", path], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                elif ext == ".exe":
                    subprocess.Popen([path], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Nie można uruchomić: {e}{Color.RESET}")
                time.sleep(2)
        else:
            print(f"{Color.RED}[!] Nieprawidłowy wybór.{Color.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    hack_dispatcher()