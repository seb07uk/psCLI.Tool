import os
from datetime import datetime
from cli import command, Color

__author__ = "Gemini"
__category__ = "system"
__group__ = "core"
__desc__ = "Saves file list with detailed folder summary to %USERPROFILE%/.polsoft/psCli/Save"

def get_size_format(b, factor=1024, suffix="B"):
    """Scales bytes to the appropriate unit (KB, MB, GB)."""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.2f} {unit}{suffix}"
        b /= factor
    return f"{b:.2f} Y{suffix}"

@command(name="save", aliases=["/s"])
def save_command(*args):
    """Generates a file list with header and detailed summary. Use -h for help."""
    
    # --- EXTENDED HELP HANDLING ---
    if args and args[0] in ["-h", "--help"]:
        print(f"\n{Color.CYAN}{Color.BOLD}COMMAND: save{Color.RESET}")
        print(f"{Color.GRAY}Generates a snapshot of the current directory as a script-like text file.{Color.RESET}")
        
        print(f"\n{Color.YELLOW}USAGE:{Color.RESET}")
        print(f"  save            # Creates a report in %USERPROFILE%/.polsoft/psCli/Save")
        print(f"  save -h         # Displays this help message")
        
        print(f"\n{Color.YELLOW}OUTPUT FORMAT EXAMPLE:{Color.RESET}")
        print(f"  print notes.txt     # Reading notes")
        print(f"  cat metadata.json   # JSON metadata preview")
        print(f"  type script.py      # Displaying source code")
        
        print(f"\n{Color.YELLOW}LOCATION:{Color.RESET}")
        print(f"  Files are automatically named with the current date and time.")
        print(f"  Path: {Color.GRAY}~/.polsoft/psCli/Save/save_YYYY-MM-DD_HH-MM-SS.txt{Color.RESET}\n")
        return

    # --- PATH CONFIGURATION ---
    current_dir = os.getcwd()
    folder_name = os.path.basename(current_dir) or current_dir
    user_profile = os.environ.get('USERPROFILE') or os.path.expanduser('~')
    target_dir = os.path.join(user_profile, '.polsoft', 'psCli', 'Save')
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    now = datetime.now()
    file_date = now.strftime("%Y-%m-%d_%H-%M-%S")
    full_path = os.path.join(target_dir, f"save_{file_date}.txt")

    # --- HEADER ---
    output_lines = [
        f"# LOCATION: {current_dir}",
        f"# DATE:     {now.strftime('%Y-%m-%d')}",
        f"# TIME:     {now.strftime('%H:%M:%S')}",
        f"#" + "-" * 50,
        ""
    ]
    
    try:
        all_items = os.listdir('.')
        files = [f for f in all_items if os.path.isfile(f)]
        dirs = [d for d in all_items if os.path.isdir(d)]
        
        total_size = 0
        for file in files:
            file_size = os.path.getsize(file)
            total_size += file_size
            
            ext = os.path.splitext(file)[1].lower()
            if ext == '.txt':
                cmd, desc = "print", "Reading notes"
            elif ext == '.json':
                cmd, desc = "cat", "JSON metadata preview"
            elif ext == '.py':
                cmd, desc = "type", "Displaying source code"
            else:
                cmd, desc = "cat", "File content"
            
            output_lines.append(f"{cmd} {file} # {desc}")

        # --- EXTENDED SUMMARY ---
        output_lines.extend([
            "",
            "#" + "-" * 50,
            f"# SUMMARY FOR:   {folder_name}",
            f"# Full path:     {current_dir}",
            f"# Total files:   {len(files)}",
            f"# Total folders: {len(dirs)}",
            f"# Total size:    {get_size_format(total_size)}",
            "#" + "-" * 50
        ])

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
            
        print(f"{Color.GREEN}[SUCCESS]{Color.RESET} Report saved: {Color.GRAY}{full_path}{Color.RESET}")
        
    except Exception as e:
        print(f"{Color.RED}[ERROR]{Color.RESET} {e}")

if __name__ == "__main__":
    save_command()