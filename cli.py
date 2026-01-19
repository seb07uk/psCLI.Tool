import os
import sys
import subprocess
import inspect
import importlib
import json
import socket
import urllib.request
import platform
import threading
import webbrowser

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

    def _register_external_binary(self, filename, name, ext, path):
        meta = self._get_json_metadata(filename)
        def external_call(*args):
            cmd_args = ["powershell", "-ExecutionPolicy", "Bypass", "-File", path] if ext == ".ps1" else \
                       ["cscript", "//nologo", path] if ext == ".vbs" else [path]
            try:
                subprocess.run(cmd_args + list(args), shell=(ext in [".bat", ".cmd"]), check=True)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Execution: {e}{Color.RESET}")

        external_call.is_command = True
        external_call.meta = meta
        self.commands[name] = external_call
        for alias in meta.get("aliases", []):
            self.aliases[alias] = name

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
        target = self.aliases.get(trigger, trigger)
        if target in self.commands:
            try:
                self.commands[target](*args)
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
                # F1 on Windows is \x00K in extended key mode
                if key == b'\x00':
                    next_key = msvcrt.getch()
                    if next_key == b'?':  # F1 key
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
                
                prompt_fmt = cli.settings.get("ui", {}).get("default_prompt", "{root_dir} > ")
                prompt_text = prompt_fmt.format(root_dir=os.path.basename(cli.root_dir))
                prompt = f"{Color.CYAN}{prompt_text}{Color.RESET}"
                
                user_input = input(prompt).strip().split()
                if not user_input: continue
                
                cmd = user_input[0]
                # Treat '#' as alias for 'menu' - check before .lower()
                if cmd == "#":
                    cmd = "menuallweb"
                else:
                    cmd = cmd.lower()
                
                args = user_input[1:]
                
                if cmd in ["exit", "quit"]: break
                
                if cmd == "all":
                    cli.display_list()
                    continue
                
                if cmd == "menu":
                    cli.display_list("menu")
                    continue

                if cmd in ["reload", "r"]: 
                    cli.settings = cli._load_settings()
                    cli.load_plugins()
                    groups = cli.get_all_groups()
                    cli.display_list("menu" if "menu" in groups else None)
                    continue

                if cmd in cli.get_all_groups():
                    cli.display_list(cmd)
                    continue
                
                cli.execute(cmd, *args)

            except (EOFError, KeyboardInterrupt):
                break
    else:
        cli.execute(sys.argv[1], *sys.argv[2:])
