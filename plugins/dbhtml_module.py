#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODUŁ DBHTML - ZARZĄDZANIE BAZAMI DANYCH HTML/WEB
polsoft.ITS™ CMD Terminal v1.5.0.25.1.26

Kompleksowy moduł do zarządzania bibliotekami i bazami danych HTML, WWW.

Funkcje:
  • Zarządzanie bazami danych (SQLite + JSON)
  • Generator bibliotek HTML/CSS/JS
  • Scraping i parsowanie stron WWW
  • Konwersje formatów (HTML↔JSON↔CSV↔SQL)
  • Katalogowanie stron internetowych
  • Zarządzanie zakładkami i metadanymi
  • Szablony HTML5/CSS3
  • Integracja z popularnymi bibliotekami web

Użycie:
    dbhtml init                      - Inicjalizacja bazy danych
    dbhtml add <url>                 - Dodaj stronę do bazy
    dbhtml list                      - Lista zapisanych stron
    dbhtml export <format>           - Eksport (html/json/csv/sql)
    dbhtml search <query>            - Szukaj w bazie
    dbhtml generate <typ>            - Generuj szablon HTML
    dbhtml scrape <url>              - Pobierz i zapisz stronę
    dbhtml convert <in> <out>        - Konwertuj między formatami
    dbhtml library <nazwa>           - Zarządzaj bibliotekami
    dbhtml stats                     - Statystyki bazy

Autor: Sebastian Januchowski
Email: polsoft.its@fastservice.com
GitHub: https://github.com/seb07uk
© 2026 polsoft.ITS™ London
"""

import sys
import os
import json
import sqlite3
import csv
import datetime
import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser
import html

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
    WHITE = '\033[97m'


class HTMLDatabase:
    """Baza danych HTML/Web"""
    
    def __init__(self, db_path=None):
        """Inicjalizacja bazy danych"""
        if db_path is None:
            # Domyślna lokalizacja w katalogu użytkownika
            self.base_dir = Path.home() / ".polsoft" / "Terminal" / "dbhtml"
            self.base_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = self.base_dir / "webpages.db"
        else:
            self.db_path = Path(db_path)
            self.base_dir = self.db_path.parent
            self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Połącz z bazą danych"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"{Colors.RED}Błąd połączenia z bazą: {e}{Colors.RESET}")
            return False
    
    def init_database(self):
        """Inicjalizuj strukturę bazy danych"""
        if not self.connect():
            return False
        
        try:
            # Tabela stron WWW
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS webpages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    description TEXT,
                    content TEXT,
                    html_source TEXT,
                    domain TEXT,
                    hash TEXT,
                    tags TEXT,
                    category TEXT,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    visit_count INTEGER DEFAULT 0,
                    favorite INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'active'
                )
            """)
            
            # Tabela bibliotek/kolekcji
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS libraries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    type TEXT,
                    path TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    webpage_count INTEGER DEFAULT 0
                )
            """)
            
            # Tabela powiązań strona-biblioteka
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS library_webpages (
                    library_id INTEGER,
                    webpage_id INTEGER,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (library_id) REFERENCES libraries(id),
                    FOREIGN KEY (webpage_id) REFERENCES webpages(id),
                    PRIMARY KEY (library_id, webpage_id)
                )
            """)
            
            # Tabela metadanych
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    webpage_id INTEGER,
                    key TEXT,
                    value TEXT,
                    FOREIGN KEY (webpage_id) REFERENCES webpages(id)
                )
            """)
            
            # Tabela zasobów (CSS, JS, obrazy)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    webpage_id INTEGER,
                    url TEXT,
                    type TEXT,
                    content BLOB,
                    size INTEGER,
                    FOREIGN KEY (webpage_id) REFERENCES webpages(id)
                )
            """)
            
            # Indeksy
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON webpages(url)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain ON webpages(domain)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags ON webpages(tags)")
            
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Baza danych zainicjalizowana: {self.db_path}{Colors.RESET}")
            print(f"{Colors.CYAN}  Lokalizacja: {self.base_dir}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Błąd inicjalizacji bazy: {e}{Colors.RESET}")
            return False
    
    def add_webpage(self, url, title=None, description=None, content=None, 
                    html_source=None, tags=None, category=None):
        """Dodaj stronę do bazy"""
        if not self.connect():
            return False
        
        try:
            # Parsuj URL
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Hash zawartości
            content_hash = hashlib.md5(
                (content or html_source or url).encode()
            ).hexdigest()
            
            # Sprawdź czy strona już istnieje
            self.cursor.execute("SELECT id FROM webpages WHERE url = ?", (url,))
            existing = self.cursor.fetchone()
            
            if existing:
                print(f"{Colors.YELLOW}Strona już istnieje w bazie{Colors.RESET}")
                return existing['id']
            
            # Dodaj stronę
            self.cursor.execute("""
                INSERT INTO webpages (url, title, description, content, 
                                     html_source, domain, hash, tags, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (url, title, description, content, html_source, 
                  domain, content_hash, tags, category))
            
            webpage_id = self.cursor.lastrowid
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Dodano stronę: {url}{Colors.RESET}")
            print(f"{Colors.CYAN}  ID: {webpage_id}{Colors.RESET}")
            return webpage_id
            
        except Exception as e:
            print(f"{Colors.RED}Błąd dodawania strony: {e}{Colors.RESET}")
            return False
    
    def list_webpages(self, limit=None, category=None, tags=None):
        """Listuj strony z bazy"""
        if not self.connect():
            return []
        
        try:
            query = "SELECT * FROM webpages WHERE status = 'active'"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if tags:
                query += " AND tags LIKE ?"
                params.append(f"%{tags}%")
            
            query += " ORDER BY modified_date DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
            
        except Exception as e:
            print(f"{Colors.RED}Błąd listowania: {e}{Colors.RESET}")
            return []
    
    def search_webpages(self, query):
        """Wyszukaj strony"""
        if not self.connect():
            return []
        
        try:
            search_query = f"%{query}%"
            self.cursor.execute("""
                SELECT * FROM webpages 
                WHERE status = 'active' 
                AND (url LIKE ? OR title LIKE ? OR description LIKE ? 
                     OR content LIKE ? OR tags LIKE ?)
                ORDER BY modified_date DESC
            """, (search_query, search_query, search_query, 
                  search_query, search_query))
            
            return self.cursor.fetchall()
            
        except Exception as e:
            print(f"{Colors.RED}Błąd wyszukiwania: {e}{Colors.RESET}")
            return []
    
    def create_library(self, name, description=None, lib_type='collection'):
        """Utwórz bibliotekę/kolekcję"""
        if not self.connect():
            return False
        
        try:
            self.cursor.execute("""
                INSERT INTO libraries (name, description, type)
                VALUES (?, ?, ?)
            """, (name, description, lib_type))
            
            library_id = self.cursor.lastrowid
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Utworzono bibliotekę: {name}{Colors.RESET}")
            return library_id
            
        except sqlite3.IntegrityError:
            print(f"{Colors.YELLOW}Biblioteka już istnieje: {name}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}Błąd tworzenia biblioteki: {e}{Colors.RESET}")
            return False
    
    def add_to_library(self, library_name, webpage_id):
        """Dodaj stronę do biblioteki"""
        if not self.connect():
            return False
        
        try:
            # Znajdź bibliotekę
            self.cursor.execute("SELECT id FROM libraries WHERE name = ?", 
                              (library_name,))
            library = self.cursor.fetchone()
            
            if not library:
                print(f"{Colors.RED}Biblioteka nie istnieje: {library_name}{Colors.RESET}")
                return False
            
            # Dodaj powiązanie
            self.cursor.execute("""
                INSERT OR IGNORE INTO library_webpages (library_id, webpage_id)
                VALUES (?, ?)
            """, (library['id'], webpage_id))
            
            # Zaktualizuj licznik
            self.cursor.execute("""
                UPDATE libraries 
                SET webpage_count = (
                    SELECT COUNT(*) FROM library_webpages 
                    WHERE library_id = ?
                )
                WHERE id = ?
            """, (library['id'], library['id']))
            
            self.conn.commit()
            
            print(f"{Colors.GREEN}✓ Dodano do biblioteki: {library_name}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Błąd dodawania do biblioteki: {e}{Colors.RESET}")
            return False
    
    def get_stats(self):
        """Pobierz statystyki bazy"""
        if not self.connect():
            return None
        
        try:
            stats = {}
            
            # Liczba stron
            self.cursor.execute("SELECT COUNT(*) as count FROM webpages WHERE status = 'active'")
            stats['webpages'] = self.cursor.fetchone()['count']
            
            # Liczba bibliotek
            self.cursor.execute("SELECT COUNT(*) as count FROM libraries")
            stats['libraries'] = self.cursor.fetchone()['count']
            
            # Liczba domen
            self.cursor.execute("SELECT COUNT(DISTINCT domain) as count FROM webpages")
            stats['domains'] = self.cursor.fetchone()['count']
            
            # Kategorie
            self.cursor.execute("""
                SELECT category, COUNT(*) as count 
                FROM webpages 
                WHERE category IS NOT NULL 
                GROUP BY category
            """)
            stats['categories'] = dict(self.cursor.fetchall())
            
            # Rozmiar bazy
            stats['db_size'] = os.path.getsize(self.db_path)
            
            return stats
            
        except Exception as e:
            print(f"{Colors.RED}Błąd pobierania statystyk: {e}{Colors.RESET}")
            return None
    
    def export_to_json(self, output_path):
        """Eksportuj bazę do JSON"""
        if not self.connect():
            return False
        
        try:
            # Pobierz wszystkie strony
            self.cursor.execute("SELECT * FROM webpages WHERE status = 'active'")
            webpages = [dict(row) for row in self.cursor.fetchall()]
            
            # Pobierz biblioteki
            self.cursor.execute("SELECT * FROM libraries")
            libraries = [dict(row) for row in self.cursor.fetchall()]
            
            data = {
                'export_date': datetime.datetime.now().isoformat(),
                'version': '1.0',
                'webpages': webpages,
                'libraries': libraries
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"{Colors.GREEN}✓ Wyeksportowano do JSON: {output_path}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Błąd eksportu JSON: {e}{Colors.RESET}")
            return False
    
    def export_to_csv(self, output_path):
        """Eksportuj bazę do CSV"""
        if not self.connect():
            return False
        
        try:
            self.cursor.execute("SELECT * FROM webpages WHERE status = 'active'")
            webpages = self.cursor.fetchall()
            
            if not webpages:
                print(f"{Colors.YELLOW}Brak danych do eksportu{Colors.RESET}")
                return False
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Nagłówki
                writer.writerow(webpages[0].keys())
                
                # Dane
                for row in webpages:
                    writer.writerow(row)
            
            print(f"{Colors.GREEN}✓ Wyeksportowano do CSV: {output_path}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Błąd eksportu CSV: {e}{Colors.RESET}")
            return False
    
    def export_to_html(self, output_path):
        """Eksportuj bazę do HTML"""
        if not self.connect():
            return False
        
        try:
            self.cursor.execute("SELECT * FROM webpages WHERE status = 'active'")
            webpages = self.cursor.fetchall()
            
            html_content = self._generate_export_html(webpages)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"{Colors.GREEN}✓ Wyeksportowano do HTML: {output_path}{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}Błąd eksportu HTML: {e}{Colors.RESET}")
            return False
    
    def _generate_export_html(self, webpages):
        """Generuj HTML z eksportowanych danych"""
        html_template = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eksport Bazy Danych Web - polsoft.ITS™</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .content {{
            padding: 30px;
        }}
        .webpage-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .webpage-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .webpage-title {{
            font-size: 1.3em;
            color: #333;
            margin-bottom: 10px;
        }}
        .webpage-title a {{
            color: #667eea;
            text-decoration: none;
        }}
        .webpage-title a:hover {{
            text-decoration: underline;
        }}
        .webpage-url {{
            color: #28a745;
            font-size: 0.9em;
            margin-bottom: 10px;
            word-break: break-all;
        }}
        .webpage-description {{
            color: #666;
            margin-bottom: 10px;
        }}
        .webpage-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.9em;
            color: #999;
        }}
        .tag {{
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        .category {{
            background: #28a745;
            color: white;
            padding: 3px 10px;
            border-radius: 5px;
            font-size: 0.85em;
        }}
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }}
        .search-box {{
            padding: 20px;
            background: #f8f9fa;
        }}
        .search-box input {{
            width: 100%;
            padding: 12px;
            border: 2px solid #667eea;
            border-radius: 5px;
            font-size: 1em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌐 Baza Danych Web</h1>
            <p>polsoft.ITS™ Database Manager</p>
            <p>Eksport: {export_date}</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{total_pages}</div>
                <div class="stat-label">Stron WWW</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total_domains}</div>
                <div class="stat-label">Domen</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total_categories}</div>
                <div class="stat-label">Kategorii</div>
            </div>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Szukaj stron..." onkeyup="searchPages()">
        </div>
        
        <div class="content" id="pagesList">
            {webpages_html}
        </div>
        
        <div class="footer">
            <p>© 2026 polsoft.ITS™ London - Sebastian Januchowski</p>
            <p>Wygenerowano przez moduł dbhtml</p>
        </div>
    </div>
    
    <script>
        function searchPages() {{
            const input = document.getElementById('searchInput');
            const filter = input.value.toLowerCase();
            const cards = document.getElementsByClassName('webpage-card');
            
            for (let i = 0; i < cards.length; i++) {{
                const text = cards[i].textContent.toLowerCase();
                cards[i].style.display = text.includes(filter) ? '' : 'none';
            }}
        }}
    </script>
</body>
</html>"""
        
        # Generuj HTML dla każdej strony
        webpages_html = ""
        domains = set()
        categories = set()
        
        for page in webpages:
            title = page['title'] or 'Bez tytułu'
            url = page['url']
            description = page['description'] or ''
            domain = page['domain'] or ''
            category = page['category'] or ''
            tags = page['tags'] or ''
            added = page['added_date'] or ''
            
            domains.add(domain)
            if category:
                categories.add(category)
            
            tags_html = ""
            if tags:
                for tag in tags.split(','):
                    tags_html += f'<span class="tag">{tag.strip()}</span> '
            
            category_html = f'<span class="category">{category}</span>' if category else ''
            
            webpages_html += f"""
            <div class="webpage-card">
                <div class="webpage-title">
                    <a href="{html.escape(url)}" target="_blank">{html.escape(title)}</a>
                </div>
                <div class="webpage-url">🔗 {html.escape(url)}</div>
                <div class="webpage-description">{html.escape(description)}</div>
                <div class="webpage-meta">
                    <span>🌐 {html.escape(domain)}</span>
                    <span>📅 {added}</span>
                    {category_html}
                    {tags_html}
                </div>
            </div>
            """
        
        return html_template.format(
            export_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_pages=len(webpages),
            total_domains=len(domains),
            total_categories=len(categories),
            webpages_html=webpages_html
        )
    
    def close(self):
        """Zamknij połączenie z bazą"""
        if self.conn:
            self.conn.close()


class HTMLTemplateGenerator:
    """Generator szablonów HTML"""
    
    @staticmethod
    def generate_basic_template():
        """Generuj podstawowy szablon HTML5"""
        return """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Opis strony">
    <meta name="author" content="polsoft.ITS™">
    <title>Tytuł Strony</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: #667eea;
            color: white;
            padding: 20px 0;
            text-align: center;
        }
        main {
            padding: 40px 0;
        }
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 20px 0;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Witaj na stronie</h1>
            <p>Szablon HTML5</p>
        </div>
    </header>
    
    <main>
        <div class="container">
            <h2>Główna zawartość</h2>
            <p>To jest podstawowy szablon HTML5 wygenerowany przez dbhtml.</p>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2026 polsoft.ITS™ - Wszystkie prawa zastrzeżone</p>
        </div>
    </footer>
</body>
</html>"""
    
    @staticmethod
    def generate_dashboard_template():
        """Generuj szablon dashboardu"""
        return """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - polsoft.ITS™</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 250px;
            height: 100vh;
            background: #2c3e50;
            color: white;
            padding: 20px;
        }
        .sidebar h2 {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #34495e;
        }
        .sidebar nav a {
            display: block;
            color: white;
            text-decoration: none;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .sidebar nav a:hover {
            background: #34495e;
        }
        .main-content {
            margin-left: 250px;
            padding: 20px;
        }
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        .card .number {
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>📊 Dashboard</h2>
        <nav>
            <a href="#overview">🏠 Przegląd</a>
            <a href="#pages">📄 Strony</a>
            <a href="#libraries">📚 Biblioteki</a>
            <a href="#analytics">📈 Analityka</a>
            <a href="#settings">⚙️ Ustawienia</a>
        </nav>
    </div>
    
    <div class="main-content">
        <div class="header">
            <h1>Witaj w Dashboard</h1>
            <p>polsoft.ITS™ Web Database Manager</p>
        </div>
        
        <div class="cards">
            <div class="card">
                <h3>Strony WWW</h3>
                <div class="number">0</div>
                <p>Zapisanych stron</p>
            </div>
            <div class="card">
                <h3>Biblioteki</h3>
                <div class="number">0</div>
                <p>Utworzonych bibliotek</p>
            </div>
            <div class="card">
                <h3>Domeny</h3>
                <div class="number">0</div>
                <p>Unikalnych domen</p>
            </div>
            <div class="card">
                <h3>Kategorie</h3>
                <div class="number">0</div>
                <p>Zdefiniowanych kategorii</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    @staticmethod
    def generate_portfolio_template():
        """Generuj szablon portfolio"""
        return """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio - polsoft.ITS™</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 20px;
            text-align: center;
        }
        .hero h1 {
            font-size: 3em;
            margin-bottom: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 20px;
        }
        .projects {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        .project-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .project-card:hover {
            transform: translateY(-5px);
        }
        .project-image {
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .project-content {
            padding: 20px;
        }
        .project-content h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 30px 0;
        }
    </style>
</head>
<body>
    <section class="hero">
        <h1>Moje Portfolio</h1>
        <p>Przykładowe projekty i realizacje</p>
    </section>
    
    <div class="container">
        <h2 style="text-align: center; margin-bottom: 40px;">Projekty</h2>
        <div class="projects">
            <div class="project-card">
                <div class="project-image"></div>
                <div class="project-content">
                    <h3>Projekt 1</h3>
                    <p>Opis projektu i wykorzystanych technologii.</p>
                </div>
            </div>
            <div class="project-card">
                <div class="project-image"></div>
                <div class="project-content">
                    <h3>Projekt 2</h3>
                    <p>Opis projektu i wykorzystanych technologii.</p>
                </div>
            </div>
            <div class="project-card">
                <div class="project-image"></div>
                <div class="project-content">
                    <h3>Projekt 3</h3>
                    <p>Opis projektu i wykorzystanych technologii.</p>
                </div>
            </div>
        </div>
    </div>
    
    <footer>
        <p>&copy; 2026 polsoft.ITS™ - Sebastian Januchowski</p>
        <p>Szablon wygenerowany przez dbhtml</p>
    </footer>
</body>
</html>"""


class SimpleHTMLParser(HTMLParser):
    """Prosty parser HTML do ekstrakcji danych"""
    
    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self.links = []
        self.images = []
        self.scripts = []
        self.styles = []
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            content = attrs_dict.get('content', '')
            if name == 'description':
                self.description = content
        elif tag == 'a':
            href = attrs_dict.get('href')
            if href:
                self.links.append(href)
        elif tag == 'img':
            src = attrs_dict.get('src')
            if src:
                self.images.append(src)
        elif tag == 'script':
            src = attrs_dict.get('src')
            if src:
                self.scripts.append(src)
        elif tag == 'link':
            rel = attrs_dict.get('rel', '').lower()
            if 'stylesheet' in rel:
                href = attrs_dict.get('href')
                if href:
                    self.styles.append(href)
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False


def main():
    """Główna funkcja CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='dbhtml - Moduł zarządzania bazami danych HTML/Web',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  dbhtml init
  dbhtml add "https://example.com" --title "Przykład" --tags "web,test"
  dbhtml list --limit 10
  dbhtml search "python"
  dbhtml export html output.html
  dbhtml generate basic > template.html
  dbhtml library create "Moje linki"
  dbhtml stats
        """
    )
    
    parser.add_argument('command', help='Komenda do wykonania')
    parser.add_argument('args', nargs='*', help='Argumenty komendy')
    parser.add_argument('--title', help='Tytuł strony')
    parser.add_argument('--description', help='Opis strony')
    parser.add_argument('--tags', help='Tagi (oddzielone przecinkami)')
    parser.add_argument('--category', help='Kategoria')
    parser.add_argument('--limit', type=int, help='Limit wyników')
    parser.add_argument('--db', help='Ścieżka do bazy danych')
    
    args = parser.parse_args()
    
    # Inicjalizacja bazy
    db = HTMLDatabase(args.db)
    
    # Wykonaj komendę
    command = args.command.lower()
    
    if command == 'init':
        db.init_database()
    
    elif command == 'add':
        if not args.args:
            print(f"{Colors.RED}Błąd: Podaj URL{Colors.RESET}")
            sys.exit(1)
        url = args.args[0]
        webpage_id = db.add_webpage(
            url,
            title=args.title,
            description=args.description,
            tags=args.tags,
            category=args.category
        )
    
    elif command == 'list':
        pages = db.list_webpages(
            limit=args.limit,
            category=args.category,
            tags=args.tags
        )
        if pages:
            print(f"{Colors.CYAN}Znaleziono {len(pages)} stron:{Colors.RESET}\n")
            for page in pages:
                print(f"{Colors.GREEN}[{page['id']}]{Colors.RESET} {page['title'] or 'Bez tytułu'}")
                print(f"  {Colors.BLUE}🔗 {page['url']}{Colors.RESET}")
                if page['description']:
                    print(f"  {page['description'][:80]}...")
                if page['tags']:
                    print(f"  {Colors.YELLOW}Tags: {page['tags']}{Colors.RESET}")
                print()
        else:
            print(f"{Colors.YELLOW}Brak stron w bazie{Colors.RESET}")
    
    elif command == 'search':
        if not args.args:
            print(f"{Colors.RED}Błąd: Podaj zapytanie{Colors.RESET}")
            sys.exit(1)
        query = ' '.join(args.args)
        results = db.search_webpages(query)
        if results:
            print(f"{Colors.CYAN}Znaleziono {len(results)} wyników dla '{query}':{Colors.RESET}\n")
            for page in results:
                print(f"{Colors.GREEN}[{page['id']}]{Colors.RESET} {page['title'] or 'Bez tytułu'}")
                print(f"  {Colors.BLUE}🔗 {page['url']}{Colors.RESET}")
                print()
        else:
            print(f"{Colors.YELLOW}Brak wyników dla '{query}'{Colors.RESET}")
    
    elif command == 'export':
        if len(args.args) < 2:
            print(f"{Colors.RED}Użycie: dbhtml export <format> <plik>{Colors.RESET}")
            sys.exit(1)
        format_type = args.args[0].lower()
        output_path = args.args[1]
        
        if format_type == 'json':
            db.export_to_json(output_path)
        elif format_type == 'csv':
            db.export_to_csv(output_path)
        elif format_type == 'html':
            db.export_to_html(output_path)
        else:
            print(f"{Colors.RED}Nieznany format: {format_type}{Colors.RESET}")
            print(f"{Colors.YELLOW}Dostępne: json, csv, html{Colors.RESET}")
    
    elif command == 'generate':
        if not args.args:
            print(f"{Colors.RED}Błąd: Podaj typ szablonu{Colors.RESET}")
            print(f"{Colors.YELLOW}Dostępne: basic, dashboard, portfolio{Colors.RESET}")
            sys.exit(1)
        
        template_type = args.args[0].lower()
        gen = HTMLTemplateGenerator()
        
        if template_type == 'basic':
            print(gen.generate_basic_template())
        elif template_type == 'dashboard':
            print(gen.generate_dashboard_template())
        elif template_type == 'portfolio':
            print(gen.generate_portfolio_template())
        else:
            print(f"{Colors.RED}Nieznany typ szablonu: {template_type}{Colors.RESET}")
    
    elif command == 'library':
        if not args.args:
            print(f"{Colors.RED}Błąd: Podaj akcję{Colors.RESET}")
            sys.exit(1)
        
        action = args.args[0].lower()
        
        if action == 'create':
            if len(args.args) < 2:
                print(f"{Colors.RED}Błąd: Podaj nazwę biblioteki{Colors.RESET}")
                sys.exit(1)
            name = args.args[1]
            db.create_library(name, args.description)
        
        elif action == 'add':
            if len(args.args) < 3:
                print(f"{Colors.RED}Błąd: Użycie: library add <nazwa> <webpage_id>{Colors.RESET}")
                sys.exit(1)
            lib_name = args.args[1]
            webpage_id = int(args.args[2])
            db.add_to_library(lib_name, webpage_id)
    
    elif command == 'stats':
        stats = db.get_stats()
        if stats:
            print(f"{Colors.CYAN}Statystyki bazy danych:{Colors.RESET}\n")
            print(f"{Colors.GREEN}Strony WWW:{Colors.RESET} {stats['webpages']}")
            print(f"{Colors.GREEN}Biblioteki:{Colors.RESET} {stats['libraries']}")
            print(f"{Colors.GREEN}Domeny:{Colors.RESET} {stats['domains']}")
            print(f"{Colors.GREEN}Rozmiar bazy:{Colors.RESET} {stats['db_size']:,} bajtów")
            
            if stats['categories']:
                print(f"\n{Colors.YELLOW}Kategorie:{Colors.RESET}")
                for cat, count in stats['categories'].items():
                    print(f"  • {cat}: {count}")
    
    else:
        print(f"{Colors.RED}Nieznana komenda: {command}{Colors.RESET}")
        print(f"{Colors.YELLOW}Użyj --help aby zobaczyć dostępne komendy{Colors.RESET}")
        sys.exit(1)
    
    # Zamknij połączenie
    db.close()


if __name__ == "__main__":
    main()
