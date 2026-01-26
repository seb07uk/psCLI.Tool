import os
import sys
import subprocess
import inspect
import importlib
import importlib.util
import json
import socket
import urllib.request
import platform
import threading
import webbrowser
import re
import getpass

from plugins import owner

# Import msvcrt for Windows key detection
try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False


class Color:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'
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

# --- DISPATCHER CLASS (2026© Terminal psCLI) ---
class Dispatcher:
    def __init__(self, plugins_folder="plugins", metadata_folder="metadata"):
        if getattr(sys, "frozen", False):
            self.root_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        else:
            self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.settings_path = os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings\terminal.json")
        self.settings = self._load_settings()
        
        self.plugins_path = os.path.join(self.root_dir, self.settings.get("dispatcher", {}).get("plugins_folder", plugins_folder))
        self.metadata_path = os.path.join(self.root_dir, self.settings.get("dispatcher", {}).get("metadata_folder", metadata_folder))
        
        self.commands = {}
        self.aliases = {}
        self._prepare_env()

    def _local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            try:
                return socket.gethostbyname(socket.gethostname())
            except:
                return None

    def _is_online(self):
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=2).close()
            return True
        except:
            return False

    def _public_ip(self):
        try:
            with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=3) as r:
                data = json.loads(r.read().decode("utf-8"))
                return data.get("ip")
        except:
            return None

    def _load_settings(self):
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Could not load settings: {e}{Color.RESET}")
        return {}

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _get_protected_commands(self):
        try:
            path = os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings\protected.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    lst = data.get("commands", [])
                    if isinstance(lst, list):
                        return set([str(x).lower() for x in lst])
        except:
            pass
        return set()

    def _prepare_env(self):
        try:
            folders = [
                self.plugins_path, 
                self.metadata_path, 
                os.path.dirname(self.settings_path),
                os.path.expandvars(r"%userprofile%\.polsoft\psCli\Calculator")
            ]
            for folder in folders:
                if not os.path.exists(folder):
                    os.makedirs(folder)

            init_file = os.path.join(self.plugins_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w", encoding="utf-8") as f:
                    f.write("# Init file\n")
            
            if self.root_dir not in sys.path:
                sys.path.insert(0, self.root_dir)
        except Exception as e:
            print(f"{Color.RED}[CRITICAL] Could not prepare environment: {e}{Color.RESET}")

    def open_html_report(self, filepath):
        """Open HTML report in default browser."""
        try:
            if os.path.exists(filepath):
                webbrowser.open(f"file:///{filepath.replace(chr(92), '/')}")
                print(f"{Color.GREEN}[OK] Opening report in default browser...{Color.RESET}")
            else:
                print(f"{Color.RED}[ERROR] File not found: {filepath}{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}[ERROR] Could not open HTML report: {e}{Color.RESET}")

    def get_html_reports(self):
        """Get list of generated HTML reports."""
        reports_dir = os.path.expandvars(r"%userprofile%\.polsoft\psCLI\reports")
        if not os.path.exists(reports_dir):
            return []
        
        try:
            reports = [f for f in os.listdir(reports_dir) if f.endswith('.html')]
            return sorted(reports, key=lambda x: os.path.getmtime(os.path.join(reports_dir, x)), reverse=True)
        except Exception as e:
            print(f"{Color.RED}[ERROR] Could not list reports: {e}{Color.RESET}")
            return []

    def _get_json_metadata(self, filename):
        meta = {"author": "System", "category": "utility", "group": "external", "desc": "No description", "aliases": []}
        meta_file = os.path.join(self.metadata_path, f"{filename}.json")
        if os.path.exists(meta_file):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        meta.update(data)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Metadata {filename}: {e}{Color.RESET}")
        return meta

    def get_all_groups(self):
        return {str(f.meta.get('group', 'python')).lower() for f in self.commands.values()}

    def load_plugins(self):
        self.commands.clear()
        self.aliases.clear()
        if not os.path.exists(self.plugins_path):
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
                print(f"{Color.RED}[ERROR] Loading {filename}: {e}{Color.RESET}")
        
        # Load games
        games_path = os.path.join(self.root_dir, "games")
        if os.path.exists(games_path):
            for filename in os.listdir(games_path):
                name, ext = os.path.splitext(filename)
                ext = ext.lower()
                full_path = os.path.join(games_path, filename)
                
                if os.path.isdir(full_path) or filename.startswith("__"):
                    continue
                
                try:
                    if ext == ".py":
                        self._load_game_module(name, full_path)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] Loading game {filename}: {e}{Color.RESET}")
        
        # Load ASCII tools
        ascii_path = os.path.join(self.root_dir, "ascii")
        if os.path.exists(ascii_path):
            for filename in os.listdir(ascii_path):
                name, ext = os.path.splitext(filename)
                ext = ext.lower()
                full_path = os.path.join(ascii_path, filename)
                
                if os.path.isdir(full_path) or filename.startswith("__"):
                    continue
                
                try:
                    if ext in [".bat", ".cmd", ".ps1", ".exe", ".vbs"]:
                        self._register_external_binary(filename, name, ext, full_path)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] Loading ASCII tool {filename}: {e}{Color.RESET}")

        
        tools_path = os.path.join(self.root_dir, "tools")
        if os.path.exists(tools_path):
            for filename in os.listdir(tools_path):
                name, ext = os.path.splitext(filename)
                ext = ext.lower()
                full_path = os.path.join(tools_path, filename)
                
                if os.path.isdir(full_path) or filename.startswith("__"):
                    continue
                
                try:
                    if ext in [".bat", ".cmd", ".ps1", ".exe", ".vbs"]:
                        self._register_external_binary(filename, name, ext, full_path)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] Loading tool {filename}: {e}{Color.RESET}")

        health_path = os.path.join(self.root_dir, "health")
        if os.path.exists(health_path):
            for filename in os.listdir(health_path):
                name, ext = os.path.splitext(filename)
                ext = ext.lower()
                full_path = os.path.join(health_path, filename)
                
                if os.path.isdir(full_path) or filename.startswith("__"):
                    continue
                
                try:
                    if ext in [".bat", ".cmd", ".ps1", ".exe", ".vbs"]:
                        self._register_external_binary(filename, name, ext, full_path)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] Loading health tool {filename}: {e}{Color.RESET}")

        install_path = os.path.join(self.root_dir, "install")
        if os.path.exists(install_path):
            for filename in os.listdir(install_path):
                name, ext = os.path.splitext(filename)
                ext = ext.lower()
                full_path = os.path.join(install_path, filename)
                
                if os.path.isdir(full_path) or filename.startswith("__"):
                    continue
                
                try:
                    if ext in [".bat", ".cmd", ".ps1", ".exe", ".vbs"]:
                        self._register_external_binary(filename, name, ext, full_path)
                except Exception as e:
                    print(f"{Color.RED}[ERROR] Loading installer {filename}: {e}{Color.RESET}")

        # Register root build script as command
        build_script = os.path.join(self.root_dir, "build.ps1")
        if os.path.exists(build_script):
            try:
                self._register_external_binary("build.ps1", "build", ".ps1", build_script)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Loading build.ps1: {e}{Color.RESET}")

    def _load_python_module(self, name):
        try:
            mod_name = f"plugins.{name}"
            if mod_name in sys.modules:
                del sys.modules[mod_name]
            
            module = importlib.import_module(mod_name)
            
            base_meta = {
                "author": getattr(module, "__author__", "Unknown"),
                "category": getattr(module, "__category__", "general"),
                "group": getattr(module, "__group__", "python"),
                "desc": getattr(module, "__desc__", None)
            }

            for _, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and hasattr(obj, "is_command"):
                    cmd_name = getattr(obj, "command_name", _)
                    cmd_meta = base_meta.copy()
                    
                    doc = (obj.__doc__ or "").strip().split('\n')[0]
                    if doc:
                        cmd_meta["desc"] = doc
                    elif not cmd_meta["desc"]:
                        cmd_meta["desc"] = "No description"

                    obj.meta = cmd_meta
                    self.commands[cmd_name] = obj
                    
                    for alias in getattr(obj, "aliases", []):
                        self.aliases[alias] = cmd_name
        except Exception as e:
            print(f"{Color.RED}[ERROR] Module {name}.py: {e}{Color.RESET}")

    def _load_game_module(self, name, full_path):
        """Load a game module from the games directory."""
        try:
            # Add games path to sys.path temporarily
            games_path = os.path.dirname(full_path)
            if games_path not in sys.path:
                sys.path.insert(0, games_path)
            
            # Import the game module
            if name in sys.modules:
                del sys.modules[name]
            
            spec = importlib.util.spec_from_file_location(name, full_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            
            # Try to load metadata from JSON first, then fallback to module attributes
            meta = self._get_metadata_from_json(name)
            
            # If JSON metadata is empty/default, try module attributes
            if meta.get("desc") == "No description":
                 meta["author"] = getattr(module, "__author__", "Unknown")
                 meta["category"] = getattr(module, "__category__", "games")
                 meta["group"] = getattr(module, "__group__", "games")
                 meta["desc"] = getattr(module, "__desc__", None)
            
            # Ensure group is set correctly if read from JSON
            if "group" not in meta:
                meta["group"] = getattr(module, "__group__", "games")

            base_meta = meta
            found_command = False

            for _, obj in inspect.getmembers(module):
                if inspect.isfunction(obj) and hasattr(obj, "is_command"):
                    found_command = True
                    cmd_name = getattr(obj, "command_name", name)
                    cmd_meta = base_meta.copy()
                    
                    doc = (obj.__doc__ or "").strip().split('\n')[0]
                    if doc:
                        cmd_meta["desc"] = doc
                    elif not cmd_meta["desc"]:
                        cmd_meta["desc"] = f"Game: {name}"

                    obj.meta = cmd_meta
                    self.commands[cmd_name] = obj
                    
                    for alias in getattr(obj, "aliases", []):
                        self.aliases[alias] = cmd_name
            
            # If no explicit command found, try to register main entry point
            if not found_command:
                entry_point = getattr(module, "main", getattr(module, "menu", None))
                if callable(entry_point):
                    def game_wrapper(*args):
                        entry_point()
                    
                    game_wrapper.is_command = True
                    game_wrapper.command_name = name
                    game_wrapper.meta = base_meta.copy()
                    if not game_wrapper.meta.get("desc"):
                        game_wrapper.meta["desc"] = f"Game: {name}"
                    
                    self.commands[name] = game_wrapper
                    
                    # Register aliases from metadata if any
                    for alias in base_meta.get("aliases", []):
                        self.aliases[alias] = name
            
            # Legacy fallback (can be removed if above covers all cases)
            if not found_command and name not in self.commands and hasattr(module, 'main'):
                 pass # Already handled above
                
        except Exception as e:
            print(f"{Color.RED}[ERROR] Loading game {name}.py: {e}{Color.RESET}")

    def _register_external_binary(self, filename, name, ext, full_path):
        """Register external binary files (.bat, .cmd, .ps1, .exe, .vbs)."""
        meta = self._get_metadata_from_json(filename)
        
        def external_call(*args):
            if ext == ".ps1":
                cmd_args = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", full_path]
                use_shell = False
            elif ext == ".vbs":
                cmd_args = ["cscript", "//nologo", full_path]
                use_shell = False
            elif ext in [".bat", ".cmd"]:
                cmd_args = ["cmd", "/c", full_path]
                use_shell = False
            else:
                cmd_args = [full_path]
                use_shell = False
            try:
                subprocess.run(cmd_args + list(args), shell=use_shell, check=True)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Execution: {e}{Color.RESET}")

        external_call.is_command = True
        external_call.meta = meta
        self.commands[name] = external_call
        
        for alias in meta.get("aliases", []):
            self.aliases[alias] = name

    def _get_metadata_from_json(self, filename):
        """Extract metadata from JSON file."""
        meta = {"desc": "No description", "aliases": [], "group": "utility", "category": "tool", "author": "Unknown"}
        base = f"{filename}.json"
        json_path = os.path.join(self.metadata_path, base)
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        meta.update(data)
            except Exception:
                pass
        return meta

    def display_all_modules(self):
        """Display all modules, tools and aliases from all directories."""
        if self.settings.get("ui", {}).get("clear_on_menu", True):
            self._clear_screen()
        
        print(f"{Color.CYAN}{Color.BOLD}ALL AVAILABLE MODULES, COMMANDS & ALIASES{Color.RESET}\n")
        print(f"{Color.BOLD}{'NAME/COMMAND':<25} | {'DESCRIPTION':<45} | {'ALIASES':<25}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 100}{Color.RESET}")
        
        # Python Modules (loaded commands)
        py_modules = []
        for name, func in self.commands.items():
            if str(func.meta.get('group', '')).lower() != "menu":
                aliases_str = ', '.join(func.meta.get('aliases', []))
                py_modules.append((name, func, aliases_str))
        
        if py_modules:
            print(f"{Color.CYAN}--- Python Modules ---{Color.RESET}")
        sorted_py = sorted(py_modules, key=lambda x: (
            str(x[1].meta.get('group', '')).lower(),
            str(x[1].meta.get('category', '')).lower(),
            x[0].lower()
        ))
        for name, func, aliases_str in sorted_py:
            desc = func.meta.get('desc', 'No description')[:45]
            print(f"{Color.CYAN}{name:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
        
        # Health Tools
        health_dir = os.path.join(self.root_dir, "health")
        if os.path.exists(health_dir):
            health_tools = []
            for f in os.listdir(health_dir):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = self._get_metadata_from_json(f)
                    health_tools.append((name, meta))
            
            if health_tools:
                print(f"\n{Color.YELLOW}--- Health Tools ---{Color.RESET}")
            sorted_health = sorted(health_tools, key=lambda x: (
                str(x[1].get('group', '')).lower(),
                str(x[1].get('category', '')).lower(),
                x[0].lower()
            ))
            for name, meta in sorted_health:
                aliases_str = ', '.join(meta.get('aliases', []))
                desc = meta.get('desc', 'No description')[:45]
                print(f"{Color.WHITE}{name:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
        
        # System Tools
        tools_dir = os.path.join(self.root_dir, "tools")
        if os.path.exists(tools_dir):
            system_tools = []
            for f in os.listdir(tools_dir):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = self._get_metadata_from_json(f)
                    system_tools.append((name, meta))
            
            if system_tools:
                print(f"\n{Color.MAGENTA}--- System Tools ---{Color.RESET}")
            sorted_system = sorted(system_tools, key=lambda x: (
                str(x[1].get('group', '')).lower(),
                str(x[1].get('category', '')).lower(),
                x[0].lower()
            ))
            for name, meta in sorted_system:
                aliases_str = ', '.join(meta.get('aliases', []))
                desc = meta.get('desc', 'No description')[:45]
                print(f"{Color.WHITE}{name:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
        
        # Games
        games_dir = os.path.join(self.root_dir, "games")
        if os.path.exists(games_dir):
            games = []
            for f in os.listdir(games_dir):
                if f.endswith('.py') and not f.startswith('__'):
                    name = os.path.splitext(f)[0]
                    meta = self._get_metadata_from_json(name)
                    games.append((name, meta))
            
            if games:
                print(f"\n{Color.GREEN}--- Games ---{Color.RESET}")
            sorted_games = sorted(games, key=lambda x: (
                str(x[1].get('group', '')).lower(),
                str(x[1].get('category', '')).lower(),
                x[0].lower()
            ))
            for name, meta in sorted_games:
                aliases_str = ', '.join(meta.get('aliases', []))
                desc = meta.get('desc', 'No description')[:45]
                print(f"{Color.WHITE}{name:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
        
        # ASCII Tools
        ascii_dir = os.path.join(self.root_dir, "ascii")
        if os.path.exists(ascii_dir):
            ascii_tools = []
            for f in os.listdir(ascii_dir):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = self._get_metadata_from_json(f)
                    ascii_tools.append((name, meta))
            
            if ascii_tools:
                print(f"\n{Color.BLUE}--- ASCII Tools ---{Color.RESET}")
            sorted_ascii = sorted(ascii_tools, key=lambda x: (
                str(x[1].get('group', '')).lower(),
                str(x[1].get('category', '')).lower(),
                x[0].lower()
            ))
            for name, meta in sorted_ascii:
                aliases_str = ', '.join(meta.get('aliases', []))
                desc = meta.get('desc', 'No description')[:45]
                print(f"{Color.WHITE}{name:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
        
        install_dir = os.path.join(self.root_dir, "install")
        if os.path.exists(install_dir):
            install_tools = []
            for f in os.listdir(install_dir):
                if os.path.splitext(f)[1].lower() in [".bat", ".cmd", ".ps1", ".vbs", ".exe"]:
                    name = os.path.splitext(f)[0]
                    meta = self._get_metadata_from_json(f)
                    install_tools.append((name, meta))
            
            if install_tools:
                print(f"\n{Color.CYAN}--- Installers ---{Color.RESET}")
            sorted_install = sorted(install_tools, key=lambda x: (
                str(x[1].get('group', '')).lower(),
                str(x[1].get('category', '')).lower(),
                x[0].lower()
            ))
            for name, meta in sorted_install:
                aliases_str = ', '.join(meta.get('aliases', []))
                desc = meta.get('desc', 'No description')[:45]
                print(f"{Color.WHITE}{name:<25}{Color.RESET} | {desc:<45} | {aliases_str:<25}")
        
        print(f"\n{Color.GRAY}{'-' * 100}{Color.RESET}")

    def display_list(self, filter_group=None):
        if self.settings.get("ui", {}).get("clear_on_menu", True):
            self._clear_screen()
            
        all_cmds = self.commands.items()
        
        if filter_group:
            filter_group = filter_group.lower()
            cmds_to_show = [(n, f) for n, f in all_cmds if str(f.meta.get('group', '')).lower() == filter_group]
            
            if filter_group == "menu":
                title = "2026© Terminal psCLI MENU (Type 'all' to see all available modules or a group name.)"
            else:
                title = f"GROUP VIEW: {filter_group.upper()}"
        else:
            cmds_to_show = [(n, f) for n, f in all_cmds if str(f.meta.get('group', '')).lower() != "menu"]
            title = "ALL MODULES (HIDDEN: MENU)"

        if not cmds_to_show:
            print(f"{Color.RED}[!] No modules in group: {filter_group if filter_group else 'general'}.{Color.RESET}")
            return

        w = {"group": 10, "cmd": 15, "desc": 45, "cat": 12}
        sorted_cmds = sorted(cmds_to_show, key=lambda x: (
            str(x[1].meta.get('group', '')).lower(), 
            str(x[1].meta.get('category', '')).lower(), 
            x[0].lower()
        ))

        print(f"{Color.CYAN}{Color.BOLD}{title}{Color.RESET}")
        try:
            owner_mod = importlib.import_module("plugins.owner")
            ni = owner_mod.get_network_info()
            online = bool(ni.get("online"))
            local_ip = ni.get("local_ip")
            public_ip = ni.get("public_ip")
            mac = owner_mod.get_preferred_mac() or ni.get("mac")
        except Exception:
            online = self._is_online()
            local_ip = self._local_ip()
            public_ip = self._public_ip() if online else None
            mac = None
        net_line = f"Network: {'Online' if online else 'Offline'}"
        if local_ip: net_line += f" | Local IP: {local_ip}"
        if public_ip: net_line += f" | Public IP: {public_ip}"
        if mac: net_line += f" | MAC: {mac}"
        print(f"{Color.GRAY}{net_line}{Color.RESET}")
        try:
            oi = owner_mod.get_os_info()
            os_line = f"OS: {oi.get('system')} {oi.get('release')}"
            if oi.get('build'): os_line += f" | Build: {oi.get('build')}"
            os_line += f" | Arch: {oi.get('machine')}"
            os_line += f" | Python: {oi.get('python_version')}"
        except Exception:
            os_line = f"OS: {platform.system()} {platform.release()} | Python: {sys.version.split()[0]}"
        os_line = os_line + " | " + Color.WHITE + Color.BOLD + "[f5] refresh" + Color.RESET
        print(f"{Color.GRAY}{os_line}{Color.RESET}")
        
        header = f"{'GROUP':<{w['group']}} | {'COMMAND':<{w['cmd']}} | {'DESCRIPTION':<{w['desc']}} | {'CATEGORY':<{w['cat']}} | ALIASES"
        sep_width = len(header) + 12
        full_line = f"{Color.GRAY}{'-' * sep_width}{Color.RESET}"
        
        print(full_line + "\n" + Color.BOLD + header + Color.RESET + "\n" + full_line)

        last_group = None
        for name, func in sorted_cmds:
            m = func.meta
            curr_group = str(m.get('group', 'python')).lower()
            if last_group is not None and last_group != curr_group and not filter_group:
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
        if trigger.lower() == "all":
            self.display_list()
            return
        if trigger.lower() in self.get_all_groups():
            self.display_list(trigger.lower())
            return
        if trigger.lower() in ["refresh", "f5", "reload", "r"]:
            self.settings = self._load_settings()
            self.load_plugins()
            groups = self.get_all_groups()
            self.display_list("menu" if "menu" in groups else None)
            return
        target = self.aliases.get(trigger, trigger)
        if target in self.commands:
            try:
                func = self.commands[target]
                grp = str(func.meta.get("group", "")).lower()
                protected = self._get_protected_commands()
                if target.lower() in protected:
                    try:
                        pm = importlib.import_module("plugins.passwd")
                        if not getattr(pm, "verify_once")():
                            print(f"{Color.RED}[!] Incorrect password{Color.RESET}")
                            return
                    except Exception:
                        entered = getpass.getpass(f"{Color.YELLOW}Password:{Color.RESET} ").strip()
                        if not entered:
                            print(f"{Color.RED}[!] Incorrect password{Color.RESET}")
                            return
                if grp == "mainte.":
                    expected = os.environ.get("PSCLI_MAINTE_PASS") or self.settings.get("security", {}).get("mainte_password") or "polsoft"
                    entered = getpass.getpass(f"{Color.YELLOW}Password:{Color.RESET} ").strip()
                    if entered != expected:
                        print(f"{Color.RED}[!] Incorrect password{Color.RESET}")
                        return
                func(*args)
            except Exception as e:
                print(f"{Color.RED}[RUNTIME ERROR] '{trigger}': {e}{Color.RESET}")
        else:
            print(f"{Color.RED}[?] Unknown command or group: '{trigger}'{Color.RESET}")

    def _check_f1_key(self):
        """Check for F1 key press in non-blocking way."""
        if not HAS_MSVCRT:
            return False
        try:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    next_key = msvcrt.getch()
                    if next_key == b';':
                        return True
        except:
            pass
        return False

    def _check_f5_key(self):
        if not HAS_MSVCRT:
            return False
        try:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in (b'\x00', b'\xe0'):
                    next_key = msvcrt.getch()
                    if next_key == b'?':
                        return True
        except:
            pass
        return False

# --- EXECUTION ---
if __name__ == "__main__":
    cli = Dispatcher()
    cli.load_plugins()
    
    if len(sys.argv) < 2:
        groups = cli.get_all_groups()
        if "menu" in groups:
            cli.display_list("menu")
        else:
            cli.display_list() 
            
        while True:
            try:
                # Check for F1 key press
                if cli._check_f1_key():
                    cli.display_list("core")
                    continue
                if hasattr(cli, "_check_f5_key") and cli._check_f5_key():
                    cli.settings = cli._load_settings()
                    cli.load_plugins()
                    groups = cli.get_all_groups()
                    cli.display_list("menu" if "menu" in groups else None)
                    continue
                
                prompt_fmt = cli.settings.get("ui", {}).get("default_prompt", "{root_dir} > ")
                prompt_text = prompt_fmt.format(root_dir=os.path.basename(cli.root_dir))
                prompt = f"{Color.CYAN}{prompt_text}{Color.RESET}"                
                raw_input = input(prompt).strip()
                if not raw_input: continue
                
                # Support command chaining with '&'
                # Handle quoted strings to avoid splitting '&' inside quotes could be complex, 
                # but for simple usage split('&') is a good start.
                commands = [c.strip() for c in raw_input.split('&') if c.strip()]
                
                should_break = False
                for cmd_str in commands:
                    user_input = cmd_str.split()
                    if not user_input: continue
                    
                    cmd = user_input[0]
                    # Treat '#' as alias for 'menu' - check before .lower()
                    if cmd == "#":
                        cmd = "menuallweb"
                    else:
                        cmd = cmd.lower()
                    
                    args = user_input[1:]
                    
                    if cmd in ["exit", "quit"]: 
                        should_break = True
                        break
                    
                    if cmd == "all":
                        cli.display_list()
                        continue
                    
                    if cmd in ["modules", "mod"]:
                        cli.display_all_modules()
                        continue
                    
                    if cmd == "menu":
                        cli.display_list("menu")
                        continue

                    if cmd in ["reload", "r", "refresh", "f5"]: 
                        cli.settings = cli._load_settings()
                        cli.load_plugins()
                        groups = cli.get_all_groups()
                        cli.display_list("menu" if "menu" in groups else None)
                        continue

                    if cmd in cli.get_all_groups():
                        cli.display_list(cmd)
                        continue
                    
                    cli.execute(cmd, *args)
                
                if should_break:
                    break

            except (EOFError, KeyboardInterrupt):
                break
    else:
        cli.execute(sys.argv[1], *sys.argv[2:])
