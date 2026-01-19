import os
from cli import command, Color

__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__category__ = "file system"
__group__ = "core"
__desc__ = "Directory tree structure visualizer with colored output"


# Color map for file extensions (Linux style)
FILE_COLORS = {
    # Archives & Compressed
    '.zip': Color.RED, '.rar': Color.RED, '.7z': Color.RED, '.tar': Color.RED, '.gz': Color.RED,
    # Executables & Scripts
    '.exe': Color.GREEN, '.bat': Color.GREEN, '.cmd': Color.GREEN, '.py': Color.GREEN, 
    '.ps1': Color.GREEN, '.sh': Color.GREEN, '.vbs': Color.GREEN,
    # Documents & Text
    '.pdf': Color.CYAN, '.doc': Color.CYAN, '.docx': Color.CYAN, '.txt': Color.CYAN, 
    '.log': Color.CYAN, '.md': Color.CYAN, '.json': Color.CYAN,
    # Media & Graphics
    '.jpg': Color.YELLOW, '.png': Color.YELLOW, '.gif': Color.YELLOW, '.bmp': Color.YELLOW,
    '.mp4': Color.YELLOW, '.avi': Color.YELLOW, '.wav': Color.YELLOW, '.mp3': Color.YELLOW,
    # Config & Source
    '.ini': Color.GRAY, '.cfg': Color.GRAY, '.conf': Color.GRAY, '.xml': Color.GRAY,
    '.yaml': Color.GRAY, '.yml': Color.GRAY, '.toml': Color.GRAY,
}


def get_file_color(filename):
    """Returns color based on file extension."""
    _, ext = os.path.splitext(filename.lower())
    return FILE_COLORS.get(ext, Color.WHITE)


def draw_tree(directory, prefix="", max_depth=None, current_depth=0, show_hidden=False):
    """Renders directory tree structure with visual connectors and colored extensions."""
    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        return

    # Filter hidden items unless explicitly shown
    if not show_hidden:
        items = [item for item in items if not item.startswith('.')]

    for i, item in enumerate(items):
        path = os.path.join(directory, item)
        is_last = (i == len(items) - 1)
        
        # Branch symbols
        connector = "└── " if is_last else "├── "
        
        if os.path.isdir(path):
            print(f"{prefix}{connector}{Color.BLUE}{item}/{Color.RESET}")
            # Extend prefix for subdirectories
            extension = "    " if is_last else "│   "
            if max_depth is None or current_depth < max_depth:
                draw_tree(path, prefix + extension, max_depth, current_depth + 1, show_hidden)
        else:
            color = get_file_color(item)
            print(f"{prefix}{connector}{color}{item}{Color.RESET}")


def show_help():
    """Display help information for tree command."""
    print(f"\n{Color.BOLD}{Color.CYAN}{'=' * 70}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}TREE - Professional Directory Structure Visualizer{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}{'=' * 70}{Color.RESET}\n")
    
    print(f"{Color.BOLD}{Color.GREEN}DESCRIPTION:{Color.RESET}")
    print(f"  Visualize your directory structure in an elegant tree format with\n"
          f"  intuitive color-coded file types for quick identification.\n")
    
    print(f"{Color.BOLD}{Color.GREEN}USAGE:{Color.RESET}")
    print(f"  {Color.YELLOW}tree{Color.RESET} [path] [options]\n")
    
    print(f"{Color.BOLD}{Color.GREEN}ARGUMENTS:{Color.RESET}")
    print(f"  {Color.CYAN}path{Color.RESET:<12} Target directory to visualize (default: current directory)\n")
    
    print(f"{Color.BOLD}{Color.GREEN}OPTIONS:{Color.RESET}")
    print(f"  {Color.CYAN}-h, --help{Color.RESET:<6} Show this comprehensive help message")
    print(f"  {Color.CYAN}-a{Color.RESET:<12} Display hidden files (files starting with '.')")
    print(f"  {Color.CYAN}-d N{Color.RESET:<12} Limit recursion depth to N levels (useful for large trees)\n")
    
    print(f"{Color.BOLD}{Color.GREEN}COLOR SCHEME:{Color.RESET}")
    print(f"  {Color.BLUE}[Folder]{Color.RESET:<10} Directory paths")
    print(f"  {Color.RED}[Archive]{Color.RESET:<9} Compressed files (.zip, .rar, .7z, etc.)")
    print(f"  {Color.GREEN}[Executable]{Color.RESET:<7} Scripts & binaries (.exe, .py, .ps1, etc.)")
    print(f"  {Color.CYAN}[Document]{Color.RESET:<8} Text & data files (.pdf, .docx, .txt, etc.)")
    print(f"  {Color.YELLOW}[Media]{Color.RESET:<11} Images & videos (.jpg, .png, .mp4, etc.)")
    print(f"  {Color.GRAY}[Config]{Color.RESET:<11} Configuration files (.json, .yaml, .ini, etc.)\n")
    
    print(f"{Color.BOLD}{Color.GREEN}EXAMPLES:{Color.RESET}")
    print(f"  {Color.CYAN}tree{Color.RESET}")
    print(f"    → Display the current directory structure\n")
    
    print(f"  {Color.CYAN}tree C:\\Users\\Documents{Color.RESET}")
    print(f"    → Explore a specific directory path\n")
    
    print(f"  {Color.CYAN}tree . -d 2{Color.RESET}")
    print(f"    → Show tree with a maximum depth of 2 levels\n")
    
    print(f"  {Color.CYAN}tree -a{Color.RESET}")
    print(f"    → Display all files, including hidden ones\n")
    
    print(f"  {Color.CYAN}tree C:\\Projects -d 3 -a{Color.RESET}")
    print(f"    → Advanced: combine multiple options for full visibility\n")
    
    print(f"{Color.BOLD}{Color.GREEN}TIPS & TRICKS:{Color.RESET}")
    print(f"  • Use {Color.CYAN}-d{Color.RESET} when exploring large directory trees (faster rendering)")
    print(f"  • Color coding helps quickly identify file types without reading extensions")
    print(f"  • Combine {Color.CYAN}-a{Color.RESET} flag to troubleshoot hidden configuration files\n")
    
    print(f"{Color.BOLD}{Color.CYAN}{'=' * 70}{Color.RESET}\n")


@command(name="tree", aliases=["ls"])
def run(*args):
    """
    Display directory structure as a tree with colored output.
    Supports custom paths, depth limiting, and hidden file visibility.
    """
    # Parse arguments
    target_path = os.getcwd()
    max_depth = None
    show_hidden = False
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["-h", "--help", "help"]:
            show_help()
            return
        elif arg == "-a":
            show_hidden = True
        elif arg == "-d":
            if i + 1 < len(args):
                try:
                    max_depth = int(args[i + 1])
                    i += 1
                except ValueError:
                    print(f"{Color.RED}[ERROR] Depth must be an integer.{Color.RESET}")
                    return
        elif not arg.startswith("-"):
            target_path = os.path.expandvars(arg)
        
        i += 1
    
    # Validate path
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        print(f"{Color.RED}[!] Error: Path '{target_path}' does not exist.{Color.RESET}")
        return
    
    if not os.path.isdir(target_path):
        print(f"{Color.RED}[!] Error: '{target_path}' is not a directory.{Color.RESET}")
        return
    
    # Display tree
    print(f"{Color.YELLOW}Directory structure for: {target_path}{Color.RESET}\n")
    print(f"{Color.BOLD}{os.path.basename(target_path)}/{Color.RESET}")
    draw_tree(target_path, "", max_depth, 0, show_hidden)