import os
import sys
import subprocess
import re
import importlib
import inspect
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "sys.health"
__group__ = "menu"
__desc__ = "Health Center - launcher for system maintenance and health tools"

HEALTH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "health"))
METADATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "metadata"))
PLUGINS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

HEADER = r"""
     __  __            _ _   _     ___            _            
    |  \/  |          | | | | |   / __|          | |           
    | |\/| |___   __ _| | |_| |__| |_       ___  | |__   ___   
    | |  | / _ \ / _` | |  _  / _` | |_    / _ \ | '_ \ / _ \  
    | |  | | (_) | (_| | | | | (_| | | |_ | (_) || | | | (_) | 
    |_|  |_|\___/ \__,_|_|_| |_\__,_|_|\__| \___/ |_| |_|\___/  
"""

def get_metadata(filename):
    """Reads tool description and metadata."""
    meta = {"desc": "No description", "aliases": []}
    base = f"{filename}.json"
    json_path = os.path.join(METADATA_DIR, base)
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = f.read()
                m = re.search(r'"desc"\s*:\s*"([^"]+)"', data)
                if m: meta["desc"] = m.group(1)
                m = re.search(r'"aliases"\s*:\s*\[(.*?)\]', data, re.DOTALL)
                if m:
                    aliases_str = m.group(1)
                    meta["aliases"] = [a.strip().strip('\'"') for a in aliases_str.split(',') if a.strip()]
        except:
            pass
    return meta

def list_tools():
    """Returns list of health tools from health directory."""
    if not os.path.exists(HEALTH_DIR):
        return []
    return [f for f in os.listdir(HEALTH_DIR) 
            if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"] 
            and f != "__init__.py"]

def list_modules():
    """Returns list of available Python modules from plugins directory."""
    modules = []
    try:
        if os.path.exists(PLUGINS_DIR):
            for f in os.listdir(PLUGINS_DIR):
                if f.endswith('.py') and not f.startswith('__'):
                    modules.append(f)
    except:
        pass
    return sorted(modules)

def launcher_command(ext, path):
    """Returns appropriate command based on file extension."""
    if ext in [".bat", ".cmd"]:
        return ["cmd", "/c", path]
    if ext == ".ps1":
        return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path]
    if ext == ".vbs":
        return ["cscript", "//nologo", path]
    if ext == ".exe":
        return [path]
    return [path]

def load_and_execute_module(module_name):
    """Load and execute a Python module function."""
    try:
        if PLUGINS_DIR not in sys.path:
            sys.path.insert(0, PLUGINS_DIR)
        
        # Import the module dynamically
        module = importlib.import_module(module_name.replace('.py', ''))
        
        # Find and execute the first command function
        for name, obj in inspect.getmembers(module):
            if callable(obj) and hasattr(obj, 'is_command'):
                print(f"{Color.YELLOW}[*] Executing: {obj.command_name}...{Color.RESET}")
                obj()
                return True
        
        print(f"{Color.YELLOW}[!] No executable command found in {module_name}{Color.RESET}")
        return False
    except Exception as e:
        print(f"{Color.RED}[ERROR] Failed to execute module {module_name}: {e}{Color.RESET}")
        return False

def show_help():
    """Displays help information for the Health Center."""
    print(f"\n{Color.BOLD}HEALTH CENTER HELP{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 50}{Color.RESET}")
    print(f"{Color.GREEN}ID / Name{Color.RESET}     - Type the tool ID or name to launch it.")
    print(f"{Color.GREEN}modules{Color.RESET}       - List and execute Python modules.")
    print(f"{Color.GREEN}menu{Color.RESET}          - Return to the main TERMINAL CLI menu.")
    print(f"{Color.GREEN}help / h{Color.RESET}      - Show this help message.")
    print(f"{Color.GREEN}exit / q{Color.RESET}      - Close the launcher.")
    print(f"{Color.GRAY}{'=' * 50}{Color.RESET}")
    input("\nPress Enter to continue...")

@command(name="health", aliases=["h", "sys", "rescue", "hh"])
def health_dispatcher(*args):
    """Health Center launcher for system maintenance tools."""
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.CYAN}{HEADER}{Color.RESET}")
        
        files = list_tools()
        
        if not files:
            print(f"{Color.YELLOW}[!] No tools found in /health folder.{Color.RESET}")
            input("Press Enter...")
            return

        print(f"{Color.BOLD}{'ID':<2} | {'TOOL':<17} | {'DESCRIPTION':<45} | {'ALIASES':<19}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 90}{Color.RESET}")

        tools_map = {}
        # Create list with metadata for sorting
        files_with_meta = []
        for filename in files:
            name = os.path.splitext(filename)[0]
            meta = get_metadata(filename)
            files_with_meta.append((filename, name, meta))
        
        # Sort by group, category, then name
        sorted_files = sorted(files_with_meta, key=lambda x: (
            str(x[2].get('group', '')).lower(),
            str(x[2].get('category', '')).lower(),
            x[1].lower()
        ))
        
        for idx, (filename, name, meta) in enumerate(sorted_files, 1):
            full_path = os.path.join(HEALTH_DIR, filename)
            tools_map[str(idx)] = (name, full_path)
            tools_map[name.lower()] = (name, full_path)
            # Add aliases to tools_map
            for alias in meta.get('aliases', []):
                tools_map[alias.lower()] = (name, full_path)
            aliases_str = ', '.join(meta.get('aliases', [])) if meta.get('aliases') else ""
            print(f"{Color.GREEN}{idx:<2}{Color.RESET} | {Color.WHITE}{name:<17}{Color.RESET} | {meta.get('desc', 'No description'):<45} | {aliases_str:<19}")

        while True:
            try:
                choice = input(f"\n{Color.CYAN}psHEALTH > {Color.RESET}").strip().lower()
            except:
                return

            if choice in ['help', 'h', '?']:
                show_help()
                break  # Refresh the main view after help

            if choice == 'modules':
                show_modules_menu()
                break

            if choice == 'menu':
                os.system('cls' if os.name == 'nt' else 'clear')
                return

            if choice in ['q', 'exit', 'quit']:
                return

            if choice in tools_map:
                tool_name, path = tools_map[choice]
                ext = os.path.splitext(path)[1].lower()
                print(f"{Color.YELLOW}[*] Starting: {tool_name}...{Color.RESET}")
                cmd = launcher_command(ext, path)
                try:
                    subprocess.Popen(cmd, shell=False, cwd=HEALTH_DIR, creationflags=subprocess.CREATE_NEW_CONSOLE)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] {e}{Color.RESET}")
            else:
                print(f"{Color.RED}[!] Unknown command: {choice}. Type 'help' for options.{Color.RESET}")

def show_modules_menu():
    """Display and handle module selection menu."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.CYAN}{Color.BOLD}--- AVAILABLE MODULES MENU ---{Color.RESET}")
        print(f"{Color.GRAY}{'=' * 50}{Color.RESET}\n")
        
        modules = list_modules()
        if not modules:
            print(f"{Color.YELLOW}[!] No modules found.{Color.RESET}")
            input("Press Enter to continue...")
            return
        
        modules_map = {}
        for idx, mod_name in enumerate(modules, 1):
            modules_map[str(idx)] = mod_name
            modules_map[mod_name.replace('.py', '').lower()] = mod_name
            print(f"{Color.GREEN}{idx:<2}{Color.RESET} | {Color.WHITE}{mod_name:<30}{Color.RESET}")
        
        print(f"\n{Color.GRAY}{'-' * 50}{Color.RESET}")
        
        try:
            choice = input(f"\n{Color.CYAN}psHEALTH [Modules] > {Color.RESET}").strip().lower()
        except:
            return
        
        if choice in ['back', 'menu', 'q', 'exit', 'quit']:
            return
        
        if choice in modules_map:
            module_name = modules_map[choice]
            load_and_execute_module(module_name)
            input(f"\n{Color.YELLOW}Press Enter to continue...{Color.RESET}")
        else:
            print(f"{Color.RED}[!] Invalid choice.{Color.RESET}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    health_dispatcher()
