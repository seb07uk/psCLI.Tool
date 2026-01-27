#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
polsoft.ITS™ CMD Terminal v1.5.0.25.1.26 - ZINTEGROWANY
Terminal z wbudowanym modułem dokumentacji technicznej

Autor: Sebastian Januchowski
Email: polsoft.its@fastservice.com
GitHub: https://github.com/seb07uk
© 2026 polsoft.ITS™ London
"""

import os
import sys
import subprocess
import platform
import json
import datetime
import shutil
from pathlib import Path

# Import modułu dokumentacji
from terminal_docs_module import TerminalDocumentation, Colors

class IntegratedTerminal:
    """Terminal z wbudowaną dokumentacją"""
    
    def __init__(self):
        self.version = "1.5.0.25.1.26"
        self.commands = []
        self.aliases = {}
        self.history = []
        self.current_dir = os.getcwd()
        self.venv_active = False
        self.venv_path = None
        
        # Zintegrowany moduł dokumentacji
        self.doc_generator = TerminalDocumentation()
        
        # Katalogi
        self.base_dir = Path.home() / ".polsoft" / "Terminal"
        self.metadata_dir = self.base_dir / "metadata"
        self.modules_dir = self.base_dir / "modules"
        
        # Inicjalizacja
        self._init_directories()
        self._register_commands()
        
    def _init_directories(self):
        """Tworzy strukturę katalogów"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(exist_ok=True)
        self.modules_dir.mkdir(exist_ok=True)
        
        # Utwórz README w modules
        readme_path = self.modules_dir / "README.txt"
        if not readme_path.exists():
            readme_path.write_text(
                "Katalog na niestandardowe moduły\n"
                "================================\n\n"
                "Wspierane formaty:\n"
                "  • .py - Skrypty Python\n"
                "  • .exe - Programy wykonywalne\n"
                "  • .bat, .cmd - Skrypty Batch\n"
                "  • .vbs - VBScript\n"
                "  • .ps1 - PowerShell\n"
                "  • .jar - Aplikacje Java\n\n"
                "Użycie: <nazwa_modułu> [argumenty]\n"
            )
    
    def _register_commands(self):
        """Rejestruje wszystkie komendy terminala"""
        self.commands = {
            # Podstawowe
            'help': self.cmd_help,
            'exit': self.cmd_exit,
            'clear': self.cmd_clear,
            'version': self.cmd_version,
            
            # Nawigacja
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'ls': self.cmd_ls,
            'dir': self.cmd_ls,
            
            # Pliki
            'cat': self.cmd_cat,
            'touch': self.cmd_touch,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'cp': self.cmd_cp,
            'mv': self.cmd_mv,
            
            # Venv
            'venv': self.cmd_venv,
            'venv-create': self.cmd_venv_create,
            'venv-activate': self.cmd_venv_activate,
            'venv-deactivate': self.cmd_venv_deactivate,
            'venv-list': self.cmd_venv_list,
            'venv-delete': self.cmd_venv_delete,
            
            # System
            'sysinfo': self.cmd_sysinfo,
            'env': self.cmd_env,
            'which': self.cmd_which,
            'whereis': self.cmd_whereis,
            
            # Historia
            'history': self.cmd_history,
            'history-clear': self.cmd_history_clear,
            'history-export': self.cmd_history_export,
            
            # Aliasy
            'alias': self.cmd_alias,
            'unalias': self.cmd_unalias,
            'alias-list': self.cmd_alias_list,
            'alias-export': self.cmd_alias_export,
            
            # Metadata
            'metadata': self.cmd_metadata,
            'metadata-export': self.cmd_metadata_export,
            'metadata-import': self.cmd_metadata_import,
            
            # Moduły
            'modules': self.cmd_modules,
            'module-info': self.cmd_module_info,
            'module-install': self.cmd_module_install,
            
            # ★ NOWA KOMENDA DOKUMENTACJI ★
            'docs': self.cmd_docs,
            'doc': self.cmd_docs,  # Alias
            'documentation': self.cmd_docs,  # Alias
            'man': self.cmd_docs,  # Alias w stylu Unix
        }
    
    # ========================================================================
    # KOMENDY DOKUMENTACJI - NOWE!
    # ========================================================================
    
    def cmd_docs(self, args):
        """
        Wyświetla dokumentację techniczną terminala
        
        Użycie:
            docs                    - Pełna dokumentacja (tekst)
            docs --format md        - Format Markdown
            docs --format html      - Format HTML
            docs --section commands - Tylko komendy
            docs --export           - Eksportuj do pliku
            docs --help             - Pomoc
        """
        if not args:
            # Wyświetl pełną dokumentację
            content = self.doc_generator.generate_full_documentation('txt')
            self._display_paginated(content)
            return True
        
        # Parsowanie argumentów
        format_type = 'txt'
        export = False
        section = 'all'
        output_file = None
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg == '--help' or arg == '-h':
                print(f"{Colors.CYAN}Dokumentacja terminala{Colors.RESET}")
                print()
                print("Użycie:")
                print("  docs                    - Pełna dokumentacja")
                print("  docs --format <format>  - Wybierz format (txt/md/html)")
                print("  docs --section <sekcja> - Wybierz sekcję")
                print("  docs --export           - Eksportuj do pliku")
                print("  docs --output <plik>    - Zapisz do konkretnego pliku")
                print()
                print("Przykłady:")
                print("  docs --format md --export")
                print("  docs --section commands")
                print("  docs --output dokumentacja.html --format html")
                return True
            
            elif arg == '--format' or arg == '-f':
                if i + 1 < len(args):
                    format_type = args[i + 1]
                    i += 1
                    if format_type not in ['txt', 'md', 'html']:
                        print(f"{Colors.RED}Błąd: Nieznany format '{format_type}'{Colors.RESET}")
                        print(f"{Colors.YELLOW}Dostępne: txt, md, html{Colors.RESET}")
                        return False
            
            elif arg == '--section' or arg == '-s':
                if i + 1 < len(args):
                    section = args[i + 1]
                    i += 1
            
            elif arg == '--export' or arg == '-e':
                export = True
            
            elif arg == '--output' or arg == '-o':
                if i + 1 < len(args):
                    output_file = args[i + 1]
                    export = True
                    i += 1
            
            i += 1
        
        # Generuj dokumentację
        print(f"{Colors.CYAN}Generowanie dokumentacji...{Colors.RESET}")
        content = self.doc_generator.generate_full_documentation(format_type)
        
        if export:
            # Eksportuj do pliku
            filename = self.doc_generator.export_to_file(content, output_file)
            if filename:
                print(f"{Colors.GREEN}✓ Dokumentacja zapisana: {filename}{Colors.RESET}")
                print(f"{Colors.CYAN}Rozmiar: {len(content)} znaków{Colors.RESET}")
                print(f"{Colors.CYAN}Format: {format_type.upper()}{Colors.RESET}")
            return True
        else:
            # Wyświetl w terminalu
            self._display_paginated(content)
            return True
    
    def _display_paginated(self, content, lines_per_page=30):
        """Wyświetla treść z paginacją"""
        lines = content.split('\n')
        total_lines = len(lines)
        current_line = 0
        
        print(f"{Colors.YELLOW}Dokumentacja ({total_lines} linii){Colors.RESET}")
        print(f"{Colors.YELLOW}Naciśnij ENTER aby kontynuować, 'q' aby wyjść{Colors.RESET}")
        print("=" * 80)
        
        while current_line < total_lines:
            # Wyświetl stronę
            end_line = min(current_line + lines_per_page, total_lines)
            for line in lines[current_line:end_line]:
                print(line)
            
            current_line = end_line
            
            if current_line < total_lines:
                # Czekaj na input użytkownika
                print()
                print(f"{Colors.CYAN}[{current_line}/{total_lines}] ENTER=dalej, q=wyjście{Colors.RESET}", end='')
                user_input = input().strip().lower()
                
                if user_input == 'q':
                    print(f"{Colors.YELLOW}Przerwano wyświetlanie{Colors.RESET}")
                    break
                
                print()  # Nowa linia przed następną stroną
    
    # ========================================================================
    # PODSTAWOWE KOMENDY
    # ========================================================================
    
    def cmd_help(self, args):
        """Wyświetla pomoc"""
        if args and args[0] in self.commands:
            # Pomoc dla konkretnej komendy
            cmd_func = self.commands[args[0]]
            if cmd_func.__doc__:
                print(f"{Colors.CYAN}{args[0]}{Colors.RESET}")
                print(cmd_func.__doc__)
            else:
                print(f"Brak dokumentacji dla komendy '{args[0]}'")
            return True
        
        # Lista wszystkich komend
        print(f"{Colors.BOLD}polsoft.ITS™ CMD Terminal v{self.version}{Colors.RESET}")
        print()
        print(f"{Colors.CYAN}Dostępne komendy ({len(self.commands)}):{Colors.RESET}")
        print()
        
        categories = {
            'Podstawowe': ['help', 'exit', 'clear', 'version'],
            'Nawigacja': ['cd', 'pwd', 'ls', 'dir'],
            'Pliki': ['cat', 'touch', 'mkdir', 'rm', 'cp', 'mv'],
            'Venv': ['venv', 'venv-create', 'venv-activate', 'venv-deactivate', 'venv-list', 'venv-delete'],
            'System': ['sysinfo', 'env', 'which', 'whereis'],
            'Historia': ['history', 'history-clear', 'history-export'],
            'Aliasy': ['alias', 'unalias', 'alias-list', 'alias-export'],
            'Metadata': ['metadata', 'metadata-export', 'metadata-import'],
            'Moduły': ['modules', 'module-info', 'module-install'],
            'Dokumentacja': ['docs', 'doc', 'documentation', 'man'],
        }
        
        for category, cmds in categories.items():
            print(f"{Colors.YELLOW}{category}:{Colors.RESET}")
            for cmd in cmds:
                if cmd in self.commands:
                    print(f"  {cmd}")
            print()
        
        print(f"{Colors.GREEN}Użyj 'help <komenda>' aby uzyskać szczegóły{Colors.RESET}")
        print(f"{Colors.GREEN}Użyj 'docs' aby wyświetlić pełną dokumentację{Colors.RESET}")
        return True
    
    def cmd_exit(self, args):
        """Wyjście z terminala"""
        print(f"{Colors.YELLOW}Zamykanie terminala...{Colors.RESET}")
        sys.exit(0)
    
    def cmd_clear(self, args):
        """Czyści ekran"""
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        return True
    
    def cmd_version(self, args):
        """Wyświetla wersję terminala"""
        print(f"{Colors.BOLD}polsoft.ITS™ CMD Terminal{Colors.RESET}")
        print(f"Wersja: {Colors.CYAN}{self.version}{Colors.RESET}")
        print(f"Python: {Colors.CYAN}{sys.version.split()[0]}{Colors.RESET}")
        print(f"Platforma: {Colors.CYAN}{platform.system()} {platform.release()}{Colors.RESET}")
        print(f"Komendy: {Colors.CYAN}{len(self.commands)}{Colors.RESET}")
        print()
        print(f"{Colors.GREEN}Użyj 'docs' aby wyświetlić dokumentację{Colors.RESET}")
        return True
    
    # ========================================================================
    # NAWIGACJA
    # ========================================================================
    
    def cmd_cd(self, args):
        """Zmienia katalog roboczy"""
        if not args:
            # Przejdź do katalogu domowego
            os.chdir(Path.home())
            self.current_dir = os.getcwd()
        else:
            try:
                os.chdir(args[0])
                self.current_dir = os.getcwd()
            except FileNotFoundError:
                print(f"{Colors.RED}Błąd: Katalog nie istnieje{Colors.RESET}")
                return False
            except PermissionError:
                print(f"{Colors.RED}Błąd: Brak uprawnień{Colors.RESET}")
                return False
        return True
    
    def cmd_pwd(self, args):
        """Wyświetla bieżący katalog"""
        print(self.current_dir)
        return True
    
    def cmd_ls(self, args):
        """Listuje zawartość katalogu"""
        path = args[0] if args else '.'
        try:
            items = os.listdir(path)
            for item in sorted(items):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(f"{Colors.BLUE}{item}/{Colors.RESET}")
                else:
                    print(item)
        except FileNotFoundError:
            print(f"{Colors.RED}Błąd: Katalog nie istnieje{Colors.RESET}")
            return False
        except PermissionError:
            print(f"{Colors.RED}Błąd: Brak uprawnień{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # OPERACJE NA PLIKACH
    # ========================================================================
    
    def cmd_cat(self, args):
        """Wyświetla zawartość pliku"""
        if not args:
            print(f"{Colors.RED}Użycie: cat <plik>{Colors.RESET}")
            return False
        
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"{Colors.RED}Błąd: Plik nie istnieje{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_touch(self, args):
        """Tworzy pusty plik"""
        if not args:
            print(f"{Colors.RED}Użycie: touch <plik>{Colors.RESET}")
            return False
        
        try:
            Path(args[0]).touch()
            print(f"{Colors.GREEN}✓ Utworzono: {args[0]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_mkdir(self, args):
        """Tworzy katalog"""
        if not args:
            print(f"{Colors.RED}Użycie: mkdir <katalog>{Colors.RESET}")
            return False
        
        try:
            os.makedirs(args[0], exist_ok=True)
            print(f"{Colors.GREEN}✓ Utworzono: {args[0]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_rm(self, args):
        """Usuwa plik lub katalog"""
        if not args:
            print(f"{Colors.RED}Użycie: rm <plik/katalog>{Colors.RESET}")
            return False
        
        try:
            path = Path(args[0])
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            else:
                print(f"{Colors.RED}Błąd: Ścieżka nie istnieje{Colors.RESET}")
                return False
            print(f"{Colors.GREEN}✓ Usunięto: {args[0]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_cp(self, args):
        """Kopiuje plik"""
        if len(args) < 2:
            print(f"{Colors.RED}Użycie: cp <źródło> <cel>{Colors.RESET}")
            return False
        
        try:
            shutil.copy2(args[0], args[1])
            print(f"{Colors.GREEN}✓ Skopiowano: {args[0]} → {args[1]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_mv(self, args):
        """Przenosi/zmienia nazwę pliku"""
        if len(args) < 2:
            print(f"{Colors.RED}Użycie: mv <źródło> <cel>{Colors.RESET}")
            return False
        
        try:
            shutil.move(args[0], args[1])
            print(f"{Colors.GREEN}✓ Przeniesiono: {args[0]} → {args[1]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # VENV
    # ========================================================================
    
    def cmd_venv(self, args):
        """Zarządza środowiskami wirtualnymi Python"""
        if not args:
            print(f"{Colors.CYAN}Zarządzanie venv:{Colors.RESET}")
            print("  venv-create <nazwa>     - Tworzy venv")
            print("  venv-activate <nazwa>   - Aktywuje venv")
            print("  venv-deactivate         - Dezaktywuje venv")
            print("  venv-list               - Lista venv")
            print("  venv-delete <nazwa>     - Usuwa venv")
            return True
        
        return self.commands.get(f'venv-{args[0]}', lambda x: False)(args[1:])
    
    def cmd_venv_create(self, args):
        """Tworzy nowe środowisko wirtualne"""
        if not args:
            print(f"{Colors.RED}Użycie: venv-create <nazwa>{Colors.RESET}")
            return False
        
        venv_path = self.base_dir / "venvs" / args[0]
        if venv_path.exists():
            print(f"{Colors.YELLOW}Venv już istnieje: {args[0]}{Colors.RESET}")
            return False
        
        try:
            print(f"{Colors.CYAN}Tworzenie venv: {args[0]}...{Colors.RESET}")
            subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
            print(f"{Colors.GREEN}✓ Utworzono venv: {args[0]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_venv_activate(self, args):
        """Aktywuje środowisko wirtualne"""
        if not args:
            print(f"{Colors.RED}Użycie: venv-activate <nazwa>{Colors.RESET}")
            return False
        
        venv_path = self.base_dir / "venvs" / args[0]
        if not venv_path.exists():
            print(f"{Colors.RED}Błąd: Venv nie istnieje: {args[0]}{Colors.RESET}")
            return False
        
        self.venv_active = True
        self.venv_path = venv_path
        print(f"{Colors.GREEN}✓ Aktywowano venv: {args[0]}{Colors.RESET}")
        return True
    
    def cmd_venv_deactivate(self, args):
        """Dezaktywuje środowisko wirtualne"""
        if not self.venv_active:
            print(f"{Colors.YELLOW}Brak aktywnego venv{Colors.RESET}")
            return False
        
        self.venv_active = False
        self.venv_path = None
        print(f"{Colors.GREEN}✓ Dezaktywowano venv{Colors.RESET}")
        return True
    
    def cmd_venv_list(self, args):
        """Listuje środowiska wirtualne"""
        venvs_dir = self.base_dir / "venvs"
        if not venvs_dir.exists():
            print(f"{Colors.YELLOW}Brak środowisk wirtualnych{Colors.RESET}")
            return True
        
        venvs = [d.name for d in venvs_dir.iterdir() if d.is_dir()]
        if not venvs:
            print(f"{Colors.YELLOW}Brak środowisk wirtualnych{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}Środowiska wirtualne:{Colors.RESET}")
            for venv in venvs:
                marker = f" {Colors.GREEN}(aktywne){Colors.RESET}" if (
                    self.venv_active and self.venv_path.name == venv
                ) else ""
                print(f"  • {venv}{marker}")
        return True
    
    def cmd_venv_delete(self, args):
        """Usuwa środowisko wirtualne"""
        if not args:
            print(f"{Colors.RED}Użycie: venv-delete <nazwa>{Colors.RESET}")
            return False
        
        venv_path = self.base_dir / "venvs" / args[0]
        if not venv_path.exists():
            print(f"{Colors.RED}Błąd: Venv nie istnieje: {args[0]}{Colors.RESET}")
            return False
        
        if self.venv_active and self.venv_path == venv_path:
            print(f"{Colors.RED}Błąd: Nie można usunąć aktywnego venv{Colors.RESET}")
            return False
        
        try:
            shutil.rmtree(venv_path)
            print(f"{Colors.GREEN}✓ Usunięto venv: {args[0]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # SYSTEM
    # ========================================================================
    
    def cmd_sysinfo(self, args):
        """Wyświetla informacje o systemie"""
        print(f"{Colors.CYAN}Informacje systemowe:{Colors.RESET}")
        print(f"  System: {platform.system()}")
        print(f"  Wersja: {platform.release()}")
        print(f"  Architektura: {platform.machine()}")
        print(f"  Python: {sys.version.split()[0]}")
        print(f"  Katalog roboczy: {self.current_dir}")
        print(f"  Katalog domowy: {Path.home()}")
        return True
    
    def cmd_env(self, args):
        """Wyświetla zmienne środowiskowe"""
        if not args:
            for key, value in os.environ.items():
                print(f"{Colors.CYAN}{key}{Colors.RESET}={value}")
        else:
            value = os.environ.get(args[0])
            if value:
                print(f"{Colors.CYAN}{args[0]}{Colors.RESET}={value}")
            else:
                print(f"{Colors.YELLOW}Zmienna nie istnieje: {args[0]}{Colors.RESET}")
        return True
    
    def cmd_which(self, args):
        """Znajduje lokalizację programu"""
        if not args:
            print(f"{Colors.RED}Użycie: which <program>{Colors.RESET}")
            return False
        
        path = shutil.which(args[0])
        if path:
            print(path)
        else:
            print(f"{Colors.RED}Nie znaleziono: {args[0]}{Colors.RESET}")
            return False
        return True
    
    def cmd_whereis(self, args):
        """Alias dla which"""
        return self.cmd_which(args)
    
    # ========================================================================
    # HISTORIA
    # ========================================================================
    
    def cmd_history(self, args):
        """Wyświetla historię komend"""
        if not self.history:
            print(f"{Colors.YELLOW}Historia jest pusta{Colors.RESET}")
            return True
        
        for i, cmd in enumerate(self.history, 1):
            print(f"{Colors.CYAN}{i:4d}{Colors.RESET}  {cmd}")
        return True
    
    def cmd_history_clear(self, args):
        """Czyści historię"""
        self.history.clear()
        print(f"{Colors.GREEN}✓ Historia wyczyszczona{Colors.RESET}")
        return True
    
    def cmd_history_export(self, args):
        """Eksportuje historię do pliku"""
        filename = args[0] if args else f"history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.metadata_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            print(f"{Colors.GREEN}✓ Wyeksportowano historię: {filepath}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # ALIASY
    # ========================================================================
    
    def cmd_alias(self, args):
        """Tworzy alias dla komendy"""
        if not args:
            return self.cmd_alias_list([])
        
        if '=' not in ' '.join(args):
            print(f"{Colors.RED}Użycie: alias <nazwa>=<komenda>{Colors.RESET}")
            return False
        
        full_arg = ' '.join(args)
        name, command = full_arg.split('=', 1)
        name = name.strip()
        command = command.strip()
        
        self.aliases[name] = command
        print(f"{Colors.GREEN}✓ Utworzono alias: {name} → {command}{Colors.RESET}")
        return True
    
    def cmd_unalias(self, args):
        """Usuwa alias"""
        if not args:
            print(f"{Colors.RED}Użycie: unalias <nazwa>{Colors.RESET}")
            return False
        
        if args[0] in self.aliases:
            del self.aliases[args[0]]
            print(f"{Colors.GREEN}✓ Usunięto alias: {args[0]}{Colors.RESET}")
        else:
            print(f"{Colors.RED}Alias nie istnieje: {args[0]}{Colors.RESET}")
            return False
        return True
    
    def cmd_alias_list(self, args):
        """Listuje aliasy"""
        if not self.aliases:
            print(f"{Colors.YELLOW}Brak aliasów{Colors.RESET}")
            return True
        
        print(f"{Colors.CYAN}Aliasy:{Colors.RESET}")
        for name, command in self.aliases.items():
            print(f"  {name} → {command}")
        return True
    
    def cmd_alias_export(self, args):
        """Eksportuje aliasy do pliku"""
        filename = args[0] if args else f"aliases_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.metadata_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.aliases, f, indent=2, ensure_ascii=False)
            print(f"{Colors.GREEN}✓ Wyeksportowano aliasy: {filepath}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # METADATA
    # ========================================================================
    
    def cmd_metadata(self, args):
        """Wyświetla metadane terminala"""
        print(f"{Colors.CYAN}Metadane terminala:{Colors.RESET}")
        print(f"  Wersja: {self.version}")
        print(f"  Katalog bazowy: {self.base_dir}")
        print(f"  Katalog metadata: {self.metadata_dir}")
        print(f"  Katalog modules: {self.modules_dir}")
        print(f"  Liczba komend: {len(self.commands)}")
        print(f"  Liczba aliasów: {len(self.aliases)}")
        print(f"  Historia: {len(self.history)} pozycji")
        print(f"  Venv aktywne: {'Tak' if self.venv_active else 'Nie'}")
        return True
    
    def cmd_metadata_export(self, args):
        """Eksportuje metadane do pliku"""
        metadata = {
            'version': self.version,
            'timestamp': datetime.datetime.now().isoformat(),
            'commands': list(self.commands.keys()),
            'aliases': self.aliases,
            'history_count': len(self.history),
            'venv_active': self.venv_active,
            'current_dir': self.current_dir,
        }
        
        filename = args[0] if args else f"metadata_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.metadata_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"{Colors.GREEN}✓ Wyeksportowano metadane: {filepath}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    def cmd_metadata_import(self, args):
        """Importuje metadane z pliku"""
        if not args:
            print(f"{Colors.RED}Użycie: metadata-import <plik>{Colors.RESET}")
            return False
        
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Załaduj aliasy jeśli są dostępne
            if 'aliases' in metadata:
                self.aliases.update(metadata['aliases'])
                print(f"{Colors.GREEN}✓ Zaimportowano {len(metadata['aliases'])} aliasów{Colors.RESET}")
            
            print(f"{Colors.GREEN}✓ Zaimportowano metadane z: {args[0]}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # MODUŁY
    # ========================================================================
    
    def cmd_modules(self, args):
        """Listuje niestandardowe moduły"""
        if not self.modules_dir.exists():
            print(f"{Colors.YELLOW}Katalog modułów nie istnieje{Colors.RESET}")
            return True
        
        modules = [f for f in self.modules_dir.iterdir() if f.is_file() and f.suffix in [
            '.py', '.exe', '.bat', '.cmd', '.vbs', '.ps1', '.jar'
        ]]
        
        if not modules:
            print(f"{Colors.YELLOW}Brak modułów{Colors.RESET}")
            print(f"{Colors.CYAN}Katalog modułów: {self.modules_dir}{Colors.RESET}")
            return True
        
        print(f"{Colors.CYAN}Dostępne moduły ({len(modules)}):{ Colors.RESET}")
        for module in sorted(modules):
            print(f"  • {module.name}")
        
        print()
        print(f"{Colors.GREEN}Użyj '<nazwa_modułu> [args]' aby uruchomić{Colors.RESET}")
        return True
    
    def cmd_module_info(self, args):
        """Wyświetla informacje o module"""
        if not args:
            print(f"{Colors.RED}Użycie: module-info <nazwa>{Colors.RESET}")
            return False
        
        module_path = self.modules_dir / args[0]
        if not module_path.exists():
            print(f"{Colors.RED}Moduł nie istnieje: {args[0]}{Colors.RESET}")
            return False
        
        print(f"{Colors.CYAN}Informacje o module:{Colors.RESET}")
        print(f"  Nazwa: {module_path.name}")
        print(f"  Ścieżka: {module_path}")
        print(f"  Rozmiar: {module_path.stat().st_size} bajtów")
        print(f"  Typ: {module_path.suffix}")
        print(f"  Ostatnia modyfikacja: {datetime.datetime.fromtimestamp(module_path.stat().st_mtime)}")
        return True
    
    def cmd_module_install(self, args):
        """Instaluje moduł (kopiuje plik do katalogu modules)"""
        if not args:
            print(f"{Colors.RED}Użycie: module-install <ścieżka_do_pliku>{Colors.RESET}")
            return False
        
        source = Path(args[0])
        if not source.exists():
            print(f"{Colors.RED}Plik nie istnieje: {args[0]}{Colors.RESET}")
            return False
        
        dest = self.modules_dir / source.name
        if dest.exists():
            print(f"{Colors.YELLOW}Moduł już istnieje: {source.name}{Colors.RESET}")
            response = input("Nadpisać? (t/n): ").strip().lower()
            if response != 't':
                print(f"{Colors.YELLOW}Anulowano{Colors.RESET}")
                return False
        
        try:
            shutil.copy2(source, dest)
            print(f"{Colors.GREEN}✓ Zainstalowano moduł: {source.name}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
            return False
        return True
    
    # ========================================================================
    # GŁÓWNA PĘTLA
    # ========================================================================
    
    def execute(self, command_line):
        """Wykonuje komendę"""
        if not command_line.strip():
            return True
        
        # Zapisz w historii
        self.history.append(command_line)
        
        # Parsuj komendę
        parts = command_line.split()
        command = parts[0]
        args = parts[1:]
        
        # Sprawdź aliasy
        if command in self.aliases:
            expanded = self.aliases[command]
            return self.execute(f"{expanded} {' '.join(args)}")
        
        # Wykonaj komendę wbudowaną
        if command in self.commands:
            try:
                return self.commands[command](args)
            except Exception as e:
                print(f"{Colors.RED}Błąd wykonania komendy: {e}{Colors.RESET}")
                return False
        
        # Sprawdź moduły niestandardowe
        module_path = self.modules_dir / command
        if module_path.exists():
            return self._execute_module(module_path, args)
        
        # Sprawdź moduły z rozszerzeniem
        for ext in ['.py', '.exe', '.bat', '.cmd', '.vbs', '.ps1', '.jar']:
            module_path = self.modules_dir / f"{command}{ext}"
            if module_path.exists():
                return self._execute_module(module_path, args)
        
        # Nieznana komenda
        print(f"{Colors.RED}Nieznana komenda: {command}{Colors.RESET}")
        print(f"{Colors.YELLOW}Użyj 'help' aby zobaczyć dostępne komendy{Colors.RESET}")
        return False
    
    def _execute_module(self, module_path, args):
        """Wykonuje moduł niestandardowy"""
        try:
            if module_path.suffix == '.py':
                # Python
                cmd = [sys.executable, str(module_path)] + args
            elif module_path.suffix == '.jar':
                # Java
                cmd = ['java', '-jar', str(module_path)] + args
            elif module_path.suffix == '.ps1':
                # PowerShell
                cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(module_path)] + args
            else:
                # Inne (.exe, .bat, .cmd, .vbs)
                cmd = [str(module_path)] + args
            
            result = subprocess.run(cmd, capture_output=False)
            return result.returncode == 0
        
        except Exception as e:
            print(f"{Colors.RED}Błąd wykonania modułu: {e}{Colors.RESET}")
            return False
    
    def run(self):
        """Uruchamia główną pętlę terminala"""
        # Banner
        print(f"{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD}║  polsoft.ITS™ CMD Terminal v{self.version}                  ║{Colors.RESET}")
        print(f"{Colors.BOLD}║  Zintegrowany z modułem dokumentacji                         ║{Colors.RESET}")
        print(f"{Colors.BOLD}╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
        print()
        print(f"{Colors.GREEN}Użyj 'help' aby zobaczyć dostępne komendy{Colors.RESET}")
        print(f"{Colors.GREEN}Użyj 'docs' aby wyświetlić pełną dokumentację{Colors.RESET}")
        print(f"{Colors.YELLOW}Użyj 'exit' aby wyjść{Colors.RESET}")
        print()
        
        # Główna pętla
        while True:
            try:
                # Prompt
                venv_marker = f"{Colors.GREEN}(venv){Colors.RESET} " if self.venv_active else ""
                prompt = f"{venv_marker}{Colors.CYAN}{os.path.basename(self.current_dir)}{Colors.RESET} > "
                
                command_line = input(prompt).strip()
                
                if command_line:
                    self.execute(command_line)
            
            except KeyboardInterrupt:
                print()
                print(f"{Colors.YELLOW}Użyj 'exit' aby wyjść{Colors.RESET}")
            except EOFError:
                print()
                break


def main():
    """Główna funkcja"""
    terminal = IntegratedTerminal()
    terminal.run()


if __name__ == "__main__":
    main()
