import os
import re
import json
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "maintenance"
__group__ = "python"
__desc__ = "Automatyczna integracja: wykrywa moduły, tworzy metadane i rejestruje"

@command(name="integrate", aliases=["autometadata", "genmeta"])
def integrate(*args):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    meta_dir = os.path.join(root, "metadata")
    if not os.path.exists(meta_dir):
        os.makedirs(meta_dir, exist_ok=True)

    targets = {
        "plugins": {"exts": [".py"], "namer": lambda n, e: f"{n}.py.json"},
        "games": {"exts": [".py"], "namer": lambda n, e: f"{n}.json"},
        "ascii": {"exts": [".bat", ".cmd", ".ps1", ".exe", ".vbs"], "namer": lambda n, e: f"{n}{e}.json"},
        "health": {"exts": [".bat", ".cmd", ".ps1", ".exe", ".vbs"], "namer": lambda n, e: f"{n}{e}.json"},
        "tools": {"exts": [".bat", ".cmd", ".ps1", ".exe", ".vbs"], "namer": lambda n, e: f"{n}{e}.json"},
        "install": {"exts": [".bat", ".cmd", ".ps1", ".exe", ".vbs"], "namer": lambda n, e: f"{n}{e}.json"}
    }

    created = []
    skipped = []

    def read_fields(path):
        fields = {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                s = f.read()
            for k in ["__author__", "__category__", "__group__", "__desc__"]:
                m = re.search(rf"{k}\s*=\s*['\"](.*?)['\"]", s)
                if m:
                    fields[k.strip("_")] = m.group(1)
        except:
            pass
        return fields

    for folder, spec in targets.items():
        base = os.path.join(root, folder)
        if not os.path.exists(base):
            continue
        for fname in os.listdir(base):
            fpath = os.path.join(base, fname)
            if os.path.isdir(fpath) or fname.startswith("__"):
                continue
            name, ext = os.path.splitext(fname)
            ext = ext.lower()
            if ext not in spec["exts"]:
                continue
            meta_name = spec["namer"](name, ext)
            meta_path = os.path.join(meta_dir, meta_name)
            if os.path.exists(meta_path):
                skipped.append(meta_name)
                continue

            data = {
                "author": "System",
                "category": "games" if folder == "games" else ("tool" if folder != "plugins" else "general"),
                "group": "games" if folder == "games" else (folder if folder != "plugins" else "python"),
                "desc": "Auto-generated metadata",
                "aliases": []
            }

            if ext == ".py":
                fields = read_fields(fpath)
                for k in ["author", "category", "group", "desc"]:
                    if k in fields:
                        data[k] = fields[k]

            try:
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                created.append(meta_name)
            except:
                pass

    print(f"{Color.GREEN}[OK]{Color.RESET} Created: {len(created)} | Skipped (exists): {len(skipped)}")
    if created:
        for m in created[:20]:
            print(f"{Color.CYAN} + {m}{Color.RESET}")
    if skipped:
        print(f"{Color.GRAY}Already present:{Color.RESET} {', '.join(skipped[:10])}{(' ...' if len(skipped)>10 else '')}")
