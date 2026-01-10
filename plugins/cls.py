# Import decorator from main CLI file
from cli import command
import os

# -------------------------
# Module metadata
# -------------------------
__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__version__ = "1.0.0"
__date__ = "2026-01-10"
__group__ = "core"
__category__ = "file system"
__desc__ = "Clears the console screen" # Description for the HELP system
__all__ = ["run"]

# ANSI colors
RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[33m"

@command(name="cls", aliases=["clear", "clean", "c"])
def run(*args):
    """
    Clears the console screen.
    Supports aliases: clear, clean, c.
    """
    # If the first argument is help trigger
    if args and args[0] in ["help", "--help", "-h", "?"]:
        show_plugin_help()
        return

    # Native Windows clear command
    os.system('cls')

def show_plugin_help():
    """Internal help for the cls module."""
    print(f"\n{CYAN}CLS Plugin Help{RESET}")
    print(f"{YELLOW}Description: {RESET}{__desc__}")
    print(f"{YELLOW}Aliases:     {RESET}clear, clean, c")
    print(f"{YELLOW}Usage:       {RESET}cls")
    print(f"{CYAN}Example:     {RESET}cls\n")