import os
import shutil
from datetime import datetime
from cli import command, Color

__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__category__ = "file system"
__group__ = "core"
__desc__ = "Explorer with dynamic sorting and file type coloring"

# Color map for extensions (Linux style)
FILE_COLORS = {
    '.zip': Color.RED, '.rar': Color.RED, '.7z': Color.RED, '.tar': Color.RED, '.gz': Color.RED,
    '.exe': Color.GREEN, '.bat': Color.GREEN, '.cmd': Color.GREEN, '.py': Color.GREEN, '.ps1': Color.GREEN,
    '.pdf': Color.CYAN, '.doc': Color.CYAN, '.docx': Color.CYAN, '.txt': Color.CYAN, '.log': Color.CYAN,
    '.jpg': Color.YELLOW, '.png': Color.YELLOW, '.gif': Color.YELLOW, '.bmp': Color.YELLOW,
}

def format_size(size):
    """Converts bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:6.1f} {unit}"
        size /= 1024
    return f"{size:6.1f} TB"

def get_file_color(filename):
    """Returns color based on file extension."""
    _, ext = os.path.splitext(filename.lower())
    return FILE_COLORS.get(ext, Color.RESET)

def show_help():
    """Displays detailed help for the dir module."""
    print(f"\n{Color.BOLD}{Color.CYAN}DIR MODULE HELP - Advanced Directory Explorer{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 65}{Color.RESET}")
    
    print(f"{Color.BOLD}USAGE:{Color.RESET}")
    print(f"  {Color.GREEN}dir <path> [option]{Color.RESET}")
    
    print(f"\n{Color.BOLD}SORTING OPTIONS:{Color.RESET}")
    print(f"  {Color.YELLOW}-t{Color.RESET}  Sort by {Color.BOLD}Type{Color.RESET} (Extension) - [Default]")
    print(f"  {Color.YELLOW}-n{Color.RESET}  Sort by {Color.BOLD}Name{Color.RESET} (Alphabetical)")
    print(f"  {Color.YELLOW}-s{Color.RESET}  Sort by {Color.BOLD}Size{Color.RESET} (Largest first)")
    print(f"  {Color.YELLOW}-d{Color.RESET}  Sort by {Color.BOLD}Date{Color.RESET} (Newest first)")
    
    print(f"\n{Color.BOLD}COLOR SCHEME (Linux-style):{Color.RESET}")
    print(f"  {Color.CYAN}<DIR>{Color.RESET}          Directory indicator")
    print(f"  {Color.YELLOW}Size{Color.RESET}           File size in yellow")
    print(f"  {Color.GREEN}Scripts{Color.RESET}        Executables (.exe, .py, .bat)")
    print(f"  {Color.RED}Archives{Color.RESET}       Packages (.zip, .rar, .7z)")
    print(f"  {Color.CYAN}Documents{Color.RESET}      Text files (.pdf, .txt, .log)")
    
    print(f"\n{Color.BOLD}EXAMPLES:{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}dir -s             {Color.GRAY}# Show largest files here{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}dir %TEMP% -d      {Color.GRAY}# Newest files in Temp folder{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}dir .. -n          {Color.GRAY}# Alphabetical list of parent folder{Color.RESET}")
    print(f"{Color.GRAY}{'=' * 65}{Color.RESET}\n")

@command(name="dir", aliases=["ls", "list"])
def run(*args):
    """Main function to list directory contents."""
    
    # Help handler
    if args and args[0] in ["-h", "--help", "help"]:
        show_help()
        return

    # Initialize default values
    path = "."
    sort_mode = "-t"  # Default by type
    
    # Argument parsing
    for arg in args:
        if arg in ["-n", "-s", "-t", "-d"]:
            sort_mode = arg
        elif not arg.startswith("-"):
            path = arg

    # Expand environment variables and get absolute path
    path = os.path.expandvars(path)
    if not os.path.exists(path):
        print(f"{Color.RED}[!] Error: Path '{path}' does not exist.{Color.RESET}")
        return

    try:
        items = os.listdir(path)
        item_data = []

        # Fetch stats for each item
        for item in items:
            f_path = os.path.join(path, item)
            try:
                stat = os.stat(f_path)
                item_data.append({
                    'name': item,
                    'is_dir': os.path.isdir(f_path),
                    'ext': os.path.splitext(item)[1].lower(),
                    'size': stat.st_size,
                    'mtime': stat.st_mtime
                })
            except:
                continue

        # Sorting logic (always directories on top)
        if sort_mode == "-s":   # Size
            item_data.sort(key=lambda x: (not x['is_dir'], -x['size']))
        elif sort_mode == "-d": # Date
            item_data.sort(key=lambda x: (not x['is_dir'], -x['mtime']))
        elif sort_mode == "-n": # Name
            item_data.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        else:                   # Type (default)
            item_data.sort(key=lambda x: (not x['is_dir'], x['ext'], x['name'].lower()))

        # Header
        print(f"\n{Color.CYAN}{Color.BOLD}Directory listing: {os.path.abspath(path)}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 75}{Color.RESET}")
        print(f"{Color.BOLD}{'Mode':<10} {'Last Write':<20} {'Size':<12} {'Name'}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 75}{Color.RESET}")

        dir_count = 0
        file_count = 0
        total_size = 0

        # Display formatted data
        for info in item_data:
            mtime_str = datetime.fromtimestamp(info['mtime']).strftime('%Y-%m-%d  %H:%M')
            
            if info['is_dir']:
                mode = "d-----"
                size_col = f"{Color.CYAN}<DIR>{Color.RESET}"
                name_col = f"{Color.BOLD}{Color.YELLOW}{info['name']}/{Color.RESET}"
                dir_count += 1
            else:
                mode = "-a----"
                size_col = f"{Color.YELLOW}{format_size(info['size']):>12}{Color.RESET}"
                f_color = get_file_color(info['name'])
                name_col = f"{f_color}{info['name']}{Color.RESET}"
                file_count += 1
                total_size += info['size']

            print(f"{Color.GRAY}{mode:<10}{Color.RESET} {mtime_str:<20} {size_col} {name_col}")

        # Footer with statistics
        print(f"{Color.GRAY}{'-' * 75}{Color.RESET}")
        print(f"  Total: {Color.CYAN}{dir_count} Folders{Color.RESET}, {Color.CYAN}{file_count} Files{Color.RESET} ({format_size(total_size).strip()})")
        
        # Free disk space
        _, _, free = shutil.disk_usage(os.path.abspath(path))
        print(f"  Free Space: {Color.GRAY}{format_size(free).strip()}{Color.RESET}\n")

    except Exception as e:
        print(f"{Color.RED}[!] Access Denied: {e}{Color.RESET}")