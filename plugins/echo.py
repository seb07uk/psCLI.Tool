# Import the decorator from the main file (cli.py)
from cli import command

# -------------------------
# Module metadata (PEP 8/257 style)
# -------------------------
__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__version__ = "1.1.0"
__date__ = "2026-01-09"
__license__ = "MIT"
__group__ = "core"
__category__ = "output"
__desc__ = "Displays the provided text in green"  # Description for the HELP system
__all__ = ["run", "echo_text"]

# ANSI colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

# -------------------------
# Main Command
# -------------------------

@command(name="echo", aliases=["say", "repeat", "e"])
def run(*args):
    """
    Displays the provided text in green.
    Supports aliases: say, print, repeat, e.
    """
    if not args:
        print(f"{YELLOW}Usage: echo <text>{RESET}")
        return

    # If the first argument is "help" (e.g., 'echo help')
    if args[0] in ["help", "--help", "-h", "?"]:
        show_plugin_help()
        return

    text = " ".join(args)
    print(f"{GREEN}{text}{RESET}")

def show_plugin_help():
    """Internal help for the echo module."""
    print(f"\n{CYAN}Echo Plugin Help{RESET}")
    print(f"{YELLOW}Description: {RESET}{__desc__}")
    print(f"{YELLOW}Aliases:     {RESET}say, print, repeat, e")
    # Added Usage section
    print(f"{YELLOW}Usage:       {RESET}echo <text>")
    print(f"{CYAN}Example:     {RESET}echo Hello world\n")

def echo_text(text: str) -> str:
    """Returns the text unchanged (helper)."""
    return text