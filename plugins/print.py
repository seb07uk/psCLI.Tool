import os
import re
from pathlib import Path
from datetime import datetime
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "file reader"
__group__ = "office"

# Definicja obsługiwanych rozszerzeń
SUPPORTED_EXTENSIONS = [".txt", ".json", ".py", ".log", ".md", ".csv", ".yaml", ".xml"]

def highlight_content(content, extension, search_query=None):
    """Simple syntax highlighting for supported file types and search results."""
    if extension == ".json":
        content = re.sub(r'(".*?")\s*:', f"{Color.CYAN}\\1{Color.RESET}:", content)
    elif extension == ".py":
        content = re.sub(r'(#.*)', f"{Color.GRAY}\\1{Color.RESET}", content)
        content = re.sub(r'(".*?"|\'.*?\')', f"{Color.YELLOW}\\1{Color.RESET}", content)
    elif extension in [".xml", ".yaml"]:
        content = re.sub(r'(<.*?>|[a-zA-Z0-9_-]+:)', f"{Color.CYAN}\\1{Color.RESET}", content)
    elif extension == ".md":
        content = re.sub(r'(#+ .*)', f"{Color.CYAN}\\1{Color.RESET}", content)
        content = re.sub(r'(\[.*?\]\(.*?\))', f"{Color.GREEN}\\1{Color.RESET}", content)
    elif extension == ".log":
        content = re.sub(r'(ERROR|FAIL|CRITICAL)', f"{Color.RED}\\1{Color.RESET}", content, flags=re.IGNORECASE)
        content = re.sub(r'(WARNING|INFO|DEBUG)', f"{Color.YELLOW}\\1{Color.RESET}", content, flags=re.IGNORECASE)
    elif extension == ".csv":
        content = content.replace(",", f"{Color.CYAN},{Color.RESET}").replace(";", f"{Color.CYAN};{Color.RESET}")

    if search_query:
        pattern = re.compile(re.escape(search_query), re.IGNORECASE)
        content = pattern.sub(f"{Color.LIGHT_RED}{search_query}{Color.RESET}", content)
        
    return content

@command(name="print", aliases=["cat", "type"])
def print_file(*args):
    """Reading notes / JSON preview / Displaying source code. Logs to History\\print.log"""
    
    # Katalog główny cli (nadrzędny dla folderu z pluginami)
    cli_root = Path(__file__).parent.parent 
    plugins_dir = cli_root / "plugins"

    # Wyświetlanie listy plików (Root + Plugins), jeśli brak argumentów
    if not args:
        print(f"{Color.CYAN}--- Available files in psCLI root & plugins ---{Color.RESET}")
        
        def list_files(directory, label):
            if not directory.exists(): return
            files = [f for f in directory.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
            if files:
                print(f"{Color.YELLOW}[{label}]{Color.RESET}")
                for f in files:
                    print(f"  {f.name}")

        list_files(cli_root, "Root")
        list_files(plugins_dir, "Plugins")
            
        print(f"\n{Color.GRAY}Tip: Use 'print <filename>' to open or 'print --help' for options.{Color.RESET}")
        return

    # Obsługa pomocy
    if "-h" in args or "--help" in args:
        print(f"{Color.CYAN}Usage:{Color.RESET}")
        print(f"  print <file_path> [search_query]")
        print(f"  cat <file_path> [search_query]")
        print(f"  type <file_path> [search_query]")
        print(f"\n{Color.CYAN}Description:{Color.RESET}")
        print("  Displays file content with highlighting. Searches Root and Plugins if path is relative.")
        print(f"  Logs: %userprofile%\\.polsoft\\psCLI\\History\\print.log")
        print(f"\n{Color.CYAN}Supported file types:{Color.RESET}")
        print(f"  {', '.join(SUPPORTED_EXTENSIONS)}")
        print(f"\n{Color.CYAN}Examples:{Color.RESET}")
        print("  print cli.py             # Open cli.py from psCLI root")
        print("  print print.py           # Open this plugin from plugins folder")
        print("  cat logs.log ERROR       # Search for ERROR in logs.log")
        print(f"\n{Color.GRAY}author:  Sebastian Januchowski")
        print("email:   polsoft.its@fastservice.com")
        print(f"github:  https://github.com/seb07uk{Color.RESET}")
        return
    
    filename = args[0]
    search_query = args[1] if len(args) > 1 else None
    path = Path(filename)
    
    # Logika szukania pliku w katalogach systemowych CLI
    if not path.exists():
        if (cli_root / filename).exists():
            path = cli_root / filename
        elif (plugins_dir / filename).exists():
            path = plugins_dir / filename

    log_dir = Path.home() / ".polsoft" / "psCLI" / "History"
    log_file = log_dir / "print.log"
    
    if not path.exists():
        print(f"{Color.RED}[ERROR] File '{filename}' not found in Root or Plugins.{Color.RESET}")
        return

    try:
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        extension = path.suffix.lower()
        status = "Completed"
        start_index = 0
        
        if search_query:
            matches = [i for i, line in enumerate(lines) if search_query.lower() in line.lower()]
            if matches:
                start_index = matches[0]
                print(f"{Color.YELLOW}Found {len(matches)} matches. Jumping to line {start_index + 1}.{Color.RESET}")
            else:
                print(f"{Color.RED}No matches found for '{search_query}'.{Color.RESET}")

        print(f"{Color.GRAY}--- Content: {path.absolute()} ({len(lines)} lines) ---{Color.RESET}")
        
        page_size = 20
        for i in range(start_index, len(lines), page_size):
            chunk = "\n".join(lines[i:i + page_size])
            print(highlight_content(chunk, extension, search_query))
            
            if i + page_size < len(lines):
                user_input = input(f"{Color.YELLOW}--- Enter for more or 'q' to quit ---{Color.RESET}").lower()
                if user_input == 'q':
                    status = "Interrupted"
                    break

        print(f"{Color.GRAY}--- End of output ---{Color.RESET}")

        # Logging
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            search_info = f" | Search: '{search_query}'" if search_query else ""
            f.write(f"[{timestamp}] Accessed: {path.absolute()} | Status: {status}{search_info}\n")
            f.write(f"{'-'*20}\n{content}\n{'='*40}\n")

    except Exception as e:
        print(f"{Color.RED}Could not read file: {e}{Color.RESET}")