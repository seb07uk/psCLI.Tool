import os
import sys
import subprocess
import re
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "ascii art"
__group__ = "menu"
__desc__ = "ASCII Center - launcher for ASCII animations and scripts"

ASCII_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ascii"))
METADATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "metadata"))

HEADER = r"""
                     (#######) 
      _____         (#########) 
     /     \       (#########)    |\/\/\/|     /\ /\  /\               /\ 
     \/     |      (#########)    |      |     | V  \/  \---.    .----/  \----. 
     | (o)(o)       (o)(o)(##)    |      |      \_        /       \          / 
     |   .---_)    ,_C     (##)    | (o)(o)       (o)(o)  <__.   .--\ (o)(o) /__. 
     | |.___|    /____,   (##)    C      _)     _C         /     \     ()     / 
     |  \__/       \     (#)       | ,___|     /____,   )  \      >   (C_)   < 
     /_____\        |    |         |   /         \     /----'    /___\____/___\ 
     _____/ \       OOOOOO        /____\          ooooo             /|    |\ 
             \     /      \      /      \        /     \           /        \ 
     
      Homer         Marge          Bart           Lisa              Maggie
"""

def get_json_metadata(filename):
    base = f"{filename}.json"
    path = os.path.join(METADATA_DIR, base)
    meta = {"author": "Unknown", "category": "ascii", "group": "fun", "desc": "No description", "aliases": []}
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
                m = re.search(r'"desc"\s*:\s*"([^"]+)"', data)
                if m: meta["desc"] = m.group(1)
                m = re.search(r'"aliases"\s*:\s*\[(.*?)\]', data, re.DOTALL)
                if m:
                    aliases_str = m.group(1)
                    meta["aliases"] = [a.strip().strip('\'"') for a in aliases_str.split(',') if a.strip()]
        except: pass
    return meta

def list_assets():
    if not os.path.exists(ASCII_DIR):
        return []
    return [f for f in os.listdir(ASCII_DIR) if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe", ".py"] and f != "__init__.py"]

def launcher_command(ext, path, args):
    if ext in [".bat", ".cmd"]:
        return ["cmd", "/c", path]
    if ext == ".ps1":
        return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path]
    if ext == ".vbs":
        return ["cscript", "//nologo", path]
    if ext == ".exe":
        return [path]
    if ext == ".py":
        return [sys.executable, path]
    return [path]

def show_help():
    print(f"\n{Color.BOLD}ASCII CENTER HELP{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 30}{Color.RESET}")
    print(f"{Color.GREEN}ID / Name{Color.RESET}   - Enter ID or name to launch.")
    print(f"{Color.GREEN}menu{Color.RESET}        - Return to the main menu.")
    print(f"{Color.GREEN}help / h{Color.RESET}    - Show help.")
    print(f"{Color.GREEN}exit / q{Color.RESET}    - Close the launcher.")
    print(f"{Color.GRAY}{'=' * 30}{Color.RESET}")
    input("\nPress Enter...")

@command(name="ascii", aliases=["art", "a"])
def run(*args):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.CYAN}{HEADER}{Color.RESET}")
        
        files = list_assets()
        if not files:
            print(f"{Color.YELLOW}[!] No assets found in /ascii.{Color.RESET}")
            input("Enter...")
            return
        
        print(f"{Color.BOLD}{'ID':<2} | {'ASSET':<17} | {'DESCRIPTION':<45} | {'ALIASES':<19}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 86}{Color.RESET}")
        
        assets_map = {}
        for idx, filename in enumerate(sorted(files), 1):
            name = os.path.splitext(filename)[0]
            meta = get_json_metadata(filename)
            full_path = os.path.join(ASCII_DIR, filename)
            assets_map[str(idx)] = (name, full_path)
            assets_map[name.lower()] = (name, full_path)
            aliases_str = ', '.join(meta['aliases']) if meta['aliases'] else ""
            print(f"{Color.GREEN}{idx:<2}{Color.RESET} | {Color.WHITE}{name:<17}{Color.RESET} | {meta['desc']:<45} | {aliases_str:<19}")
        
        while True:
            try:
                choice = input(f"\n{Color.CYAN}psASCII > {Color.RESET}").strip().lower()
            except:
                return
            
            if choice in ['help', 'h', '?']:
                show_help()
                break
            if choice == 'menu':
                os.system('cls' if os.name == 'nt' else 'clear')
                return
            if choice in ['q', 'exit', 'quit']:
                return
            
            parts = choice.split()
            key = parts[0]
            extra = parts[1:]
            if key in assets_map:
                name, path = assets_map[key]
                ext = os.path.splitext(path)[1].lower()
                print(f"{Color.YELLOW}[*] Starting: {name}{Color.RESET}")
                cmd = launcher_command(ext, path, extra) + extra
                try:
                    subprocess.Popen(cmd, shell=False, cwd=ASCII_DIR, creationflags=subprocess.CREATE_NEW_CONSOLE)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] {e}{Color.RESET}")
            else:
                print(f"{Color.RED}[!] Unknown command: {choice}.{Color.RESET}")

if __name__ == "__main__":
    run()
