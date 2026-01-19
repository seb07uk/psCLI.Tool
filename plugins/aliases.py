import os
import sys
import re
import importlib
import inspect
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "utilities"
__group__ = "menu"
__desc__ = "Aliases Manager - displays all available modules, commands and their aliases"

PLUGINS_DIR = os.path.abspath(os.path.dirname(__file__))
METADATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "metadata"))
HEALTH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "health"))
TOOLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools"))
GAMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "games"))
ASCII_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ascii"))

def get_metadata_from_json(filename):
    """Read metadata from JSON file."""
    meta = {"desc": "No description", "aliases": [], "group": "", "category": ""}
    base = f"{filename}.json"
    json_path = os.path.join(METADATA_DIR, base)
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = f.read()
                m = re.search(r'"desc"\s*:\s*"([^"]+)"', data)
                if m: meta["desc"] = m.group(1)
                m = re.search(r'"group"\s*:\s*"([^"]+)"', data)
                if m: meta["group"] = m.group(1)
                m = re.search(r'"category"\s*:\s*"([^"]+)"', data)
                if m: meta["category"] = m.group(1)
                m = re.search(r'"aliases"\s*:\s*\[(.*?)\]', data, re.DOTALL)
                if m:
                    aliases_str = m.group(1)
                    meta["aliases"] = [a.strip().strip('\'"') for a in aliases_str.split(',') if a.strip()]
        except:
            pass
    return meta

def get_python_modules():
    """Load all Python modules with their command info."""
    modules = []
    try:
        if os.path.exists(PLUGINS_DIR):
            for f in os.listdir(PLUGINS_DIR):
                if f.endswith('.py') and not f.startswith('__'):
                    name = f.replace('.py', '')
                    try:
                        mod = importlib.import_module(f"plugins.{name}")
                        for _, obj in inspect.getmembers(mod):
                            if callable(obj) and hasattr(obj, 'is_command'):
                                cmd_name = getattr(obj, 'command_name', name)
                                aliases = getattr(obj, 'aliases', [])
                                desc = getattr(mod, '__desc__', 'No description')
                                group = getattr(mod, '__group__', 'python')
                                category = getattr(mod, '__category__', 'general')
                                modules.append({
                                    'type': 'Python Module',
                                    'file': f,
                                    'command': cmd_name,
                                    'aliases': aliases,
                                    'desc': desc,
                                    'group': group,
                                    'category': category
                                })
                    except:
                        pass
    except:
        pass
    return modules

def get_health_tools():
    """Load all health tools with metadata."""
    tools = []
    try:
        if os.path.exists(HEALTH_DIR):
            for f in os.listdir(HEALTH_DIR):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = get_metadata_from_json(f)
                    tools.append({
                        'type': 'Health Tool',
                        'file': f,
                        'name': name,
                        'aliases': meta.get('aliases', []),
                        'desc': meta.get('desc', 'No description'),
                        'group': meta.get('group', 'health'),
                        'category': meta.get('category', 'tool')
                    })
    except:
        pass
    return tools

def get_system_tools():
    """Load all system tools with metadata."""
    tools = []
    try:
        if os.path.exists(TOOLS_DIR):
            for f in os.listdir(TOOLS_DIR):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = get_metadata_from_json(f)
                    tools.append({
                        'type': 'System Tool',
                        'file': f,
                        'name': name,
                        'aliases': meta.get('aliases', []),
                        'desc': meta.get('desc', 'No description'),
                        'group': meta.get('group', 'system'),
                        'category': meta.get('category', 'tool')
                    })
    except:
        pass
    return tools

def get_games():
    """Load all games with metadata."""
    games = []
    try:
        if os.path.exists(GAMES_DIR):
            for f in os.listdir(GAMES_DIR):
                if f.endswith('.py') and not f.startswith('__'):
                    name = os.path.splitext(f)[0]
                    meta = get_metadata_from_json(f)
                    games.append({
                        'type': 'Game',
                        'file': f,
                        'name': name,
                        'aliases': meta.get('aliases', []),
                        'desc': meta.get('desc', 'No description'),
                        'group': meta.get('group', 'games'),
                        'category': meta.get('category', 'game')
                    })
    except:
        pass
    return games

def get_ascii_tools():
    """Load all ASCII tools with metadata."""
    tools = []
    try:
        if os.path.exists(ASCII_DIR):
            for f in os.listdir(ASCII_DIR):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = get_metadata_from_json(f)
                    tools.append({
                        'type': 'ASCII Tool',
                        'file': f,
                        'name': name,
                        'aliases': meta.get('aliases', []),
                        'desc': meta.get('desc', 'No description'),
                        'group': meta.get('group', 'ascii'),
                        'category': meta.get('category', 'tool')
                    })
    except:
        pass
    return tools

def display_all():
    """Display all loaded modules, tools and aliases."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Color.CYAN}{Color.BOLD}ALL AVAILABLE MODULES, COMMANDS & ALIASES{Color.RESET}\n")
    print(f"{Color.BOLD}{'NAME/COMMAND':<25} | {'DESCRIPTION':<45} | {'ALIASES':<25}{Color.RESET}")
    print(f"{Color.GRAY}{'-' * 100}{Color.RESET}")
    
    # Load all data
    py_modules = get_python_modules()
    health_tools = get_health_tools()
    system_tools = get_system_tools()
    games = get_games()
    ascii_tools = get_ascii_tools()
    
    # Display Python Modules
    if py_modules:
        print(f"{Color.CYAN}--- Python Modules ---{Color.RESET}")
        sorted_py = sorted(py_modules, key=lambda x: (
            str(x.get('group', '')).lower(),
            str(x.get('category', '')).lower(),
            x.get('command', '').lower()
        ))
        for mod in sorted_py:
            aliases_str = ', '.join(mod['aliases']) if mod['aliases'] else ""
            desc = mod['desc'][:45]
            print(f"{Color.CYAN}{mod['command']:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
    
    # Display Health Tools
    if health_tools:
        print(f"\n{Color.YELLOW}--- Health Tools ---{Color.RESET}")
        sorted_health = sorted(health_tools, key=lambda x: (
            str(x.get('group', '')).lower(),
            str(x.get('category', '')).lower(),
            x.get('name', '').lower()
        ))
        for tool in sorted_health:
            aliases_str = ', '.join(tool['aliases']) if tool['aliases'] else ""
            desc = tool['desc'][:45]
            print(f"{Color.WHITE}{tool['name']:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
    
    # Display System Tools
    if system_tools:
        print(f"\n{Color.MAGENTA}--- System Tools ---{Color.RESET}")
        sorted_system = sorted(system_tools, key=lambda x: (
            str(x.get('group', '')).lower(),
            str(x.get('category', '')).lower(),
            x.get('name', '').lower()
        ))
        for tool in sorted_system:
            aliases_str = ', '.join(tool['aliases']) if tool['aliases'] else ""
            desc = tool['desc'][:45]
            print(f"{Color.WHITE}{tool['name']:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
    
    # Display Games
    if games:
        print(f"\n{Color.GREEN}--- Games ---{Color.RESET}")
        sorted_games = sorted(games, key=lambda x: (
            str(x.get('group', '')).lower(),
            str(x.get('category', '')).lower(),
            x.get('name', '').lower()
        ))
        for game in sorted_games:
            aliases_str = ', '.join(game['aliases']) if game['aliases'] else ""
            desc = game['desc'][:45]
            print(f"{Color.WHITE}{game['name']:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
    
    # Display ASCII Tools
    if ascii_tools:
        print(f"\n{Color.BLUE}--- ASCII Tools ---{Color.RESET}")
        sorted_ascii = sorted(ascii_tools, key=lambda x: (
            str(x.get('group', '')).lower(),
            str(x.get('category', '')).lower(),
            x.get('name', '').lower()
        ))
        for tool in sorted_ascii:
            aliases_str = ', '.join(tool['aliases']) if tool['aliases'] else ""
            desc = tool['desc'][:45]
            print(f"{Color.WHITE}{tool['name']:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
    
    print(f"\n{Color.GRAY}{'-' * 100}{Color.RESET}")

@command(name="aliases", aliases=["mod", "modules", "list"])
def aliases_dispatcher(*args):
    """Display all available modules, commands and their aliases."""
    display_all()
    input(f"\n{Color.CYAN}Press Enter to continue...{Color.RESET}")

if __name__ == "__main__":
    aliases_dispatcher()
