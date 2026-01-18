import os
import sys
import platform
import re
from datetime import datetime, timedelta
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__email__ = "polsoft.its@fastservice.com"
__github__ = "https://github.com/seb07uk"
__category__ = "system"
__group__ = "core"
__desc__ = "System Shutdown Utility - schedule or abort system shutdown"

def print_help():
    help_text = f"""
    {Color.CYAN}TERMINAL CLI - System Shutdown Utility{Color.RESET}
    {Color.CYAN}======================================{Color.RESET}
    {Color.WHITE}Usage:{Color.RESET} python shutdown.py {Color.GREEN}[option]{Color.RESET}

    {Color.YELLOW}Available formats:{Color.RESET}
    1. {Color.GREEN}No argument{Color.RESET}        - Shuts down the computer in 1 second.
    2. {Color.GREEN}t[seconds]{Color.RESET}         - Shutdown after a specified number of seconds (e.g., t30).
    3. {Color.GREEN}t[HH-MM-SS]{Color.RESET}        - Shutdown at a specific time (e.g., t12-10-00).
    4. {Color.GREEN}help / --h{Color.RESET}         - Displays this help message.
    5. {Color.GREEN}abort{Color.RESET}              - Cancels a scheduled shutdown.

    {Color.YELLOW}Examples:{Color.RESET}
    {Color.WHITE}python shutdown.py t60{Color.RESET}       {Color.BLUE}# Shutdown in one minute{Color.RESET}
    {Color.WHITE}python shutdown.py t23-59-00{Color.RESET} # Shutdown just before midnight{Color.RESET}

    {Color.CYAN}------------------------------------{Color.RESET}
    {Color.WHITE}Sebastian Januchowski{Color.RESET}
    {Color.BLUE}polsoft.its@fastservice.com{Color.RESET}
    {Color.BLUE}https://github.com/seb07uk{Color.RESET}
    {Color.WHITE}2026© polsoft.ITS London{Color.RESET}
    """
    print(help_text)

def abort_shutdown():
    if platform.system() == "Windows":
        os.system("shutdown /a")
        print(f"{Color.GREEN}Scheduled shutdown has been cancelled.{Color.RESET}")
    else:
        os.system("sudo shutdown -c")
        print(f"{Color.GREEN}Shutdown cancelled.{Color.RESET}")

def get_seconds_until(time_str):
    try:
        now = datetime.now()
        target_time = datetime.strptime(time_str, "%H-%M-%S")
        target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute, second=target_time.second)
        if target_datetime < now:
            target_datetime += timedelta(days=1)
        return int((target_datetime - now).total_seconds())
    except ValueError:
        print(f"{Color.RED}[!] Error: Invalid time format HH-MM-SS.{Color.RESET}")
        sys.exit(1)

def shutdown_system(delay):
    if platform.system() == "Windows":
        os.system(f"shutdown /s /t {delay} /f")
    else:
        # Convert to minutes for Unix systems
        delay_min = max(1, delay // 60)
        os.system(f"sudo shutdown -h +{delay_min}")

@command(name="shutdown", aliases=["poweroff", "sd"])
def run(*args):
    """
    Schedule system shutdown or abort scheduled shutdown.
    Usage: shutdown [t<seconds|HH-MM-SS>] | shutdown abort | shutdown help
    """
    # Help handler
    if args and args[0] in ["help", "--h", "/?", "-h"]:
        print_help()
        return
    
    # Abort handler
    if args and args[0].lower() == "abort":
        abort_shutdown()
        return
    
    # No arguments - shutdown immediately
    if not args:
        shutdown_system(1)
        return
    
    # Process time argument
    arg = args[0].lower()
    
    if arg.startswith("t"):
        val = arg[1:]
        if "-" in val:
            sec = get_seconds_until(val)
            print(f"{Color.YELLOW}Shutdown scheduled for {val.replace('-', ':')} (in {sec}s).{Color.RESET}")
            shutdown_system(sec)
        elif val.isdigit():
            sec = int(val)
            print(f"{Color.YELLOW}Shutdown in {sec} seconds.{Color.RESET}")
            shutdown_system(sec)
        else:
            print(f"{Color.RED}[!] Error: Invalid argument format '{arg}'{Color.RESET}")
    else:
        print(f"{Color.RED}[!] Unknown argument. Type 'shutdown help' for assistance.{Color.RESET}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        shutdown_system(1)
    else:
        arg = sys.argv[1].lower()
        
        if arg in ["help", "--h", "/?"]:
            print_help()
        elif arg == "abort":
            abort_shutdown()
        elif arg.startswith("t"):
            val = arg[1:]
            if "-" in val:
                sec = get_seconds_until(val)
                print(f"{Color.YELLOW}Shutdown scheduled for {val.replace('-', ':')} (in {sec}s).{Color.RESET}")
                shutdown_system(sec)
            elif val.isdigit():
                sec = int(val)
                print(f"{Color.YELLOW}Shutdown in {sec} seconds.{Color.RESET}")
                shutdown_system(sec)
        else:
            print(f"{Color.RED}Unknown argument. Type 'python shutdown.py help'.{Color.RESET}")