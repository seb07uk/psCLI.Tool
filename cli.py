import os
import sys
import subprocess
import inspect
import importlib
import json

# --- ANSI COLOR CONFIGURATION ---
class Color:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'  # Added to prevent "AttributeError"
    BOLD = '\033[1m'
    RESET = '\033[0m'

if sys.platform == "win32":
    os.system('color')

# --- DECORATOR ---
def command(name=None, aliases=None):
    def decorator(func):
        func.is_command = True
        func.command_name = name if name else func.__name__
        func.aliases = aliases if aliases else []
        func.meta = {}
        return func
    return decorator

# --- DISPATCHER CLASS ---
class Dispatcher:
    def __init__(self, plugins_folder="plugins", metadata_folder="metadata"):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugins_path = os.path.join(self.root_dir, plugins_folder)
        self.metadata_path = os.path.join(self.root_dir, metadata_folder)
        self.commands = {}
        self.aliases = {}
        self._prepare_env()

    def _prepare_env(self):
        """Creates necessary folders and files."""
        try:
            for folder in [self.plugins_path, self.metadata_path]:
                if not os.path.exists(folder):
                    os.makedirs(folder)
            init_file = os.path.join(self.plugins_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w", encoding="utf-8") as f:
                    f.write("# Init file\n")
            if self.root_dir not in sys.path:
                sys.path.insert(0, self.root_dir)
        except Exception as e:
            print(f"{Color.RED}[FATAL] Could not prepare environment: {e}{Color.RESET}")

    def _get_json_metadata(self, filename):
        """Safely reads JSON metadata for external binaries."""
        meta = {"author": "System", "category": "utility", "group": "external", "desc": "No description", "aliases": []}
        meta_file = os.path.join(self.metadata_path, f"{filename}.json")
        if os.path.exists(meta_file):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        meta.update(data)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Metadata error in {filename}: {e}{Color.RESET}")
        return meta

    def load_plugins(self):
        """Loads all plugins from the plugins folder."""
        self.commands.clear()
        self.aliases.clear()
        if not os.path.exists(self.plugins_path):
            print(f"{Color.RED}[ERROR] Plugins folder missing!{Color.RESET}")
            return

        for filename in os.listdir(self.plugins_path):
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            full_path = os.path.join(self.plugins_path, filename)
            
            if os.path.isdir(full_path) or filename.startswith("__"):
                continue

            try:
                if ext == ".py":
                    self._load_python_module(name)
                elif ext in [".bat", ".cmd", ".ps1", ".exe", ".vbs"]:
                    self._register_external_binary(filename, name, ext, full_path)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Failed to load {filename}: {e}{Color.RESET}")

    def _load_python_module(self, name):
        """Imports Python module and registers decorated functions."""
        try:
            mod_name = f"plugins.{name}"
            if mod_name in sys.modules:
                del sys.modules[mod_name]
            
            module = importlib.import_module(mod_name)
            module_meta = {
                "author": getattr(module, "__author__", "Unknown"),
                "category": getattr(module, "__category__", "general"),
                "group": getattr(module, "__group__", "python"),
                "desc": getattr(module, "__desc__", None)
            }

            for _, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and hasattr(obj, "is_command"):
                    cmd_name = getattr(obj, "command_name", _)
                    if not module_meta["desc"]:
                        module_meta["desc"] = (obj.__doc__ or "No description").strip().split('\n')[0]
                    obj.meta = module_meta
                    self.commands[cmd_name] = obj
                    for alias in getattr(obj, "aliases", []):
                        self.aliases[alias] = cmd_name
        except Exception as e:
            print(f"{Color.RED}[ERROR] Module {name}.py: {e}{Color.RESET}")

    def _register_external_binary(self, filename, name, ext, path):
        """Registers non-python files as commands."""
        meta = self._get_json_metadata(filename)
        def external_call(*args):
            cmd_args = ["powershell", "-ExecutionPolicy", "Bypass", "-File", path] if ext == ".ps1" else \
                       ["cscript", "//nologo", path] if ext == ".vbs" else [path]
            try:
                subprocess.run(cmd_args + list(args), shell=(ext in [".bat", ".cmd"]), check=True)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Execution failed: {e}{Color.RESET}")

        external_call.is_command = True
        external_call.meta = meta
        self.commands[name] = external_call
        for alias in meta.get("aliases", []):
            self.aliases[alias] = name

    def display_help(self):
        """Displays formatted help table with group-based separators."""
        if not self.commands:
            print(f"{Color.YELLOW}[!] Command system is empty.{Color.RESET}")
            return

        w = {"group": 8, "cmd": 12, "desc": 40, "cat": 12}
        
        sorted_cmds = sorted(self.commands.items(), 
                            key=lambda x: (str(x[1].meta.get('group', '')).lower(), 
                                           str(x[1].meta.get('category', '')).lower(), 
                                           x[0].lower()))

        print(f"\n{Color.CYAN}{Color.BOLD}ROOT:{Color.RESET} {Color.GRAY}{self.root_dir}{Color.RESET}")
        header = f"{'GROUP':<{w['group']}} | {'COMMAND':<{w['cmd']}} | {'DESCRIPTION':<{w['desc']}} | {'CATEGORY':<{w['cat']}} | ALIASES"
        sep_width = len(header) + 12
        full_line = f"{Color.GRAY}{'-' * sep_width}{Color.RESET}"
        
        print(full_line + "\n" + Color.BOLD + header + Color.RESET + "\n" + full_line)

        last_group = None
        for name, func in sorted_cmds:
            m = func.meta
            curr_group = str(m.get('group', 'python')).lower()
            
            if last_group is not None and last_group != curr_group:
                print(f"{Color.GRAY}{'-' * sep_width}{Color.RESET}")
            last_group = curr_group

            desc = (m.get("desc") or "None").strip()[:w['desc']]
            aliases = ", ".join([a for a, t in self.aliases.items() if t == name]) or "-"
            
            print(f"{Color.BLUE}{str(m.get('group')):<{w['group']}}{Color.RESET} {Color.GRAY}|{Color.RESET} "
                  f"{Color.GREEN}{Color.BOLD}{name:<{w['cmd']}}{Color.RESET} {Color.GRAY}|{Color.RESET} "
                  f"{desc:<{w['desc']}} {Color.GRAY}|{Color.RESET} "
                  f"{Color.CYAN}{str(m.get('category')):<{w['cat']}}{Color.RESET} {Color.GRAY}|{Color.RESET} "
                  f"{Color.YELLOW}{aliases}{Color.RESET}")
        
        print(full_line + "\n")

    def execute(self, trigger, *args):
        """Executes the command or its alias."""
        target = self.aliases.get(trigger, trigger)
        if target in self.commands:
            try:
                self.commands[target](*args)
            except Exception as e:
                print(f"{Color.RED}[RUNTIME ERROR] '{trigger}': {e}{Color.RESET}")
        else:
            print(f"{Color.RED}[?] Unknown command: '{trigger}'{Color.RESET}")

if __name__ == "__main__":
    cli = Dispatcher()
    cli.load_plugins()
    
    if len(sys.argv) < 2:
        cli.display_help()
        while True:
            try:
                prompt = f"{Color.CYAN}{os.path.basename(cli.root_dir)}{Color.RESET} > "
                user_input = input(prompt).strip().split()
                if not user_input: continue
                
                cmd = user_input[0].lower()
                
                # Handling built-in commands
                if cmd in ["exit", "quit"]: break
                if cmd in ["help", "?"]: 
                    cli.display_help()
                    continue
                if cmd in ["reload", "r"]: 
                    cli.load_plugins()
                    cli.display_help()
                    continue
                
                # Execute registered commands or aliases
                cli.execute(cmd, *user_input[1:])
            except (EOFError, KeyboardInterrupt):
                print(f"\n{Color.YELLOW}[!] Closing session...{Color.RESET}")
                break
    else:
        cli.execute(sys.argv[1], *sys.argv[2:])