import os
import json
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "core"
__group__ = "menu"
__desc__ = "Core Module Viewer - displays essential system plugins"

@command(name="core", aliases=["sys", "base"])
def core_viewer(*args):
    """Main function displaying core group files."""
    
    # Path to settings according to your configuration
    settings_file = os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings\terminal.json")
    
    # Get the path to the plugins folder relative to core.py
    plugins_dir = os.path.dirname(__file__)

    if not os.path.exists(plugins_dir):
        print(f"{Color.RED}[ERROR] Directory '{plugins_dir}' does not exist.{Color.RESET}")
        return

    print(f"{Color.CYAN}{Color.BOLD}--- CORE FILE LIST ---{Color.RESET}")

    # Filter .py files that contain the phrase 'core' in their name
    files = [f for f in os.listdir(plugins_dir) if f.endswith('.py') and "core" in f.lower()]
    
    # Add cls.py as a key core element if it exists
    if os.path.exists(os.path.join(plugins_dir, "cls.py")):
        if "cls.py" not in files:
            files.append("cls.py")

    # Sorting and displaying according to your alignment scheme: file # description
    for file in sorted(files):
        if file == "core.py":
            print(f"{Color.GREEN}{file:<20}{Color.RESET} {Color.GRAY}# Main core viewer module{Color.RESET}")
        elif file == "cls.py":
            # Alignment as per your request: type plugins/cls.py # Displaying source code
            print(f"{Color.GREEN}type plugins/{file:<12}{Color.RESET} {Color.GRAY}# Displaying source code{Color.RESET}")
        else:
            print(f"{Color.GREEN}{file:<20}{Color.RESET} {Color.GRAY}# Core system plugin{Color.RESET}")

    print(f"{Color.CYAN}{'-' * 40}{Color.RESET}")

if __name__ == "__main__":
    core_viewer()