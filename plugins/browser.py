import urllib.request
import urllib.parse
import http.cookiejar
import html.parser
import textwrap
import shutil
import os
import json
import re
from datetime import datetime
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "web browser"
__group__ = "office"
__desc__ = "psBrowser CLI: Full Suite with History & Quick Links"

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.join(os.environ['USERPROFILE'], ".polsoft", "psCli", "Browser")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "Screenshots")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "Downloads")
COOKIE_FILE = os.path.join(BASE_DIR, "cookies.txt")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

for path in [BASE_DIR, SCREENSHOT_DIR, DOWNLOAD_DIR]:
    if not os.path.exists(path): os.makedirs(path)

# --- SESSION CONFIGURATION ---
cookie_jar = http.cookiejar.MozillaCookieJar(COOKIE_FILE)
if os.path.exists(COOKIE_FILE):
    try: cookie_jar.load(ignore_discard=True, ignore_expires=True)
    except: pass
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)

def save_history(url):
    history_data = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f: history_data = json.load(f)
        except: pass
    
    history_data.append({"url": url, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    # Keep only the last 50 entries
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history_data[-50:], f, indent=4)

class FullParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = ""
        self.links = []
        self.forms = []
        self.ignore_tags = {"script", "style", "head", "title", "meta", "link", "nav", "footer", "aside"}
        self.is_ignored = False
        self.width, _ = shutil.get_terminal_size((80, 20))

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in self.ignore_tags: self.is_ignored = True
        if tag == "input" and not self.is_ignored:
            if attrs_dict.get("type") in ["text", "search", "password", None]:
                name = attrs_dict.get("name", "query")
                self.forms.append({"name": name, "action": ""})
                self.text_content += f" {Color.CYAN}[S{len(self.forms)}]{Color.RESET} "
        if tag == "form": self.last_form_action = attrs_dict.get("action", "")
        if tag in ["h1", "h2", "h3"]: self.text_content += f"\n\n{Color.BOLD}{Color.CYAN}# "
        elif tag in ["p", "div", "li", "tr"]: self.text_content += "\n"
        elif tag == "a" and not self.is_ignored:
            href = attrs_dict.get("href")
            if href:
                self.links.append(href)
                self.text_content += f" {Color.YELLOW}[{len(self.links)}]{Color.RESET} "

    def handle_endtag(self, tag):
        if tag in self.ignore_tags: self.is_ignored = False

    def handle_data(self, data):
        if not self.is_ignored:
            cleaned = " ".join(data.split())
            if cleaned: self.text_content += cleaned + " "

    def get_formatted_text(self):
        lines = [line.strip() for line in self.text_content.split('\n') if line.strip()]
        wrapped = [textwrap.fill(line, width=self.width - 4) for line in lines]
        return "\n\n".join(wrapped)

def download_file(url):
    try:
        local_filename = os.path.join(DOWNLOAD_DIR, url.split('/')[-1].split('?')[0])
        print(f"{Color.YELLOW}[DOWNLOAD]{Color.RESET} Downloading: {url}...")
        with urllib.request.urlopen(url) as response, open(local_filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print(f"{Color.GREEN}[OK]{Color.RESET} Saved in Downloads.")
    except Exception as e:
        print(f"{Color.RED}[ERROR]{Color.RESET} {e}")

def fetch_content(url):
    if not url.startswith("http"): url = "http://" + url
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content_type = response.info().get_content_type()
            if "html" not in content_type:
                download_file(url)
                return "DOWNLOAD", None, [], [], ""
            
            cookie_jar.save(ignore_discard=True, ignore_expires=True)
            real_url = response.geturl()
            save_history(real_url)
            raw_data = response.read().decode('utf-8', errors='ignore')
            parser = FullParser()
            parser.feed(raw_data)
            for f in parser.forms:
                if not f["action"]: f["action"] = real_url
            return real_url, parser.get_formatted_text(), [urllib.parse.urljoin(real_url, l) for l in parser.links], parser.forms, raw_data
    except Exception as e:
        print(f"{Color.RED}[ERROR]{Color.RESET} {e}")
        return None, None, [], [], ""

def show_about():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Color.BOLD}{Color.BLUE}--- psBrowser CLI ---{Color.RESET}")
    print(f"{Color.WHITE}author:  Sebastian Januchowski")
    print(f"email:   polsoft.its@fastservice.com")
    print(f"github:  https://github.com/seb07uk{Color.RESET}")
    print("-" * 30)
    input("\nPress Enter to continue...")

@command(name="browser", aliases=["web", "www"])
def browse(url=None):
    """psBrowser CLI: [Nr] Link, [S(nr)] Search, [h] History, [snap] Screenshot, [u] Back."""
    history_stack = []
    current_url = url or "google.com"

    while current_url and current_url.lower() not in ['q', 'quit']:
        if current_url.lower() == 'about':
            show_about()
            current_url = history_stack[-1] if history_stack else "google.com"
            continue
        
        if current_url.lower() == 'h':
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f: 
                    h_list = json.load(f)
                    print(f"\n{Color.BOLD}RECENT HISTORY:{Color.RESET}")
                    for entry in h_list[-15:]: print(f"[{entry['ts']}] {entry['url']}")
            else:
                print("\nNo history found.")
            input("\nPress Enter...")
            current_url = history_stack[-1] if history_stack else "google.com"
            continue

        res = fetch_content(current_url)
        if res[0] == "DOWNLOAD":
            current_url = history_stack.pop() if history_stack else "google.com"
            continue
            
        real_url, content, links, forms, raw_html = res
        if content:
            if not history_stack or history_stack[-1] != current_url: history_stack.append(current_url)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Color.GRAY}psBrowser CLI | {real_url}{Color.RESET}")
            print("-" * shutil.get_terminal_size().columns)
            print(content)
            print("-" * shutil.get_terminal_size().columns)
        
        print(f"{Color.CYAN}NAV:{Color.RESET} [Nr] Link | [S(nr) text] | [h] history | [about] info | [u] back | [g] google | [q] exit")
        cmd = input(f"{Color.GREEN}WWW{Color.RESET} > ").strip()

        if not cmd: continue
        if cmd.lower() == 'q': break
        if cmd.lower() == 'about': current_url = 'about'; continue
        if cmd.lower() == 'h': current_url = 'h'; continue
        if cmd.lower() == 'g': current_url = "google.com"; continue
        if cmd.lower() == 'u' and len(history_stack) > 1:
            history_stack.pop(); current_url = history_stack.pop(); continue
        
        if cmd.lower().startswith("get "):
            try:
                idx = int(cmd.split()[1]) - 1
                download_file(links[idx])
            except: print("Command 'get' error.")
            continue

        if cmd.lower() == 'snap':
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = os.path.join(SCREENSHOT_DIR, f"snap_{ts}.txt")
            with open(fname, "w", encoding="utf-8") as f: f.write(content)
            print(f"Saved to: {fname}"); input("Enter..."); continue

        if cmd.upper().startswith("S"):
            try:
                parts = cmd.split(" ", 1)
                idx = int(re.search(r'\d+', parts[0]).group()) - 1
                current_url = f"{forms[idx]['action']}?{urllib.parse.urlencode({forms[idx]['name']: parts[1]})}"
            except: pass
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(links): current_url = links[idx]
        else:
            current_url = cmd