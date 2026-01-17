#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  psCLI - VIRTUAL ENVIRONMENT MANAGER
================================================================================
  File: plugins/venv.py
  Author: Sebastian Januchowski
  Version: 1.0.0
  Date: January 17, 2026
  License: MIT
================================================================================
  Complete virtual environment management system for psCLI.
  Create, activate, deactivate, and manage Python virtual environments.
================================================================================
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from cli import command, Color

# --- METADATA (Read by cli.py dispatcher) ---
__author__ = "Sebastian Januchowski"
__category__ = "environment"
__group__ = "system"
__desc__ = "Virtual environment manager - create, activate, and manage Python venvs"
__version__ = "1.0.0"

# ======================== COLOR CONSTANTS ========================
BOLD = Color.BOLD
RESET = Color.RESET
CYAN = Color.CYAN
GREEN = Color.GREEN
YELLOW = Color.YELLOW
GRAY = Color.GRAY
RED = Color.RED
WHITE = Color.WHITE
BLUE = Color.BLUE

# ======================== CONFIGURATION ========================
VENV_CONFIG_FILE = os.path.expandvars(r"%userprofile%\.polsoft\psCli\venv_config.json")
VENV_ROOT = os.path.expandvars(r"%userprofile%\.polsoft\psCli\venvs")

# ======================== UTILITY FUNCTIONS ========================

def _ensure_config_dir():
    """Ensure configuration directory exists"""
    config_dir = os.path.dirname(VENV_CONFIG_FILE)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(VENV_ROOT):
        os.makedirs(VENV_ROOT)

def _load_venv_config():
    """Load virtual environment configuration"""
    _ensure_config_dir()
    if os.path.exists(VENV_CONFIG_FILE):
        try:
            with open(VENV_CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"{RED}[ERROR] Failed to load venv config: {e}{RESET}")
            return {"venvs": {}, "active": None}
    return {"venvs": {}, "active": None}

def _save_venv_config(config):
    """Save virtual environment configuration"""
    _ensure_config_dir()
    try:
        with open(VENV_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"{RED}[ERROR] Failed to save venv config: {e}{RESET}")

def _get_active_venv():
    """Get currently active virtual environment"""
    config = _load_venv_config()
    return config.get("active")

def _set_active_venv(venv_name):
    """Set active virtual environment"""
    config = _load_venv_config()
    config["active"] = venv_name
    _save_venv_config(config)

def _is_windows():
    """Check if running on Windows"""
    return sys.platform.lower() in ["win32", "cygwin"]

def _get_venv_paths(venv_name):
    """Get paths for a virtual environment"""
    venv_path = os.path.join(VENV_ROOT, venv_name)
    if _is_windows():
        activate_path = os.path.join(venv_path, "Scripts", "activate.bat")
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        activate_path = os.path.join(venv_path, "bin", "activate")
        python_path = os.path.join(venv_path, "bin", "python")
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    return {
        "root": venv_path,
        "activate": activate_path,
        "python": python_path,
        "pip": pip_path
    }

def _venv_exists(venv_name):
    """Check if virtual environment exists"""
    paths = _get_venv_paths(venv_name)
    return os.path.exists(paths["python"])

# ======================== COMMANDS ========================

@command(name="venv", aliases=["ve"])
def venv_manager(*args):
    """Virtual environment manager - manage Python virtual environments"""
    
    if not args:
        venv_help()
        return
    
    subcommand = args[0].lower()
    sub_args = args[1:] if len(args) > 1 else ()
    
    commands_map = {
        "create": venv_create,
        "c": venv_create,
        "activate": venv_activate,
        "a": venv_activate,
        "deactivate": venv_deactivate,
        "d": venv_deactivate,
        "list": venv_list,
        "ls": venv_list,
        "l": venv_list,
        "delete": venv_delete,
        "rm": venv_delete,
        "info": venv_info,
        "i": venv_info,
        "install": venv_install,
        "pip": venv_pip,
        "help": venv_help,
        "h": venv_help,
    }
    
    if subcommand in commands_map:
        commands_map[subcommand](*sub_args)
    else:
        print(f"{RED}[!] Unknown subcommand: {subcommand}{RESET}")
        venv_help()

def venv_create(*args):
    """Create a new virtual environment"""
    if not args:
        print(f"{YELLOW}[?] Usage: venv create <name> [python-version]{RESET}")
        return
    
    venv_name = args[0]
    python_version = args[1] if len(args) > 1 else "3"
    
    _ensure_config_dir()
    
    if _venv_exists(venv_name):
        print(f"{YELLOW}[!] Virtual environment '{venv_name}' already exists{RESET}")
        return
    
    venv_path = _get_venv_paths(venv_name)["root"]
    
    try:
        print(f"{CYAN}[*] Creating virtual environment '{venv_name}'...{RESET}")
        
        cmd = [sys.executable, "-m", "venv", venv_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{RED}[ERROR] Failed to create venv: {result.stderr}{RESET}")
            return
        
        config = _load_venv_config()
        config["venvs"][venv_name] = {
            "path": venv_path,
            "created": str(Path(venv_path).stat().st_ctime),
            "packages": {}
        }
        _save_venv_config(config)
        
        print(f"{GREEN}[OK] Virtual environment '{venv_name}' created successfully{RESET}")
        print(f"{GRAY}    Path: {venv_path}{RESET}")
        print(f"{GRAY}    To activate: venv activate {venv_name}{RESET}")
        
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

def venv_activate(*args):
    """Activate a virtual environment"""
    if not args:
        print(f"{YELLOW}[?] Usage: venv activate <name>{RESET}")
        return
    
    venv_name = args[0]
    
    if not _venv_exists(venv_name):
        print(f"{RED}[!] Virtual environment '{venv_name}' does not exist{RESET}")
        return
    
    venv_paths = _get_venv_paths(venv_name)
    activate_cmd = venv_paths["activate"]
    
    if _is_windows():
        try:
            _set_active_venv(venv_name)
            print(f"{GREEN}[OK] Virtual environment '{venv_name}' marked as active{RESET}")
            print(f"{GRAY}    To activate in current shell, run:{RESET}")
            print(f"{YELLOW}    {activate_cmd}{RESET}")
            print(f"{GRAY}    Or open a new PowerShell window{RESET}")
        except Exception as e:
            print(f"{RED}[ERROR] {e}{RESET}")
    else:
        try:
            _set_active_venv(venv_name)
            print(f"{GREEN}[OK] Virtual environment '{venv_name}' marked as active{RESET}")
            print(f"{GRAY}    To activate, run: source {activate_cmd}{RESET}")
        except Exception as e:
            print(f"{RED}[ERROR] {e}{RESET}")

def venv_deactivate(*args):
    """Deactivate the current virtual environment"""
    active = _get_active_venv()
    if not active:
        print(f"{YELLOW}[!] No active virtual environment{RESET}")
        return
    
    try:
        _set_active_venv(None)
        print(f"{GREEN}[OK] Virtual environment '{active}' deactivated{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

def venv_list(*args):
    """List all virtual environments"""
    config = _load_venv_config()
    venvs = config.get("venvs", {})
    active = config.get("active")
    
    if not venvs:
        print(f"{YELLOW}[!] No virtual environments found{RESET}")
        return
    
    print(f"{CYAN}{BOLD}--- VIRTUAL ENVIRONMENTS ---{RESET}")
    
    width = {"name": 25, "status": 12, "path": 45}
    sep = f"{GRAY}{'-' * (width['name'] + width['status'] + width['path'] + 8)}{RESET}"
    
    header = f"{'NAME':<{width['name']}} | {'STATUS':<{width['status']}} | {'PATH':<{width['path']}}"
    print(f"{BOLD}{header}{RESET}")
    print(sep)
    
    for venv_name in sorted(venvs.keys()):
        status = f"{GREEN}[ACTIVE*]{RESET}" if venv_name == active else f"{GRAY}inactive{RESET}"
        venv_path = venvs[venv_name].get("path", "Unknown")
        path_short = venv_path if len(venv_path) <= width['path'] else "..." + venv_path[-(width['path']-3):]
        
        print(f"{CYAN}{venv_name:<{width['name']}}{RESET} | {status:<{width['status'] + 10}} | {path_short}")
    
    print(sep)

def venv_delete(*args):
    """Delete a virtual environment"""
    if not args:
        print(f"{YELLOW}[?] Usage: venv delete <name>{RESET}")
        return
    
    venv_name = args[0]
    
    if not _venv_exists(venv_name):
        print(f"{RED}[!] Virtual environment '{venv_name}' does not exist{RESET}")
        return
    
    try:
        config = _load_venv_config()
        venv_path = _get_venv_paths(venv_name)["root"]
        
        print(f"{YELLOW}[?] Delete '{venv_name}'? (yes/no): {RESET}", end="")
        confirm = input().strip().lower()
        
        if confirm not in ["yes", "y"]:
            print(f"{GRAY}Cancelled{RESET}")
            return
        
        # Remove directory
        import shutil
        shutil.rmtree(venv_path)
        
        # Update config
        if venv_name in config["venvs"]:
            del config["venvs"][venv_name]
        if config.get("active") == venv_name:
            config["active"] = None
        
        _save_venv_config(config)
        
        print(f"{GREEN}[OK] Virtual environment '{venv_name}' deleted{RESET}")
        
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

def venv_info(*args):
    """Show detailed information about a virtual environment"""
    if not args:
        active = _get_active_venv()
        if not active:
            print(f"{RED}[!] No active virtual environment and no name specified{RESET}")
            return
        venv_name = active
    else:
        venv_name = args[0]
    
    if not _venv_exists(venv_name):
        print(f"{RED}[!] Virtual environment '{venv_name}' does not exist{RESET}")
        return
    
    config = _load_venv_config()
    venv_data = config.get("venvs", {}).get(venv_name, {})
    venv_paths = _get_venv_paths(venv_name)
    
    print(f"{CYAN}{BOLD}--- VENV INFO: {venv_name} ---{RESET}")
    print(f"{GRAY}Root Path     :{RESET} {venv_paths['root']}")
    print(f"{GRAY}Python Path   :{RESET} {venv_paths['python']}")
    print(f"{GRAY}Pip Path      :{RESET} {venv_paths['pip']}")
    print(f"{GRAY}Activate Path :{RESET} {venv_paths['activate']}")
    print(f"{GRAY}Exists        :{RESET} {GREEN if os.path.exists(venv_paths['root']) else RED}{'Yes' if os.path.exists(venv_paths['root']) else 'No'}{RESET}")
    
    # Try to get installed packages
    try:
        result = subprocess.run([venv_paths["pip"], "list", "--format=json"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            print(f"{GRAY}Installed Packages: ({len(packages)}){RESET}")
            for pkg in sorted(packages, key=lambda x: x['name'].lower())[:10]:
                print(f"  {CYAN}{pkg['name']:<30}{RESET} {pkg['version']}")
            if len(packages) > 10:
                print(f"  {GRAY}... and {len(packages) - 10} more{RESET}")
    except Exception as e:
        print(f"{GRAY}Installed Packages: (unable to retrieve){RESET}")

def venv_install(*args):
    """Install packages into a virtual environment"""
    if not args:
        print(f"{YELLOW}[?] Usage: venv install <package1> [package2] ... [-e venv_name]{RESET}")
        return
    
    # Parse arguments to find venv name
    venv_name = None
    packages = []
    i = 0
    while i < len(args):
        if args[i] == "-e" and i + 1 < len(args):
            venv_name = args[i + 1]
            i += 2
        else:
            packages.append(args[i])
            i += 1
    
    if not venv_name:
        venv_name = _get_active_venv()
    
    if not venv_name:
        print(f"{RED}[!] No virtual environment specified and none active{RESET}")
        return
    
    if not _venv_exists(venv_name):
        print(f"{RED}[!] Virtual environment '{venv_name}' does not exist{RESET}")
        return
    
    if not packages:
        print(f"{RED}[!] No packages specified{RESET}")
        return
    
    try:
        venv_paths = _get_venv_paths(venv_name)
        print(f"{CYAN}[*] Installing packages into '{venv_name}'...{RESET}")
        
        cmd = [venv_paths["pip"], "install"] + packages
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{RED}[ERROR] Installation failed:{RESET}")
            print(result.stderr)
            return
        
        print(f"{GREEN}[OK] Packages installed successfully{RESET}")
        print(result.stdout)
        
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

def venv_pip(*args):
    """Run pip command in a virtual environment"""
    if not args:
        print(f"{YELLOW}[?] Usage: venv pip <pip-command> [-e venv_name]{RESET}")
        return
    
    # Parse arguments to find venv name
    venv_name = None
    pip_args = []
    i = 0
    while i < len(args):
        if args[i] == "-e" and i + 1 < len(args):
            venv_name = args[i + 1]
            i += 2
        else:
            pip_args.append(args[i])
            i += 1
    
    if not venv_name:
        venv_name = _get_active_venv()
    
    if not venv_name:
        print(f"{RED}[!] No virtual environment specified and none active{RESET}")
        return
    
    if not _venv_exists(venv_name):
        print(f"{RED}[!] Virtual environment '{venv_name}' does not exist{RESET}")
        return
    
    try:
        venv_paths = _get_venv_paths(venv_name)
        cmd = [venv_paths["pip"]] + pip_args
        
        print(f"{CYAN}[*] Running pip in '{venv_name}'...{RESET}\n")
        subprocess.run(cmd)
        
    except Exception as e:
        print(f"{RED}[ERROR] {e}{RESET}")

def venv_help(*args):
    """Display help for virtual environment commands"""
    print(f"""
{CYAN}{BOLD}--- VIRTUAL ENVIRONMENT MANAGER HELP ---{RESET}

{BOLD}SYNTAX:{RESET}
  venv <subcommand> [arguments]
  ve <subcommand> [arguments]    (short alias)

{BOLD}SUBCOMMANDS:{RESET}

  {GREEN}create{RESET} <name> [py-version]    Create a new virtual environment
    Example: venv create myenv 3.11

  {GREEN}activate{RESET} <name>               Mark a venv as active (symbolic)
    Example: venv activate myenv

  {GREEN}deactivate{RESET}                    Deactivate the current venv
    Example: venv deactivate

  {GREEN}list{RESET}                          List all virtual environments
    Aliases: ls, l
    Example: venv list

  {GREEN}info{RESET} [name]                   Show detailed venv information
    Aliases: i
    Example: venv info myenv

  {GREEN}delete{RESET} <name>                 Delete a virtual environment
    Aliases: rm
    Example: venv delete myenv

  {GREEN}install{RESET} <pkg1> [pkg2] ... [-e venv]  Install packages
    Example: venv install numpy pandas
    Example: venv install requests -e myenv

  {GREEN}pip{RESET} <pip-args> [-e venv]     Run pip command directly
    Example: venv pip list
    Example: venv pip freeze -e myenv

  {GREEN}help{RESET}                          Show this help message
    Aliases: h

{BOLD}LOCATIONS:{RESET}
  Config:    {VENV_CONFIG_FILE}
  Venvs:     {VENV_ROOT}

{BOLD}NOTES:{RESET}
  - Virtual environments are stored in ~/.polsoft/psCli/venvs/
  - Configuration is stored in ~/.polsoft/psCli/venv_config.json
  - Use activate to set the default venv for install/pip commands
  - On Windows, use the activation script: Scripts\\activate.bat

{GRAY}Version: {__version__}{RESET}
""")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        venv_manager(*sys.argv[1:])
    else:
        venv_help()
