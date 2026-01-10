import os
from cli import command, Color

__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__category__ = "file system"
__group__ = "core"
__desc__ = "Changes the current working directory (with history support)"

# Global variable to store previous path (support for 'cd -')
_prev_path = os.getcwd()

@command(name="cd", aliases=["chdir", "jump"])
def run(*args):
    """
    Changes the current working directory.
    Supports: cd .., cd ~, cd -, cd %VAR%
    """
    global _prev_path
    
    # 1. Help handler
    if args and args[0] in ["-h", "--help", "help"]:
        show_help()
        return

    # 2. Set target (default to home directory)
    target = args[0] if args else "~"
    current_path = os.getcwd()

    # 3. Handle special shortcuts
    if target == "~":
        target = os.path.expanduser("~")
    elif target == "-":
        target = _prev_path
        print(f"{Color.GRAY}{target}{Color.RESET}")
    
    # Expand environment variables
    target = os.path.expandvars(target)

    # 4. Attempt to change directory
    try:
        new_path = os.path.abspath(target)
        
        if not os.path.exists(new_path):
            print(f"{Color.RED}[!] Error: System cannot find the path specified: '{target}'{Color.RESET}")
            return

        if not os.path.isdir(new_path):
            print(f"{Color.RED}[!] Error: '{target}' is not a directory.{Color.RESET}")
            return

        os.chdir(new_path)
        _prev_path = current_path

    except PermissionError:
        print(f"{Color.RED}[!] Access Denied: Insufficient permissions.{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[!] Error: {e}{Color.RESET}")

def show_help():
    """Displays help for the cd command with usage examples."""
    print(f"\n{Color.BOLD}{Color.CYAN}CD MODULE HELP:{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 65}{Color.RESET}")
    
    print(f"{Color.BOLD}USAGE:{Color.RESET}")
    print(f"  {Color.GREEN}cd <path>{Color.RESET}")
    
    print(f"\n{Color.BOLD}SHORTCUTS:{Color.RESET}")
    print(f"  {Color.YELLOW}..{Color.RESET}         Go up one level")
    print(f"  {Color.YELLOW}~{Color.RESET}          Go to user home directory")
    print(f"  {Color.YELLOW}-{Color.RESET}          Return to previous location")
    
    print(f"\n{Color.BOLD}EXAMPLES:{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}cd plugins         {Color.GRAY}# Enter the plugins folder{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}cd ..              {Color.GRAY}# Go back to root{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}cd %APPDATA%       {Color.GRAY}# Jump to AppData folder{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}cd -               {Color.GRAY}# Toggle between two folders{Color.RESET}")
    
    print(f"\n{Color.YELLOW}Aliases:{Color.RESET} chdir, jump")
    print(f"{Color.GRAY}{'=' * 65}{Color.RESET}\n")