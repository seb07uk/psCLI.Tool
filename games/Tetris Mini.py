# --- PLUGIN METADATA (Read by Dispatcher._load_python_module) ---
__author__ = "Sebastian Januchowski"
__category__ = "games"
__group__ = "entertainment"
__desc__ = "Retro arcade Tetris game with levels, high-score ranking and neon graphics."

import tkinter as tk
from tkinter import simpledialog
import random
import json
import os

# Path configuration for TERMINAL CLI
GAMES_DIR = os.path.expandvars(r"C:\Users\%userprofile%\.polsoft\psCLI\Games")
SETTINGS_FILE = os.path.join(GAMES_DIR, "Tetris.json")
COLUMNS, ROWS, TILE_SIZE = 10, 20, 30

class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris Mini")
        self.state = "MENU"
        self.menu_index = 0
        self.menu_options = ["NEW GAME", "TOP 5", "HELP", "EXIT"]
        self.blink_state = True
        
        self.ensure_settings_exists()
        
        self.canvas = tk.Canvas(root, width=COLUMNS*TILE_SIZE, height=ROWS*TILE_SIZE + 40, bg='#222222', highlightthickness=0)
        self.canvas.pack()
        
        self.root.bind("<KeyPress>", self.handle_input)
        self.show_menu()

    def ensure_settings_exists(self):
        try:
            if not os.path.exists(GAMES_DIR): os.makedirs(GAMES_DIR, exist_ok=True)
            if not os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                    json.dump({"top_scores": []}, f, indent=4)
        except Exception: pass

    def load_scores(self):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get("top_scores", [])
        except: return []

    def check_high_score(self):
        if self.score <= 0: return
        scores = self.load_scores()
        is_new_best = not scores or self.score > scores[0].get('score', 0)
        
        if len(scores) < 5 or self.score > scores[-1].get('score', 0):
            if is_new_best: self.show_celebration()
            
            self.root.update() 
            name = simpledialog.askstring("New Record!", "Enter your name:", parent=self.root)
            if not name: name = "Player"
            
            scores.append({"name": name[:10], "score": self.score})
            scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
            
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump({"top_scores": scores}, f, indent=4)

    def show_celebration(self):
        """Displays a flashing high score message."""
        for _ in range(6):
            self.canvas.create_text(150, 200, text="!!! NEW BEST !!!", fill="gold", font=('Consolas', 24, 'bold'), tags="blink")
            self.root.update()
            self.root.after(200)
            self.canvas.delete("blink")
            self.root.update()
            self.root.after(200)

    def start_game(self):
        self.state = "GAME"
        self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.score, self.level, self.speed = 0, 1, 500
        self.game_over = False
        self.spawn_piece()
        self.run_game_loop()

    def show_menu(self):
        self.canvas.delete("all")
        self.canvas.create_text(150, 80, text="TETRIS MINI", fill="#0FFF50", font=('Consolas', 34, 'bold'))
        for i, option in enumerate(self.menu_options):
            color = "#FFFFFF" if i != self.menu_index else "#0FFF50"
            prefix = "> " if i == self.menu_index else "  "
            self.canvas.create_text(150, 250 + (i * 40), text=prefix + option, fill=color, font=('Consolas', 14, 'bold'))
        
        footer = "Sebastian Januchowski\n2026© polsoft.ITS London"
        self.canvas.create_text(150, 580, text=footer, fill="#AAAAAA", font=('Consolas', 8), justify="center")

    def show_top5(self):
        self.canvas.delete("all")
        scores = self.load_scores()
        self.canvas.create_text(150, 80, text="TOP 5 PLAYERS", fill="#FFD700", font=('Consolas', 18, 'bold'))
        for i, s in enumerate(scores):
            name, pts = s.get('name', '???'), s.get('score', 0)
            self.canvas.create_text(50, 180 + (i * 40), anchor="w", text=f"{i+1}. {name}", fill="white", font=('Consolas', 12))
            self.canvas.create_text(250, 180 + (i * 40), anchor="e", text=f"{pts} PTS", fill="#00FFFF", font=('Consolas', 12))
        self.canvas.create_text(150, 550, text="ENTER = BACK", fill="#BBBBBB", font=('Consolas', 10))

    def show_help(self):
        self.canvas.delete("all")
        self.canvas.create_text(150, 50, text="HELP & INFO", fill="#00FFFF", font=('Consolas', 18, 'bold'))
        desc = "Arrange falling blocks to form\ncomplete lines. Full lines vanish,\ngiving points. Speed increases\nas you score more!"
        self.canvas.create_text(150, 140, text=desc, fill="#DDDDDD", font=('Consolas', 9), justify="center")
        controls = "LEF/RIGHT: Move\nUP: Rotate\nDOWN: Soft Drop"
        self.canvas.create_text(150, 260, text=controls, fill="white", font=('Consolas', 10, 'bold'), justify="center")
        self.canvas.create_text(150, 580, text="ENTER = BACK", fill="#BBBBBB", font=('Consolas', 9))

    def handle_input(self, event):
        key = event.keysym
        if self.state == "MENU":
            if key == "Up": self.menu_index = (self.menu_index - 1) % len(self.menu_options); self.show_menu()
            elif key == "Down": self.menu_index = (self.menu_index + 1) % len(self.menu_options); self.show_menu()
            elif key == "Return":
                choice = self.menu_options[self.menu_index]
                if choice == "NEW GAME": self.start_game()
                elif choice == "TOP 5": self.state = "TOP5"; self.show_top5()
                elif choice == "HELP": self.state = "HELP"; self.show_help()
                elif choice == "EXIT": self.root.destroy()
        elif self.state in ["TOP5", "HELP"]:
            if key in ["Return", "Escape"]: self.state = "MENU"; self.show_menu()
        elif self.state == "GAME":
            if not self.game_over:
                if key == "Left": self.move(-1, 0)
                elif key == "Right": self.move(1, 0)
                elif key == "Down": self.move(0, 1)
                elif key == "Up": self.rotate()
            elif key in ["Return", "Escape"]: self.state = "MENU"; self.show_menu()

    def spawn_piece(self):
        shapes = [[(0, 1), (1, 1), (2, 1), (3, 1)], [(1, 1), (2, 1), (1, 2), (2, 2)], 
                  [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (2, 0), (0, 1), (1, 1)], 
                  [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, 1), (1, 1), (2, 1)], [(2, 0), (0, 1), (1, 1), (2, 1)]]
        self.current_piece = {'coords': random.choice(shapes), 
                              'color': random.choice(['#FF3131', '#0FFF50', '#BCFF00', '#FF00FF', '#00FFFF', '#FFBF00', '#39FF14']), 
                              'x': 3, 'y': 0}
        if self.check_collision(0, 0):
            self.game_over = True
            self.draw()
            self.check_high_score()

    def check_collision(self, dx, dy, piece_coords=None):
        coords = piece_coords or self.current_piece['coords']
        for px, py in coords:
            nx, ny = px + self.current_piece['x'] + dx, py + self.current_piece['y'] + dy
            if nx < 0 or nx >= COLUMNS or ny >= ROWS or (ny >= 0 and self.grid[ny][nx]): return True
        return False

    def move(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            self.draw()
            return True
        elif dy > 0: self.lock_piece()
        return False

    def rotate(self):
        new_coords = [(-y, x) for x, y in self.current_piece['coords']]
        mx, my = min(x for x, y in new_coords), min(y for x, y in new_coords)
        new_coords = [(x - mx, y - my) for x, y in new_coords]
        if not self.check_collision(0, 0, new_coords):
            self.current_piece['coords'] = new_coords
            self.draw()

    def lock_piece(self):
        for px, py in self.current_piece['coords']:
            self.grid[py + self.current_piece['y']][px + self.current_piece['x']] = self.current_piece['color']
        full_lines = [i for i, row in enumerate(self.grid) if all(row)]
        for i in full_lines:
            del self.grid[i]
            self.grid.insert(0, [None for _ in range(COLUMNS)])
            self.score += 100
        self.level = (self.score // 500) + 1
        self.speed = max(100, 500 - (self.level * 40))
        self.spawn_piece()
        self.draw()

    def draw(self):
        if self.state != "GAME": return
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 600, 300, 640, fill="#333333", outline="")
        self.canvas.create_text(10, 620, anchor="w", text=f"SCORE: {self.score}  LVL: {self.level}", fill="#0FFF50", font=('Consolas', 10, 'bold'))
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color: self.draw_tile(x, y, color)
        if not self.game_over:
            for px, py in self.current_piece['coords']:
                self.draw_tile(px + self.current_piece['x'], py + self.current_piece['y'], self.current_piece['color'])
        else:
            self.canvas.create_rectangle(50, 250, 250, 350, fill="#222", outline="#FF3131", width=2)
            self.canvas.create_text(150, 300, text=f"GAME OVER\n{self.score} PTS\n[ENTER]", fill="#FF3131", font=('Consolas', 16, 'bold'), justify="center")

    def draw_tile(self, x, y, color):
        self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill=color, outline="#444444", width=1)

    def run_game_loop(self):
        if self.state == "GAME" and not self.game_over:
            self.move(0, 1)
            self.root.after(self.speed, self.run_game_loop)

def main():
    root = tk.Tk()
    game = Tetris(root)
    root.mainloop()

if __name__ == "__main__":
    main()
