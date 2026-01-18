import os
import sys
import platform
import re
from datetime import datetime, timedelta

def print_help():
    help_text = """
    TERMINAL CLI - System Reboot Utility
    ====================================
    Użycie: python reboot.py [opcja]

    Dostępne formaty:
    1. Brak argumentu     - Restartuje komputer w ciągu 1 sekundy.
    2. t[sekundy]         - Restart za określoną liczbę sekund (np. t30).
    3. t[HH-MM-SS]        - Restart o konkretnej godzinie (np. t12-10-00).
    4. help / --h         - Wyświetla tę pomoc.
    5. abort              - Anuluje zaplanowany restart.

    Przykłady:
    python reboot.py t60       # Restart za minutę
    python reboot.py t23-59-00 # Restart tuż przed północą

    ------------------------------------
    Sebastian Januchowski
    polsoft.its@fastservice.com
    https://github.com/seb07uk
    2026© polsoft.ITS London
    """
    print(help_text)

def abort_reboot():
    if platform.system() == "Windows":
        os.system("shutdown /a")
        print("Zaplanowany restart został anulowany.")
    else:
        os.system("sudo shutdown -c")
        print("Reboot cancelled.")

def get_seconds_until(time_str):
    try:
        now = datetime.now()
        target_time = datetime.strptime(time_str, "%H-%M-%S")
        target_datetime = now.replace(hour=target_time.hour, minute=target_time.minute, second=target_time.second)
        if target_datetime < now:
            target_datetime += timedelta(days=1)
        return int((target_datetime - now).total_seconds())
    except ValueError:
        print("Błąd: Nieprawidłowy format czasu HH-MM-SS.")
        sys.exit(1)

def reboot_system(delay):
    if platform.system() == "Windows":
        os.system(f"shutdown /r /t {delay} /f")
    else:
        # Konwersja na minuty dla systemów Unix
        delay_min = max(1, delay // 60)
        os.system(f"sudo shutdown -r +{delay_min}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        reboot_system(1)
    else:
        arg = sys.argv[1].lower()
        
        if arg in ["help", "--h", "/?"]:
            print_help()
        elif arg == "abort":
            abort_reboot()
        elif arg.startswith("t"):
            val = arg[1:]
            if "-" in val:
                sec = get_seconds_until(val)
                print(f"Restart zaplanowany na {val.replace('-', ':')} (za {sec}s).")
                reboot_system(sec)
            elif val.isdigit():
                sec = int(val)
                print(f"Restart za {sec} sekund.")
                reboot_system(sec)
        else:
            print("Nieznany argument. Wpisz 'python reboot.py help'.")