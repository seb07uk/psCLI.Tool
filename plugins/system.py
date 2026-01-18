import os
import sys
import re
import subprocess
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "system"
__group__ = "menu"
__desc__ = "System Tools - launcher for system utilities and administration tools"

HEADER = r"""
               _
             | |
             | |===( )   //////
             |_|   |||  | o o|                                              _.-;;-._
                    ||| ( c  )                  ____                 '-..-'|   ||   |
                     ||| \= /                  ||   \_               '-..-'|_.-;;-._|
                      ||| \\ /                  ||     |             '-..-'|   ||   |
                       ||||||                   ||__/|-"             '-..-'|_.-''-._|
                       ||||||             __|________|__
                         |||             |______________|
                         |||             || ||      || ||
                         |||             || ||      || ||
------------------------|||-------------||-||------||-||-------
                         |__>            || ||      || ||
"""

TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
METADATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "metadata"))

def get_metadata(filename):
    """Reads tool description from JSON metadata file."""
    base = f"{filename}.json"
    path = os.path.join(METADATA_DIR, base)
    meta = {"desc": "No description", "aliases": [], "group": ""}
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
                m = re.search(r'"desc"\s*:\s*"([^"]+)"', data)
                if m: meta["desc"] = m.group(1)
                m = re.search(r'"group"\s*:\s*"([^"]+)"', data)
                if m: meta["group"] = m.group(1)
                m = re.search(r'"aliases"\s*:\s*\[(.*?)\]', data, re.DOTALL)
                if m:
                    aliases_str = m.group(1)
                    meta["aliases"] = [a.strip().strip('\'"') for a in aliases_str.split(',') if a.strip()]
        except: pass
    return meta

def list_tools():
    """Lists all available system tools."""
    if not os.path.exists(TOOLS_DIR):
        return []
    return [f for f in os.listdir(TOOLS_DIR) if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe", ".py"] and f != "__init__.py"]

def launcher_command(ext, path, args):
    """Returns the appropriate command to launch a tool based on file extension."""
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
    """Displays help information for the System Tools launcher."""
    print(f"\n{Color.BOLD}SYSTEM TOOLS HELP{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 30}{Color.RESET}")
    print(f"{Color.GREEN}ID / Name{Color.RESET}   - Type the tool ID or name to launch it.")
    print(f"{Color.GREEN}menu{Color.RESET}        - Return to the main TERMINAL CLI menu.")
    print(f"{Color.GREEN}help / h{Color.RESET}    - Show this help message.")
    print(f"{Color.GREEN}exit / q{Color.RESET}    - Close the launcher.")
    print(f"{Color.GRAY}{'=' * 30}{Color.RESET}")
    input("\nPress Enter to continue...")

@command(name="system", aliases=["sys", "tools", "s"])
def run(*args):
    """System Tools launcher for TERMINAL CLI."""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.CYAN}{HEADER}{Color.RESET}")
        
        tools = list_tools()
        if not tools:
            print(f"{Color.YELLOW}[!] No tools found in /tools folder.{Color.RESET}")
            input("Press Enter...")
            return
        
        print(f"{Color.BOLD}{'ID':<2} | {'TOOL':<17} | {'DESCRIPTION':<45} | {'ALIASES':<19}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 86}{Color.RESET}")
        
        tools_map = {}
        display_idx = 0
        for filename in sorted(tools):
            name = os.path.splitext(filename)[0]
            meta = get_metadata(filename)
            # Filter by "system" group
            if meta['group'] != "system":
                continue
            display_idx += 1
            full_path = os.path.join(TOOLS_DIR, filename)
            tools_map[str(display_idx)] = (name, full_path)
            tools_map[name.lower()] = (name, full_path)
            aliases_str = ', '.join(meta['aliases']) if meta['aliases'] else ""
            print(f"{Color.GREEN}{display_idx:<2}{Color.RESET} | {Color.WHITE}{name:<17}{Color.RESET} | {meta['desc']:<45} | {aliases_str:<19}")
        
        while True:
            try:
                choice = input(f"\n{Color.CYAN}psSYSTEM > {Color.RESET}").strip().lower()
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
            if key in tools_map:
                name, path = tools_map[key]
                ext = os.path.splitext(path)[1].lower()
                print(f"{Color.YELLOW}[*] Starting: {name}{Color.RESET}")
                cmd = launcher_command(ext, path, extra) + extra
                try:
                    subprocess.Popen(cmd, shell=False, cwd=TOOLS_DIR, creationflags=subprocess.CREATE_NEW_CONSOLE)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] {e}{Color.RESET}")
            else:
                print(f"{Color.RED}[!] Unknown command: {choice}.{Color.RESET}")

if __name__ == "__main__":
    run()
