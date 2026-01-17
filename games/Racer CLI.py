# --- PLUGIN METADATA (Read by Dispatcher._load_python_module) ---
__author__ = "Sebastian Januchowski"
__category__ = "games"
__group__ = "entertainment"
__desc__ = "Retro arcade Racer CLI game with levels."

import tkinter as tk
import random
import json
import os
from tkinter import simpledialog

# Improve font clarity on Windows (High DPI Awareness)
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class RacerCLI:
    def __init__(self, root):
        self.root = root
        self.root.title("TERMINAL CLI - Racer CLI")
        
        # Application Dimensions
        self.win_width = 600
        self.win_height = 750
        
        # Disable window resizing
        self.root.resizable(False, False)
        
        # Fonts
        self.font_main = ("Segoe UI", 45, "bold")
        self.font_btn = ("Segoe UI", 14, "bold")
        self.font_text = ("Segoe UI", 12)
        self.font_mono = ("Consolas", 14)
        self.font_footer = ("Consolas", 10)
        
        # Colors
        self.bg_color = "#111"
        self.footer_color = "#888"
        
        # File Paths
        user_home = os.environ.get('USERPROFILE', os.path.expanduser('~'))
        self.base_dir = os.path.join(user_home, ".polsoft", "psCLI", "Games")
        self.stats_file = os.path.join(self.base_dir, "Racer_HighScores.json")
        
        self.ensure_dir()
        self.scores_list = self.load_scores()
        self.running = False
        self.obstacles = []
        
        self.center_window()
        self.show_main_menu()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.win_width // 2)
        y = (screen_height // 2) - (self.win_height // 2)
        self.root.geometry(f"{self.win_width}x{self.win_height}+{x}+{y}")

    def ensure_dir(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def load_scores(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r") as f:
                    data = json.load(f)
                    return sorted(data, key=lambda x: x['score'], reverse=True)[:5]
            except: return []
        return []

    def save_new_score(self, name, score):
        self.scores_list.append({"name": name, "score": score})
        self.scores_list = sorted(self.scores_list, key=lambda x: x['score'], reverse=True)[:5]
        try:
            with open(self.stats_file, "w") as f:
                json.dump(self.scores_list, f, indent=4)
        except: pass

    def show_main_menu(self):
        for w in self.root.winfo_children(): w.destroy()
        self.root.configure(bg=self.bg_color)

        tk.Label(self.root, text="Racer CLI", fg="#0f0", bg=self.bg_color, font=self.font_main).pack(pady=50)
        
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(expand=True)

        buttons = [
            ("NEW GAME", self.start_game),
            ("HIGH SCORES", self.show_high_scores),
            ("HELP", self.show_help),
            ("EXIT", self.root.quit)
        ]

        for text, cmd in buttons:
            tk.Button(buttons_frame, text=text, command=cmd, width=22, height=2, 
                      bg="#222", fg="white", font=self.font_btn, 
                      relief="flat", activebackground="#0f0", activeforeground="#000",
                      cursor="hand2").pack(pady=10)

        footer_text = "Sebastian Januchowski\n2026© polsoft.ITS London"
        tk.Label(self.root, text=footer_text, fg=self.footer_color, bg=self.bg_color, 
                 font=self.font_footer, justify="center").pack(side="bottom", pady=20)

    def show_help(self):
        for w in self.root.winfo_children(): w.destroy()
        tk.Label(self.root, text="HELP & DESCRIPTION", fg="#0f0", bg=self.bg_color, font=("Segoe UI", 30, "bold")).pack(pady=20)
        
        description = (
            "Welcome to Racer CLI – a dynamic arcade game in retro style!\n"
            "You take on the role of a digital racer speeding through an endless\n"
            "stream of data. Your task is to survive as long as possible."
        )

        help_text = (
            "CONTROLS:\n"
            "• [A] or [Left Arrow]  - Turn Left\n"
            "• [D] or [Right Arrow] - Turn Right\n\n"
            "RULES:\n"
            "• Avoid red blocks – collision ends the run.\n"
            "• You gain 1 point for every obstacle passed.\n"
            "• Speed increases every 8 points."
        )
        
        tk.Label(self.root, text=description, fg="#ccc", bg=self.bg_color, font=self.font_text, 
                 justify="center", wraplength=500).pack(pady=10)
        tk.Label(self.root, text=help_text, fg="white", bg=self.bg_color, font=self.font_text, 
                 justify="left").pack(pady=10)
        
        tk.Button(self.root, text="BACK", command=self.show_main_menu, width=15, 
                  bg="#333", fg="white", font=self.font_btn, relief="flat").pack(pady=15)

        author_info = (
            "author:  Sebastian Januchowski\n"
            "email:   polsoft.its@fastservice.com\n"
            "github:  https://github.com/seb07uk\n"
        )
        tk.Label(self.root, text=author_info, fg=self.footer_color, bg=self.bg_color, 
                 font=self.font_footer, justify="left").pack(side="bottom", pady=20)

    def show_high_scores(self):
        for w in self.root.winfo_children(): w.destroy()
        tk.Label(self.root, text="TOP 5 PLAYERS", fg="yellow", bg=self.bg_color, font=("Segoe UI", 30, "bold")).pack(pady=40)
        
        if not self.scores_list:
            tk.Label(self.root, text="NO SCORES YET", fg="gray", bg=self.bg_color, font=self.font_text).pack(pady=20)
        else:
            for i, entry in enumerate(self.scores_list):
                txt = f"{i+1}. {entry['name'][:10]:<10} {entry['score']:>5}"
                tk.Label(self.root, text=txt, fg="white", bg=self.bg_color, font=self.font_mono).pack(pady=5)

        tk.Button(self.root, text="BACK", command=self.show_main_menu, width=15, 
                  bg="#333", fg="white", font=self.font_btn, relief="flat").pack(pady=40)

    def start_game(self):
        for w in self.root.winfo_children(): w.destroy()
        self.score = 0
        self.obstacles = []
        self.running = True
        
        self.canvas = tk.Canvas(self.root, width=450, height=750, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.player = self.canvas.create_rectangle(210, 680, 240, 710, fill="#00ffff", outline="white", width=2)
        self.score_lbl = self.canvas.create_text(20, 20, anchor="nw", text="Score: 0", fill="white", font=self.font_btn)

        self.root.bind("<a>", lambda e: self.move(-30))
        self.root.bind("<d>", lambda e: self.move(30))
        self.root.bind("<Left>", lambda e: self.move(-30))
        self.root.bind("<Right>", lambda e: self.move(30))
        self.loop()

    def move(self, dx):
        if not self.running: return
        p = self.canvas.coords(self.player)
        if 0 <= p[0] + dx <= 420: 
            self.canvas.move(self.player, dx, 0)

    def loop(self):
        if not self.running: return
        if random.random() < 0.12:
            x = random.randint(0, 390)
            o = self.canvas.create_rectangle(x, -60, x + 60, 0, fill="#ff3333", outline="#ff9999", width=1)
            self.obstacles.append(o)

        for o in self.obstacles[:]:
            speed = 7 + (self.score // 8)
            self.canvas.move(o, 0, speed)
            pos = self.canvas.coords(o)
            
            if pos[1] > 750:
                self.canvas.delete(o)
                self.obstacles.remove(o)
                self.score += 1
                self.canvas.itemconfig(self.score_lbl, text=f"Score: {self.score}")
            
            p = self.canvas.coords(self.player)
            if not (p[2] < pos[0] or p[0] > pos[2] or p[3] < pos[1] or p[1] > pos[3]):
                self.game_over()
                return
        self.root.after(30, self.loop)

    def game_over(self):
        self.running = False
        self.canvas.create_text(225, 300, text="CRASH!", fill="red", font=self.font_main)
        self.root.update()
        
        is_top = len(self.scores_list) < 5 or (self.score > 0 and (not self.scores_list or self.score > self.scores_list[-1]['score']))
        if is_top:
            name = simpledialog.askstring("New Record!", f"Your Score: {self.score}\nEnter Name:", parent=self.root)
            if not name: name = "Player"
            self.save_new_score(name[:10], self.score)
        else:
            self.root.after(1500)
        self.show_high_scores()

if __name__ == "__main__":
    root = tk.Tk()
    app = RacerCLI(root)
    root.mainloop()