# Import decorator from main CLI file
from cli import command
import ctypes
import shutil
import platform
import os
import subprocess

# -------------------------
# Module metadata
# -------------------------
__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__version__ = "1.1.1"
__date__ = "2026-01-10"
__group__ = "system"
__category__ = "info"
__desc__ = "Show integrated Windows system info, drives and processes"
__all__ = ["run"]

# ANSI colors for styling
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[91m"
GRAY = "\033[90m"

@command(name="syswin", aliases=["swi", "disks", "ps"])
def run(*args):
    """
    Displays integrated Windows system information.
    Supports aliases: list, ls, disks, ps.
    """
    # If no arguments or first argument is help trigger
    if args and args[0] in ["help", "--help", "-h", "?"]:
        show_plugin_help()
        return

    mode = args[0].lower() if args else "all"

    print(f"\n{CYAN}{BOLD}--- WINDOWS SYSTEM INTEGRATION ---{RESET}")

    if mode in ["os", "all"]:
        display_os_info()

    if mode in ["mem", "all"]:
        display_memory_info()

    if mode in ["drives", "all"]:
        display_drive_info()

    if mode in ["proc", "ps"]:
        display_processes()

    if mode == "all":
        print(f"{GRAY}Tip: Use 'syswin proc' to see all running processes.{RESET}")

    print(f"{CYAN}{BOLD}----------------------------------{RESET}\n")

def show_plugin_help():
    """Internal help for the syswin module."""
    print(f"\n{CYAN}SysWin Plugin Help{RESET}")
    print(f"{YELLOW}Description: {RESET}{__desc__}")
    print(f"{YELLOW}Aliases:     {RESET}list, ls, disks, ps")
    print(f"{YELLOW}Usage:        {RESET}syswin <mode>")
    print(f"{YELLOW}Modes:        {RESET}")
    print(f"  {GREEN}os{RESET}      - Display Windows version and architecture")
    print(f"  {GREEN}mem{RESET}     - Show RAM usage (Total/Free)")
    print(f"  {GREEN}drives{RESET}  - List all drives with storage stats")
    print(f"  {GREEN}proc{RESET}    - List top running processes")
    print(f"  {GREEN}all{RESET}     - Show everything (default)")
    print(f"{CYAN}Example:      {RESET}syswin mem\n")

def display_os_info():
    """Displays Windows OS details using platform module."""
    print(f"{YELLOW}[OS Info]{RESET}")
    print(f"  Name:     {platform.system()} {platform.release()}")
    print(f"  Build:    {platform.version()}")
    print(f"  Arch:     {platform.machine()}")
    print("")

def display_memory_info():
    """Fetches RAM status using GlobalMemoryStatusEx via ctypes."""
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_uint),
            ("dwMemoryLoad", ctypes.c_uint),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))

    total_gb = stat.ullTotalPhys / (1024**3)
    avail_gb = stat.ullAvailPhys / (1024**3)
    
    print(f"{YELLOW}[Memory]{RESET}")
    print(f"  Load:     {stat.dwMemoryLoad}%")
    print(f"  Total:    {total_gb:.2f} GB")
    print(f"  Free:     {avail_gb:.2f} GB")
    print("")

def display_drive_info():
    """Lists all logical drives and their storage capacity."""
    print(f"{YELLOW}[Storage]{RESET}")
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    
    for i in range(26):
        if bitmask & (1 << i):
            drive_letter = f"{chr(65 + i)}:\\"
            try:
                total, used, free = shutil.disk_usage(drive_letter)
                free_pct = (free / total) * 100
                print(f"  {GREEN}{drive_letter}{RESET} {free/(1024**3):.1f} GB free / {total/(1024**3):.1f} GB total ({free_pct:.1f}%)")
            except Exception:
                continue
    print("")

def display_processes():
    """Lists running processes using Windows tasklist."""
    print(f"{YELLOW}[Running Processes - Top 15 by Name]{RESET}")
    try:
        output = subprocess.check_output("tasklist /NH /FI \"STATUS eq running\"", shell=True).decode("cp852")
        lines = output.strip().split('\n')
        
        for line in lines[:15]:
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                pid = parts[1]
                mem = parts[-2] + " " + parts[-1]
                print(f"  {GRAY}{pid:<8}{RESET} {name:<25} {GREEN}{mem:>12}{RESET}")
    except Exception as e:
        print(f"  {RED}Error fetching processes: {e}{RESET}")