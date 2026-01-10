import os
import shutil
from collections import Counter
from datetime import datetime
from cli import command, Color

__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__category__ = "file system"
__group__ = "core"
__desc__ = "Professional Directory Auditor & Path Telemetry Tool"

# Standardized Linux LS_COLORS mapping for professional visualization
LINUX_COLORS = {
    # Executables & Scripts (High-intensity Green)
    '.exe': Color.GREEN, '.py': Color.GREEN, '.bat': Color.GREEN, '.sh': Color.GREEN, '.cmd': Color.GREEN,
    # Archives & Compressed Volumes (Red)
    '.zip': Color.RED, '.tar': Color.RED, '.gz': Color.RED, '.rar': Color.RED, '.7z': Color.RED,
    # Media & Graphics (Magenta/Purple)
    '.jpg': '\033[95m', '.png': '\033[95m', '.gif': '\033[95m', '.mp4': '\033[95m', '.wav': '\033[95m',
    # Formatted Documents (Cyan/White)
    '.pdf': Color.CYAN, '.docx': Color.CYAN, '.txt': Color.WHITE, '.log': Color.GRAY,
}

def format_size(size):
    """Calculates human-readable storage units."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024: return f"{size:6.1f} {unit}"
        size /= 1024
    return f"{size:6.1f} TB"

@command(name="pwd", aliases=["path", "where"])
def run(*args):
    """
    Executes a high-level directory introspection and telemetry report.
    Supports targeting specific paths as arguments for remote auditing.
    """
    # 1. Technical Documentation Handler
    if args and args[0] in ["-h", "--help", "help"]:
        show_help()
        return

    # 2. Target Path Resolution (Supports argument or defaults to CWD)
    target = args[0] if args else os.getcwd()
    target_path = os.path.abspath(os.path.expandvars(target))
    
    # Validation
    if not os.path.exists(target_path):
        print(f"{Color.RED}[!] Analysis Error: Target path '{target}' not found.{Color.RESET}")
        return
    if not os.path.isdir(target_path):
        print(f"{Color.RED}[!] Analysis Error: Target '{target}' is not a directory.{Color.RESET}")
        return

    try:
        items = os.listdir(target_path)
        dir_count, file_count, total_size = 0, 0, 0
        ext_counter = Counter()

        for item in items:
            full_path = os.path.join(target_path, item)
            try:
                stat = os.stat(full_path)
                if os.path.isdir(full_path):
                    dir_count += 1
                else:
                    file_count += 1
                    total_size += stat.st_size
                    _, ext = os.path.splitext(item.lower())
                    ext_counter[ext if ext else "[no ext]"] += 1
            except (PermissionError, OSError):
                continue

        # --- TELEMETRY HEADER ---
        header_label = "Audit Target Directory:" if args else "Current Working Directory:"
        print(f"\n{Color.BOLD}{header_label}{Color.RESET}")
        print(f"{Color.CYAN}{target_path}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 82}{Color.RESET}")
        
        # --- TYPE DISTRIBUTION MATRIX (4-Columns) ---
        if file_count > 0:
            print(f"{Color.BOLD}FILE TYPES DISTRIBUTION MATRIX:{Color.RESET}")
            sorted_types = sorted(ext_counter.items())
            for i in range(0, len(sorted_types), 4):
                chunk = sorted_types[i:i + 4]
                line = ""
                for ext, count in chunk:
                    color = LINUX_COLORS.get(ext, Color.WHITE) if ext != "[no ext]" else Color.GRAY
                    line += f"{color}{ext:<10}{Color.RESET}: {Color.YELLOW}{count:<4}{Color.RESET} | "
                print(line.rstrip(" | "))
            print(f"{Color.GRAY}{'-' * 82}{Color.RESET}")

        # --- STORAGE & TEMPORAL SUMMARY ---
        last_mod = datetime.fromtimestamp(os.path.getmtime(target_path)).strftime('%Y-%m-%d %H:%M:%S')
        _, _, free = shutil.disk_usage(target_path)

        print(f"{Color.BOLD}DIRECTORY ANALYTICS SUMMARY:{Color.RESET}")
        print(f"  Total Volume : {Color.YELLOW}{format_size(total_size).strip():<15}{Color.RESET} |  Folders : {Color.CYAN}{dir_count}{Color.RESET}")
        print(f"  Entry Count  : {Color.YELLOW}{file_count:<15}{Color.RESET} |  Disk Free : {Color.GRAY}{format_size(free).strip()}{Color.RESET}")
        print(f"  Modified At  : {Color.WHITE}{last_mod}{Color.RESET}")
        print(f"{Color.GRAY}{'-' * 82}{Color.RESET}\n")

    except Exception as e:
        print(f"\n{Color.RED}[RUNTIME ERROR] Analysis failed: {e}{Color.RESET}\n")

def show_help():
    """Displays professional technical documentation for the PWD module."""
    print(f"\n{Color.BOLD}{Color.CYAN}MODULE: Path & Directory Analytics (PWD){Color.RESET}")
    print(f"{Color.GRAY}{'=' * 82}{Color.RESET}")
    
    print(f"{Color.BOLD}OVERVIEW:{Color.RESET}")
    print(f"  The PWD module is a core filesystem utility designed for high-level directory")
    print(f"  introspection. It provides real-time telemetry of the Current Working Directory")
    print(f"  (CWD) or target paths, offering deep insights into file distribution.")
    
    print(f"\n{Color.BOLD}TECHNICAL CAPABILITIES:{Color.RESET}")
    print(f"  * {Color.CYAN}Path Resolution{Color.RESET}  : Displays absolute, system-agnostic path auditing.")
    print(f"  * {Color.CYAN}Targeted Audits{Color.RESET}  : Analyze remote folders without changing CWD.")
    print(f"  * {Color.CYAN}Type Distribution{Color.RESET}: Generates a 4-column matrix using Linux LS_COLORS.")
    print(f"  * {Color.CYAN}Storage Telemetry{Color.RESET}: Calculates aggregate volume and disk availability.")
    
    print(f"\n{Color.BOLD}DATA VISUALIZATION (LS_COLORS):{Color.RESET}")
    print(f"  {Color.GREEN}[EXEC]{Color.RESET} Scripts/Binaries  |  {Color.RED}[ARCH]{Color.RESET} Compressed Volumes")
    print(f"  \033[95m[MEDA]\033[0m Media/Graphics    |  {Color.CYAN}[DOCS]{Color.RESET} Formatted Documents")
    
    print(f"\n{Color.BOLD}USAGE SYNTAX:{Color.RESET}")
    print(f"  {Color.GREEN}pwd{Color.RESET} [path/option]      (Available aliases: {Color.YELLOW}path, where{Color.RESET})")
    
    print(f"\n{Color.BOLD}EXAMPLES:{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}pwd                  {Color.GRAY}# Execute full directory audit of CWD{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}pwd plugins          {Color.GRAY}# Perform audit on 'plugins' folder{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}where %TEMP%         {Color.GRAY}# Inspect temporary system folder{Color.RESET}")
    print(f"  {Color.GRAY}> {Color.RESET}path help            {Color.GRAY}# Access this technical documentation{Color.RESET}")
    
    print(f"{Color.GRAY}{'=' * 82}{Color.RESET}\n")