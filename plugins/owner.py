import os
import getpass
import platform
import socket
import json
from datetime import datetime
from cli import command, Color
import urllib.request
import sys
import uuid
import subprocess
import io
import csv
import re

__author__ = "Sebastian Januchowski"
__category__ = "info"
__group__ = "hack"
__desc__ = "Owner and environment information"

def get_os_info():
    u = platform.uname()
    arch = platform.architecture()[0]
    pyv = platform.python_version()
    build = None
    try:
        build = str(sys.getwindowsversion().build)
    except:
        build = None
    return {
        "system": u.system,
        "release": u.release,
        "version": u.version,
        "machine": u.machine,
        "processor": u.processor,
        "architecture": arch,
        "python_version": pyv,
        "build": build
    }

def get_network_info():
    def _local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            try:
                return socket.gethostbyname(socket.gethostname())
            except:
                return None
    def _is_online():
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=2).close()
            return True
        except:
            return False
    def _public_ip():
        try:
            with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=3) as r:
                data = json.loads(r.read().decode("utf-8"))
                return data.get("ip")
        except:
            return None
    def _mac():
        try:
            n = uuid.getnode()
            return ":".join(f"{(n >> (i*8)) & 0xff:02x}" for i in reversed(range(6)))
        except:
            return None
    info = {"local_ip": _local_ip(), "online": _is_online(), "mac": _mac()}
    if info["online"]:
        info["public_ip"] = _public_ip()
    return info

def get_interfaces():
    items = []
    try:
        out = subprocess.check_output(["getmac", "/v", "/fo", "csv"], encoding="utf-8", errors="ignore")
        reader = csv.DictReader(io.StringIO(out))
        for row in reader:
            name = (row.get("Connection Name") or row.get("Interface Name") or row.get("Name") or "").strip()
            mac = (row.get("Physical Address") or row.get("MAC Address") or "").strip()
            if mac:
                mac_norm = mac.replace("-", ":").lower()
            else:
                mac_norm = None
            items.append({"name": name, "mac": mac_norm})
    except Exception:
        try:
            out = subprocess.check_output(["ipconfig", "/all"], encoding="utf-8", errors="ignore")
            current = None
            for line in out.splitlines():
                l = line.strip()
                m = re.match(r'^.*adapter\s+(.+):$', l, flags=re.I)
                if m:
                    current = m.group(1).strip()
                    continue
                low = l.lower()
                if current and (("physical address" in low) or ("adres fizyczny" in low)):
                    parts = l.split(":", 1)
                    mac = parts[1].strip() if len(parts) > 1 else ""
                    mac_norm = mac.replace("-", ":").lower() if mac else None
                    items.append({"name": current, "mac": mac_norm})
                    current = None
        except Exception:
            pass
    return [i for i in items if i.get("name")]

def _settings_path():
    return os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings\terminal.json")

def get_preferred_adapter():
    try:
        p = _settings_path()
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                return (data.get("network", {}) or {}).get("preferred_adapter")
    except Exception:
        return None

def set_preferred_adapter(name):
    try:
        p = _settings_path()
        data = {}
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        if "network" not in data:
            data["network"] = {}
        data["network"]["preferred_adapter"] = name
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False

def get_preferred_mac():
    name = get_preferred_adapter()
    if not name:
        return None
    for it in get_interfaces():
        if it["name"].lower() == str(name).lower():
            return it["mac"]
    return None

def get_owner_info():
    username = getpass.getuser()
    
    metadata = {
        "version": "1.0.2",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "author": username,
        "environment": "TERMINAL CLI"
    }

    net = get_network_info()
    osi = get_os_info()

    info = {
        "metadata": metadata,
        "user": {
            "username": username,
            "hostname": socket.gethostname(),
            "home_directory": os.path.expanduser("~"),
            "os": platform.system(),
            "ip_address": net.get("local_ip")
        },
        "network": net,
        "os_details": osi,
        "paths": {
            "root": r"C:\Users\%userprofile%\.polsoft\psCLI",
            "settings": r"C:\Users\%userprofile%\.polsoft\psCli\settings\terminal.json",
            "games": r"C:\Users\%userprofile%\.polsoft\psCLI\Games"
        }
    }
    return info

def save_metadata(info):
    # Ścieżka do zapisu metadanych zgodnie z Twoją strukturą
    meta_dir = os.path.join(os.path.expanduser("~"), ".polsoft", "psCLI", "metadata")
    if not os.path.exists(meta_dir):
        os.makedirs(meta_dir)
        
    path = os.path.join(meta_dir, "echo.json")
    with open(path, "w") as f:
        json.dump(info, f, indent=4)
    return path

@command(name="owner", aliases=["about", "me", "whoami"])
def owner(*args):
    data = get_owner_info()
    if args and args[0].lower() == "save":
        p = save_metadata(data)
        print(f"{Color.GREEN}Saved:{Color.RESET} {p}")
        return
    if args and args[0].lower() == "mac":
        if len(args) == 1:
            print(f"{Color.CYAN}ADAPTERS & MAC{Color.RESET}")
            for it in get_interfaces():
                print(f"- {it['name']}: {it.get('mac')}")
            pref = get_preferred_adapter()
            if pref:
                print(f"Preferred: {pref}")
            return
        if args[1].lower() == "set" and len(args) >= 3:
            ok = set_preferred_adapter(" ".join(args[2:]))
            if ok:
                print(f"{Color.GREEN}Preferred adapter set:{Color.RESET} {' '.join(args[2:])}")
            else:
                print(f"{Color.RED}Failed to set preferred adapter{Color.RESET}")
            return
        # show MAC for specific adapter
        target = " ".join(args[1:])
        mac = None
        for it in get_interfaces():
            if it["name"].lower() == target.lower():
                mac = it.get("mac")
                break
        print(f"{Color.CYAN}{target}{Color.RESET} MAC: {mac}")
        return
    print(f"{Color.CYAN}OWNER INFORMATION{Color.RESET}")
    print(f"User: {data['user']['username']}")
    print(f"Host: {data['user']['hostname']}")
    print(f"Home: {data['user']['home_directory']}")
    print(f"OS: {data['user']['os']}")
    print(f"IP Address: {data['user'].get('ip_address')}")
    od = data.get("os_details", {})
    if od:
        print(f"OS Release: {od.get('release')}")
        print(f"OS Version: {od.get('version')}")
        if od.get('build'):
            print(f"OS Build: {od.get('build')}")
        print(f"Machine: {od.get('machine')}")
        print(f"Processor: {od.get('processor')}")
        print(f"Architecture: {od.get('architecture')}")
        print(f"Python: {od.get('python_version')}")
    print(f"Version: {data['metadata']['version']}")
    print(f"Updated: {data['metadata']['last_update']}")
    print(f"Local IP: {data.get('network', {}).get('local_ip')}")
    print(f"Online: {data.get('network', {}).get('online')}")
    if data.get('network', {}).get('public_ip'):
        print(f"Public IP: {data['network']['public_ip']}")
    print(f"MAC: {data.get('network', {}).get('mac')}")

if __name__ == "__main__":
    data = get_owner_info()
    save_path = save_metadata(data)
    
    print(f"--- OWNER METADATA UPDATED ---")
    print(f"User: {data['user']['username']}")
    print(f"Version: {data['metadata']['version']}")
    print(f"File: {save_path}")
