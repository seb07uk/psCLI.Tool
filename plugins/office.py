import os
import json
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "office"
__group__ = "menu"
__desc__ = "Office Suite - manages documents and metadata previews"

@command(name="office", aliases=["docs", "work"])
def office_viewer(*args):
    """Main office module of the TERMINAL CLI system."""
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metadata_dir = os.path.join(root_dir, "metadata")
    notes_file = "notes.txt"

    print(f"{Color.CYAN}{Color.BOLD}--- OFFICE & DOCUMENTS ---{Color.RESET}")

    # 1. Example of reading notes (following your alignment scheme)
    if os.path.exists(notes_file):
        print(f"{Color.GREEN}print {notes_file:<14}{Color.RESET} {Color.GRAY}# Reading notes{Color.RESET}")
    else:
        print(f"{Color.RED}{notes_file:<20}{Color.RESET} {Color.GRAY}# File not found{Color.RESET}")

    # 2. JSON Metadata Preview
    if os.path.exists(metadata_dir):
        json_files = [f for f in os.listdir(metadata_dir) if f.endswith('.json')]
        for j_file in sorted(json_files):
            # Align: cat metadata/echo.json # JSON metadata preview
            display_path = f"metadata/{j_file}"
            print(f"{Color.GREEN}cat {display_path:<16}{Color.RESET} {Color.GRAY}# JSON metadata preview{Color.RESET}")
    else:
        print(f"{Color.YELLOW}metadata/ folder missing{Color.RESET} {Color.GRAY}# No JSON files found{Color.RESET}")

    # 3. Listing other office plugin files
    plugins_dir = os.path.dirname(__file__)
    office_plugins = [f for f in os.listdir(plugins_dir) if f.endswith('.py') and "office" in f.lower()]
    
    for plugin in sorted(office_plugins):
        if plugin != "office.py":
            print(f"{Color.GREEN}{plugin:<20}{Color.RESET} {Color.GRAY}# Office tool plugin{Color.RESET}")

    print(f"{Color.CYAN}{'-' * 45}{Color.RESET}")

if __name__ == "__main__":
    office_viewer()