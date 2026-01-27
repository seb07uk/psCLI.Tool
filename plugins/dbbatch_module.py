#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODUŁ DBBATCH - ZARZĄDZANIE BIBLIOTEKAMI SKRYPTÓW BAT/CMD
polsoft.ITS™ CMD Terminal v1.5.0.25.1.26

Kompleksowy system zarządzania bibliotekami, bazami danych i skryptami BAT/CMD.

Funkcje:
  • Baza danych skryptów BAT/CMD/PS1/VBS
  • Biblioteki tematyczne skryptów
  • Generator dokumentacji z grafiką polsoft.ITS™
  • Katalogowanie i wersjonowanie
  • Eksport do HTML/JSON/CSV
  • Integracja z terminalem
  • Szablony skryptów (basic, advanced, menu)
  • Analiza i walidacja składni
  • Statystyki i analityka

Autor: Sebastian Januchowski  
Email: polsoft.its@fastservice.com
GitHub: https://github.com/seb07uk
© 2026 polsoft.ITS™ London
"""

import sys
import os
import json
import sqlite3
import datetime
import hashlib
import shutil
from pathlib import Path
from textwrap import dedent
import base64

# Kolory ANSI
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


class BatchScriptDatabase:
    """Baza danych skryptów BAT/CMD"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            self.base_dir = Path.home() / ".polsoft" / "Terminal" / "dbbatch"
            self.base_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = self.base_dir / "scripts.db"
        else:
            self.db_path = Path(db_path)
            self.base_dir = self.db_path.parent
            self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self.cursor = None
        
        # Katalogi
        self.scripts_dir = self.base_dir / "scripts"
        self.docs_dir = self.base_dir / "documentation"
        self.exports_dir = self.base_dir / "exports"
        
        for dir_path in [self.scripts_dir, self.docs_dir, self.exports_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"{Colors.RED}Błąd połączenia: {e}{Colors.RESET}")
            return False
    
    def init_database(self):
        if not self.connect():
            return False
        
        try:
            # Tabela skryptów
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS scripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    filepath TEXT UNIQUE NOT NULL,
                    title TEXT,
                    description TEXT,
                    content TEXT,
                    type TEXT,
                    version TEXT,
                    author TEXT DEFAULT 'polsoft.ITS™',
                    hash TEXT,
                    tags TEXT,
                    category TEXT,
                    commands_count INTEGER DEFAULT 0,
                    lines_count INTEGER DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Tabela bibliotek
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS libraries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    type TEXT DEFAULT 'batch',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    script_count INTEGER DEFAULT 0
                )
            """)
            
            # Tabela powiązań
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS library_scripts (
                    library_id INTEGER,
                    script_id INTEGER,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (library_id) REFERENCES libraries(id),
                    FOREIGN KEY (script_id) REFERENCES scripts(id),
                    PRIMARY KEY (library_id, script_id)
                )
            """)
            
            # Indeksy
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_filename ON scripts(filename)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON scripts(type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON scripts(category)")
            
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Baza danych zainicjalizowana{Colors.RESET}")
            print(f"{Colors.CYAN}  Lokalizacja: {self.base_dir}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Błąd inicjalizacji: {e}{Colors.RESET}")
            return False
    
    def add_script(self, filepath, title=None, description=None, 
                   category=None, tags=None, copy_to_lib=True):
        if not self.connect():
            return False
        
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"{Colors.RED}Plik nie istnieje: {filepath}{Colors.RESET}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            script_type = filepath.suffix.lower()
            lines_count = len(content.split('\n'))
            commands_count = self._count_commands(content)
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            if not title:
                title = self._extract_title(content)
            if not description:
                description = self._extract_description(content)
            
            if copy_to_lib:
                dest_path = self.scripts_dir / filepath.name
                shutil.copy2(filepath, dest_path)
                filepath = dest_path
            
            self.cursor.execute("SELECT id FROM scripts WHERE filepath = ?", (str(filepath),))
            existing = self.cursor.fetchone()
            
            if existing:
                print(f"{Colors.YELLOW}Skrypt już istnieje w bazie{Colors.RESET}")
                return existing['id']
            
            self.cursor.execute("""
                INSERT INTO scripts (filename, filepath, title, description, content,
                                   type, hash, tags, category, commands_count, lines_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (filepath.name, str(filepath), title, description, content,
                  script_type, content_hash, tags, category, commands_count, lines_count))
            
            script_id = self.cursor.lastrowid
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Dodano skrypt: {filepath.name}{Colors.RESET}")
            print(f"{Colors.CYAN}  ID: {script_id} | Linii: {lines_count} | Komend: {commands_count}{Colors.RESET}")
            return script_id
            
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
    
    def _count_commands(self, content):
        count = 0
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('::') or line.startswith('REM'):
                continue
            if any(cmd in line.upper() for cmd in [
                'ECHO', 'SET', 'IF', 'FOR', 'GOTO', 'CALL', 'CD', 'MKDIR', 'DEL'
            ]):
                count += 1
        return count
    
    def _extract_title(self, content):
        for line in content.split('\n')[:10]:
            line = line.strip()
            if line.startswith('::') or line.upper().startswith('REM'):
                return line.lstrip(':').lstrip('REM').strip()
        return "Bez tytułu"
    
    def _extract_description(self, content):
        desc_lines = []
        for line in content.split('\n')[:20]:
            line = line.strip()
            if line.startswith('::') or line.upper().startswith('REM'):
                desc_lines.append(line.lstrip(':').lstrip('REM').strip())
            if len(desc_lines) >= 3:
                break
        return ' '.join(desc_lines) if desc_lines else "Brak opisu"
    
    def list_scripts(self, limit=None, category=None, script_type=None):
        if not self.connect():
            return []
        
        try:
            query = "SELECT * FROM scripts WHERE status = 'active'"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            if script_type:
                query += " AND type = ?"
                params.append(script_type)
            
            query += " ORDER BY modified_date DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return []
    
    def search_scripts(self, query):
        if not self.connect():
            return []
        
        try:
            search_query = f"%{query}%"
            self.cursor.execute("""
                SELECT * FROM scripts 
                WHERE status = 'active'
                AND (filename LIKE ? OR title LIKE ? OR description LIKE ? 
                     OR content LIKE ? OR tags LIKE ?)
                ORDER BY modified_date DESC
            """, (search_query, search_query, search_query, search_query, search_query))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return []
    
    def create_library(self, name, description=None):
        if not self.connect():
            return False
        
        try:
            self.cursor.execute("""
                INSERT INTO libraries (name, description)
                VALUES (?, ?)
            """, (name, description))
            
            library_id = self.cursor.lastrowid
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Utworzono bibliotekę: {name}{Colors.RESET}")
            return library_id
        except sqlite3.IntegrityError:
            print(f"{Colors.YELLOW}Biblioteka już istnieje: {name}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
    
    def add_to_library(self, library_name, script_id):
        if not self.connect():
            return False
        
        try:
            self.cursor.execute("SELECT id FROM libraries WHERE name = ?", (library_name,))
            library = self.cursor.fetchone()
            
            if not library:
                print(f"{Colors.RED}Biblioteka nie istnieje: {library_name}{Colors.RESET}")
                return False
            
            self.cursor.execute("""
                INSERT OR IGNORE INTO library_scripts (library_id, script_id)
                VALUES (?, ?)
            """, (library['id'], script_id))
            
            self.cursor.execute("""
                UPDATE libraries 
                SET script_count = (
                    SELECT COUNT(*) FROM library_scripts WHERE library_id = ?
                )
                WHERE id = ?
            """, (library['id'], library['id']))
            
            self.conn.commit()
            print(f"{Colors.GREEN}✓ Dodano do biblioteki: {library_name}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
    
    def get_stats(self):
        if not self.connect():
            return None
        
        try:
            stats = {}
            
            self.cursor.execute("SELECT COUNT(*) as count FROM scripts WHERE status = 'active'")
            stats['scripts'] = self.cursor.fetchone()['count']
            
            self.cursor.execute("SELECT COUNT(*) as count FROM libraries")
            stats['libraries'] = self.cursor.fetchone()['count']
            
            self.cursor.execute("""
                SELECT type, COUNT(*) as count 
                FROM scripts WHERE status = 'active'
                GROUP BY type
            """)
            stats['types'] = dict(self.cursor.fetchall())
            
            self.cursor.execute("SELECT SUM(lines_count) as total FROM scripts WHERE status = 'active'")
            stats['total_lines'] = self.cursor.fetchone()['total'] or 0
            
            stats['db_size'] = os.path.getsize(self.db_path)
            
            return stats
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return None
    
    def close(self):
        if self.conn:
            self.conn.close()


class BatchDocumentationGenerator:
    """Generator dokumentacji z grafiką polsoft.ITS™"""
    
    def __init__(self, db):
        self.db = db
        self.logo_data = None
    
    def set_logo(self, logo_path):
        try:
            with open(logo_path, 'rb') as f:
                self.logo_data = base64.b64encode(f.read()).decode()
            return True
        except Exception as e:
            print(f"{Colors.YELLOW}Nie można wczytać logo: {e}{Colors.RESET}")
            return False
    
    def generate_html_docs(self, script_id, output_path):
        if not self.db.connect():
            return False
        
        try:
            self.db.cursor.execute("SELECT * FROM scripts WHERE id = ?", (script_id,))
            script = self.db.cursor.fetchone()
            
            if not script:
                print(f"{Colors.RED}Skrypt nie istnieje: ID {script_id}{Colors.RESET}")
                return False
            
            html = self._generate_html(script)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"{Colors.GREEN}✓ Wygenerowano dokumentację: {output_path}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
    
    def _generate_html(self, script):
        title = script['title'] or script['filename']
        logo_html = ""
        if self.logo_data:
            logo_html = f'<img src="data:image/png;base64,{self.logo_data}" style="max-width: 400px; margin: 20px 0;">'
        
        html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Dokumentacja: {title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .logo-container {{ text-align: center; padding: 20px; background: #f8f9fa; }}
        .content {{ padding: 40px; }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .info-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .info-card .value {{ font-size: 2em; font-weight: bold; }}
        .section {{
            margin-bottom: 30px;
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .section h2 {{ color: #667eea; margin-bottom: 15px; }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 25px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📜 Dokumentacja Skryptu</h1>
            <p>{script['filename']}</p>
        </div>
        
        <div class="logo-container">
            {logo_html}
            <p style="color: #666;">polsoft.ITS™ Batch Script Database</p>
        </div>
        
        <div class="content">
            <div class="info-grid">
                <div class="info-card">
                    <h3>Linii kodu</h3>
                    <div class="value">{script['lines_count']}</div>
                </div>
                <div class="info-card">
                    <h3>Komend</h3>
                    <div class="value">{script['commands_count']}</div>
                </div>
                <div class="info-card">
                    <h3>Typ</h3>
                    <div class="value" style="font-size: 1.5em;">{script['type']}</div>
                </div>
            </div>
            
            <div class="section">
                <h2>Informacje</h2>
                <h3>{title}</h3>
                <p style="color: #666; margin-top: 10px;">{script['description']}</p>
                <p style="margin-top: 15px;"><strong>Kategoria:</strong> {script['category'] or 'Brak'}</p>
                <p><strong>Tagi:</strong> {script['tags'] or 'Brak'}</p>
                <p><strong>Utworzono:</strong> {script['created_date']}</p>
            </div>
            
            <div class="section">
                <h2>Kod źródłowy</h2>
                <pre><code>{script['content']}</code></pre>
            </div>
        </div>
        
        <div class="footer">
            <h3>polsoft.ITS™ Batch Script Database</h3>
            <p>Sebastian Januchowski • polsoft.its@fastservice.com</p>
            <p style="margin-top: 10px; opacity: 0.7;">© 2026 polsoft.ITS™ London</p>
        </div>
    </div>
</body>
</html>"""
        return html


class BatchTemplateGenerator:
    """Generator szablonów skryptów"""
    
    @staticmethod
    def generate_basic():
        return dedent("""
        @echo off
        :: ============================================
        :: Skrypt: [NAZWA]
        :: Autor: polsoft.ITS™
        :: Data: {date}
        :: ============================================
        
        setlocal EnableDelayedExpansion
        
        echo Uruchamianie skryptu...
        echo Data: %DATE% %TIME%
        
        :: TODO: Dodaj swój kod tutaj
        
        echo Zakończono.
        pause
        
        endlocal
        exit /b 0
        """).format(date=datetime.datetime.now().strftime('%Y-%m-%d'))
    
    @staticmethod
    def generate_advanced():
        return dedent("""
        @echo off
        :: ============================================
        :: Zaawansowany skrypt BAT
        :: polsoft.ITS™ - {date}
        :: ============================================
        
        setlocal EnableDelayedExpansion
        
        :: Kolory
        set "GREEN=[92m"
        set "RED=[91m"
        set "RESET=[0m"
        
        :: Konfiguracja
        set "SCRIPT_NAME=%~n0"
        set "LOG_FILE=%SCRIPT_NAME%.log"
        
        echo %GREEN%[OK]%RESET% Uruchamianie skryptu
        
        :: TODO: Dodaj logikę
        
        echo %GREEN%[OK]%RESET% Zakończono
        pause
        
        endlocal
        exit /b 0
        """).format(date=datetime.datetime.now().strftime('%Y-%m-%d'))
    
    @staticmethod
    def generate_menu():
        return dedent("""
        @echo off
        :: ============================================
        :: Menu Skryptu - polsoft.ITS™
        :: ============================================
        
        :menu
        cls
        echo ========================================
        echo         polsoft.ITS - Menu
        echo ========================================
        echo.
        echo  [1] Opcja 1
        echo  [2] Opcja 2
        echo  [3] Opcja 3
        echo  [0] Wyjście
        echo.
        set /p choice="Wybierz (0-3): "
        
        if "%choice%"=="1" goto option1
        if "%choice%"=="2" goto option2
        if "%choice%"=="3" goto option3
        if "%choice%"=="0" goto exit
        
        echo Nieprawidłowy wybór!
        pause
        goto menu
        
        :option1
        echo Opcja 1...
        pause
        goto menu
        
        :option2
        echo Opcja 2...
        pause
        goto menu
        
        :option3
        echo Opcja 3...
        pause
        goto menu
        
        :exit
        exit /b 0
        """)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='dbbatch - Zarządzanie skryptami BAT/CMD')
    parser.add_argument('command', help='Komenda')
    parser.add_argument('args', nargs='*', help='Argumenty')
    parser.add_argument('--title', help='Tytuł')
    parser.add_argument('--description', help='Opis')
    parser.add_argument('--category', help='Kategoria')
    parser.add_argument('--tags', help='Tagi')
    parser.add_argument('--logo', help='Ścieżka do logo PNG')
    
    args = parser.parse_args()
    db = BatchScriptDatabase()
    command = args.command.lower()
    
    if command == 'init':
        db.init_database()
    
    elif command == 'add':
        if not args.args:
            print(f"{Colors.RED}Podaj ścieżkę do pliku{Colors.RESET}")
            sys.exit(1)
        db.add_script(args.args[0], title=args.title, description=args.description,
                     category=args.category, tags=args.tags)
    
    elif command == 'list':
        scripts = db.list_scripts(category=args.category)
        if scripts:
            print(f"{Colors.CYAN}Znaleziono {len(scripts)} skryptów:{Colors.RESET}\n")
            for s in scripts:
                print(f"{Colors.GREEN}[{s['id']}]{Colors.RESET} {s['filename']}")
                print(f"  📄 {s['title']}")
                print(f"  📊 Linii: {s['lines_count']} | Komend: {s['commands_count']}")
                print()
    
    elif command == 'search':
        if not args.args:
            print(f"{Colors.RED}Podaj zapytanie{Colors.RESET}")
            sys.exit(1)
        results = db.search_scripts(' '.join(args.args))
        print(f"{Colors.CYAN}Znaleziono {len(results)} wyników{Colors.RESET}\n")
        for s in results:
            print(f"{Colors.GREEN}[{s['id']}]{Colors.RESET} {s['filename']}")
            print(f"  {s['title']}\n")
    
    elif command == 'library':
        if not args.args:
            print(f"{Colors.RED}Podaj akcję (create/add){Colors.RESET}")
            sys.exit(1)
        action = args.args[0]
        if action == 'create' and len(args.args) > 1:
            db.create_library(args.args[1], args.description)
        elif action == 'add' and len(args.args) > 2:
            db.add_to_library(args.args[1], int(args.args[2]))
    
    elif command == 'stats':
        stats = db.get_stats()
        if stats:
            print(f"{Colors.CYAN}Statystyki:{Colors.RESET}\n")
            print(f"Skrypty: {stats['scripts']}")
            print(f"Biblioteki: {stats['libraries']}")
            print(f"Linii kodu: {stats['total_lines']:,}")
            print(f"Rozmiar bazy: {stats['db_size']:,} B")
    
    elif command == 'template':
        if not args.args:
            print(f"{Colors.RED}Podaj typ (basic/advanced/menu){Colors.RESET}")
            sys.exit(1)
        gen = BatchTemplateGenerator()
        ttype = args.args[0]
        if ttype == 'basic':
            print(gen.generate_basic())
        elif ttype == 'advanced':
            print(gen.generate_advanced())
        elif ttype == 'menu':
            print(gen.generate_menu())
    
    elif command == 'doc':
        if not args.args:
            print(f"{Colors.RED}Podaj ID skryptu{Colors.RESET}")
            sys.exit(1)
        script_id = int(args.args[0])
        output = args.args[1] if len(args.args) > 1 else f"script_{script_id}_docs.html"
        
        doc_gen = BatchDocumentationGenerator(db)
        if args.logo:
            doc_gen.set_logo(args.logo)
        doc_gen.generate_html_docs(script_id, output)
    
    else:
        print(f"{Colors.RED}Nieznana komenda: {command}{Colors.RESET}")
    
    db.close()


if __name__ == "__main__":
    main()
