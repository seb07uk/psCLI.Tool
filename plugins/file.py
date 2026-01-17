import os
import shutil
import platform
import subprocess
from datetime import datetime
from pathlib import Path
from cli import command

# --- METADATA (Read by cli.py dispatcher) ---
__author__ = "Sebastian Januchowski"
__category__ = "file manager"
__group__ = "system"
__desc__ = "CMD Cli File Manager: Full suite with history and quick links"

# --- COLOR AND FORMATTING CONFIGURATION ---
G = "\033[92m"      # Green (Success)
R = "\033[91m"      # Red (Error)
Y = "\033[93m"      # Yellow (Warning/Info)
B = "\033[94m"      # Blue (Frames)
BOLD = "\033[1m"    # Bold
RESET = "\033[0m"   # Reset formatting

class FileManager:
    def __init__(self):
        self.msg = ""
        self.save_path = Path.home() / ".polsoft" / "psCLI" / "FileList"
        self.save_path.mkdir(parents=True, exist_ok=True)
        
        if platform.system() == "Windows":
            os.system("title CMD File Manager Cli")
            os.system("mode con: cols=105 lines=50")

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def get_dir_content(self):
        try:
            items = sorted(os.listdir('.'))
            dirs = [d for d in items if os.path.isdir(d)]
            files = [f for f in items if os.path.isfile(f)]
            return dirs, files
        except Exception:
            return [], []

    def draw_menu(self):
        self.clear_screen()
        curr_dir = os.getcwd()
        dirs, files = self.get_dir_content()

        print(f"\n {Y}DIRECTORY CONTENT:{RESET}  {B}[{curr_dir}]{RESET}")
        print(f"{B} ┌" + "─" * 94 + f"┐{RESET}")
        
        for d in dirs:
            display_name = (d[:85] + '...') if len(d) > 85 else d
            padding = 94 - (2 + 5 + 2 + len(display_name))
            print(f"{B} │{RESET}  {G}[DIR]{RESET}  {display_name}" + " " * padding + f"{B}│{RESET}")
        
        if dirs and files:
            print(f"{B} ├" + "─" * 94 + f"┤{RESET}")
        
        for f in files:
            display_name = (f[:85] + '...') if len(f) > 85 else f
            padding = 94 - (10 + len(display_name))
            print(f"{B} │{RESET}          {display_name}" + " " * padding + f"{B}│{RESET}")
            
        print(f"{B} └" + "─" * 94 + f"┘{RESET}")

        header_text = "CMD File Manager Cli"
        margin = (95 - len(header_text)) // 2
        header_line = " " * margin + header_text + " " * (95 - margin - len(header_text))

        print(f"\n{B}╔═══════════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{B}║{header_line}║{RESET}")
        print(f"{B}╠═══════════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{B}║{RESET}  [1]  REFRESH         [2]  ENTER (CD)       [3]  UP (..)          [4]  DISK INFO              {B}║{RESET}")
        print(f"{B}║{RESET}  [5]  NEW FILE        [6]  NEW FOLDER       [7]  DELETE FILE      [8]  DELETE FOLDER          {B}║{RESET}")
        print(f"{B}║{RESET}  [9]  RENAME          [10] COPY (SHUTIL)    [11] MOVE             [12] SAVE LIST              {B}║{RESET}")
        print(f"{B}║{RESET}  [13] BACKUP (MIRROR) [14] SEARCH           [15] OPEN SAVES       [16] HELP                   {B}║{RESET}")
        print(f"{B}║{RESET}  [17] ABOUT           [18] EXIT                                                               {B}║{RESET}")
        print(f"{B}╚═══════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
        
        if self.msg:
            print(self.msg)
            self.msg = ""

    def run(self):
        while True:
            self.draw_menu()
            choice = input(f"{B} CMD CLI > {RESET}Select option: ").strip()
            if choice == "1": continue
            elif choice == "2": self.enter_dir()
            elif choice == "3": os.chdir("..")
            elif choice == "4": self.disk_info()
            elif choice == "5": self.make_file()
            elif choice == "6": self.make_dir()
            elif choice == "7": self.delete_file()
            elif choice == "8": self.delete_folder()
            elif choice == "9": self.rename_item()
            elif choice == "10": self.copy_item()
            elif choice == "11": self.move_item()
            elif choice == "12": self.save_list()
            elif choice == "13": self.backup()
            elif choice == "14": self.search()
            elif choice == "15": self.open_saves()
            elif choice == "16": self.show_help()
            elif choice == "17": self.show_about()
            elif choice == "18": break
            else: self.msg = f"{R} [!] Invalid choice!{RESET}"

    def enter_dir(self):
        folder = input(" [?] Folder name: ")
        try: os.chdir(folder)
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def disk_info(self):
        self.clear_screen()
        print(f"\n{B}  ═══ VOLUME AND DIRECTORY STATISTICS ═══{RESET}\n")
        try:
            usage = shutil.disk_usage(os.getcwd())
            print(f" {Y} [ DISK USAGE ]{RESET}")
            print(f" Total:     {usage.total // (2**30)} GB")
            print(f" Used:      {usage.used // (2**30)} GB")
            print(f" Free:      {usage.free // (2**30)} GB")
            input(f"\n{G}Press [ENTER] to return...{RESET}")
        except Exception as e: print(f"{R} [!] ERROR: {e}{RESET}")

    def make_file(self):
        name = input(" [+] New file name: ")
        try: Path(name).touch(); self.msg = f"{G} [+] Created successfully.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def make_dir(self):
        name = input(" [+] New folder name: ")
        try: os.makedirs(name, exist_ok=True); self.msg = f"{G} [+] Folder created.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def delete_file(self):
        name = input(" [!] File to delete: ")
        try: os.remove(name); self.msg = f"{G} [+] Deleted.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def delete_folder(self):
        name = input(" [!] Folder to delete: ")
        try: shutil.rmtree(name); self.msg = f"{G} [+] Directory deleted.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def rename_item(self):
        old = input(" [!] Current name: ")
        new = input(" [!] New name: ")
        try: os.rename(old, new); self.msg = f"{G} [+] Name changed.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def copy_item(self):
        src, dst = input(" [?] Source: "), input(" [?] Destination: ")
        try:
            if os.path.isdir(src): shutil.copytree(src, dst, dirs_exist_ok=True)
            else: shutil.copy2(src, dst)
            self.msg = f"{G} [+] Copied.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def move_item(self):
        src, dst = input(" [?] Source: "), input(" [?] Destination: ")
        try: shutil.move(src, dst); self.msg = f"{G} [+] Moved.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def save_list(self):
        folder_name = os.path.basename(os.getcwd()) or "DRIVE"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = self.save_path / f"{folder_name}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"REPORT - {datetime.now()}\n\n")
                for item in os.listdir('.'): f.write(f"{item}\n")
            self.msg = f"{G} [+] List saved.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def search(self):
        query = input(" [?] Search phrase: ")
        print(f"\n {Y}RESULTS:{RESET}")
        print(f"{B} ┌" + "─" * 94 + f"┐{RESET}")
        for path in Path('.').rglob(f"*{query}*"):
            line = str(path)[:90]
            print(f"{B} │{RESET}  {line:<91}{B}│{RESET}")
        print(f"{B} └" + "─" * 94 + f"┘{RESET}")
        input(f"\n{G}Back [ENTER]...{RESET}")

    def open_saves(self):
        try:
            if platform.system() == "Windows": os.startfile(self.save_path)
            else: subprocess.run(["xdg-open", str(self.save_path)])
        except Exception: pass

    def backup(self):
        src, dst = input(" [?] Source: "), input(" [?] Destination: ")
        try: shutil.copytree(src, dst, dirs_exist_ok=True); self.msg = f"{G} [+] Backup OK.{RESET}"
        except Exception as e: self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def show_help(self):
        self.clear_screen()
        print(f"{B}╔═══════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{B}║{RESET}                 SYSTEM DOCUMENTATION AND USER MANUAL                                      {B}║{RESET}")
        print(f"{B}╠═══════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{B}║{RESET}  {Y}1. NAVIGATION AND SYSTEM{RESET}                                                                 {B}║{RESET}")
        print(f"{B}║{RESET}  [1] REFRESH       - Updates the file view in the current folder.                         {B}║{RESET}")
        print(f"{B}║{RESET}  [2] ENTER (CD)    - Navigates to the specified folder (enter name).                      {B}║{RESET}")
        print(f"{B}║{RESET}  [3] UP (..)       - Returns to the parent directory.                                     {B}║{RESET}")
        print(f"{B}║{RESET}  [4] DISK INFO     - Displays space usage on the current volume.                          {B}║{RESET}")
        print(f"{B}║{RESET}                                                                                           {B}║{RESET}")
        print(f"{B}║{RESET}  {Y}2. FILE MANAGEMENT{RESET}                                                                       {B}║{RESET}")
        print(f"{B}║{RESET}  [5] NEW FILE      - Creates an empty text or system file.                                {B}║{RESET}")
        print(f"{B}║{RESET}  [6] NEW FOLDER    - Creates a new directory structure.                                   {B}║{RESET}")
        print(f"{B}║{RESET}  [7] DELETE FILE   - Permanently removes a file from disk.                                {B}║{RESET}")
        print(f"{B}║{RESET}  [8] DELETE DIR    - Deletes a folder along with all its contents.                        {B}║{RESET}")
        print(f"{B}║{RESET}                                                                                           {B}║{RESET}")
        print(f"{B}║{RESET}  {Y}3. ADVANCED OPERATIONS{RESET}                                                                   {B}║{RESET}")
        print(f"{B}║{RESET}  [9] RENAME        - Renames a file or folder.                                            {B}║{RESET}")
        print(f"{B}║{RESET}  [10] COPY         - Copies items (requires shutil module).                               {B}║{RESET}")
        print(f"{B}║{RESET}  [11] MOVE         - Moves a file/folder to another location.                             {B}║{RESET}")
        print(f"{B}║{RESET}  [13] BACKUP       - Creates a backup (Mirror) of the selected source.                    {B}║{RESET}")
        print(f"{B}║{RESET}                                                                                           {B}║{RESET}")
        print(f"{B}║{RESET}  {Y}4. TOOLS AND EXPORT{RESET}                                                                      {B}║{RESET}")
        print(f"{B}║{RESET}  [12] SAVE LIST    - Exports the file list to .txt format.                                {B}║{RESET}")
        print(f"{B}║{RESET}  [14] SEARCH       - Searches subdirectories for a given phrase.                          {B}║{RESET}")
        print(f"{B}║{RESET}  [15] OPEN SAVES   - Opens the system folder containing saved reports.                    {B}║{RESET}")
        print(f"{B}╠═══════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{B}║{RESET}  SHORTCUTS: Select a number [1-18] and press [ENTER].                                     {B}║{RESET}")
        print(f"{B}╚═══════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        input(f"\n{G}  Press [ENTER] to return to menu...{RESET}")

    def show_about(self):
        self.clear_screen()
        print(f"{B}╔══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"║                                ABOUT PROGRAM                             ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════╣\n")
        print(f" Name:        CMD File Manager Cli")
        print(f" Version:     1.5.0")
        print(f" Author:      {__author__}")
        print(f" Category:    {__category__}")
        print(f" Email:       polsoft.its@fastservice.com")
        print(f" GitHub:      https://github.com/seb07uk")
        print(f"\n Description: {__desc__}")
        print(f"\n{B}╚══════════════════════════════════════════════════════════════════════════╝{RESET}")
        input(f"\n{G}Press [ENTER] to return...{RESET}")

@command(name="file", aliases=["fm", "fileman"])
def run_file_manager():
    app = FileManager()
    app.run()

if __name__ == "__main__":
    app = FileManager()
    app.run()
